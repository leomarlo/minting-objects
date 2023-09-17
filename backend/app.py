import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from config.glob import (
    ALLOWED_UPLOAD_EXTENSIONS,
    IMAGE_UPLOAD_SIZE_LIMIT,
    IMAGE_UPLOAD_FOLDER,
    IMAGE_THUMB_FOLDER,
    VISION_BUCKET_NAME
)
from utils.path import (
    export_credential_path, 
    load_env, 
    create_tables_if_with_db,
    create_directory_if_not_there)
from utils.products import __get_main_product_set_ids
from db.utils import create_tables
from db.session import engine, SessionLocal
from db.mock import mockdb
from db.models import (
    Base, 
    User,
    Image,
)
from db.utils import (
    db_create_image_entry, 
    db_fetch_image_from_filename, 
    db_close_session)
from vision.query import (
    list_product_sets, 
    list_products_and_product_sets,
    list_products_in_product_set,
    list_reference_images_for_product)
from vision.addimage import create_reference_image
from vision.createset import create_product_set
from vision.manage import create_product, add_product_to_product_set, remove_product_from_product_set
from vision.storage import upload_file, allowed_file
from vision.similarity import search_products
from vision.compression import compress_image
from vision.ipfs import upload_image_to_ipfs

from blockchain.minting import mint_token




# save global enviornment variable to the os
load_env()
export_credential_path()
create_tables_if_with_db()
# create path to upload folder with os.path.join and abspath
create_directory_if_not_there(
    folder=os.path.abspath(os.path.join(os.path.dirname(__file__), IMAGE_UPLOAD_FOLDER)))
create_directory_if_not_there(
    folder=os.path.abspath(os.path.join(os.path.dirname(__file__), IMAGE_THUMB_FOLDER)))
# print('GOOGLE_CREDENTIAL_PATH', os.getenv("GOOGLE_CREDENTIAL_PATH"))


# create the flask app
app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000", "http://another.domain"])  # This will allow all origins to access your app. It's okay for development but not for production!

routes = {
    "HOME": {"path":"/"},
    "UPLOAD": {"path":"/upload"},
    "PRODUCT_SETS": {"path": '/vision/listProductSets'},
    "SEARCH_PRODUCTS_FROM_FILE": {"path":"/vision/searchProductsFromFileName", "args":['filename', 'product_set_id']},
    "TEMP_UPLOAD":{"path":"/tempUpload"}
}

@app.route(routes["HOME"]["path"])
def root():
    return jsonify(message="Hello from the Object Minting!")


@app.route(routes["UPLOAD"]["path"], methods=['POST'])
def upload_file_route():
    result_dict, status = upload_file(
        files=request.files, size=request.content_length, session=SessionLocal())
    return result_dict, status


@app.route(routes["TEMP_UPLOAD"]["path"], methods=['POST'])
def temp_upload_file_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # check size
    if int(request.content_length) > IMAGE_UPLOAD_SIZE_LIMIT:
        return jsonify({"error": f'File size too large: {request.content_length}'}), 400
    
    # print the size of the file
    print(f'File size: {request.content_length}')
    # source_file_name = os.path.join(os.path.dirname(__file__), 'img', 'SocksOrNot.jpg')
    filename = os.path.join(IMAGE_UPLOAD_FOLDER, file.filename)
    file.save(filename)
    
    print(f'File name: {filename}')

    allowed_flag = allowed_file(file.filename)

    if not allowed_flag:
        return jsonify({"error": "File type not allowed"}), 400
    
    # save to thumbnails
    thumbnail = os.path.join(IMAGE_THUMB_FOLDER, 'thumb_' + file.filename)
    compress_image(filename, thumbnail)
    # Upload directly to GCS
    destination_blob_name = file.filename
    return {"status":"success"}, 200

# @app.route('/vision/listProductSets', methods=['GET'])
## test write to a file 
@app.route('/testWrite', methods=['GET'])
def test_write():
    with open('testfile.txt', 'w') as f:
        f.write('This is a test.')


@app.route(routes["PRODUCT_SETS"]["path"], methods=['GET'])
def list_product_sets_route():
    sets, status =  list_product_sets(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"))
    print('The sets are', sets)
    return sets, status


@app.route(routes["SEARCH_PRODUCTS_FROM_FILE"]["path"] + '/<filename>/<product_set_id>', methods=['GET'])
def search_products_route(filename, product_set_id):
    # Example usage
    image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'img', filename))

    matched_products, status = search_products(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT"), 
        location=os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"),
        product_set_id=product_set_id, 
        product_category="general-v1", 
        image_path=image_path)
    
    print('matched products', matched_products)
    
    return jsonify([{"name":prod["product_name"], "score": prod["score"]} for prod in matched_products]), status


@app.route('/vision/listProducts', methods=['GET'])
def list_products_route():
    products, status =  list_products_and_product_sets(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"))
    print('The products are', products)
    print('We would like to return the products here')
    return products, status


@app.route('/vision/listProductsInProductSet', methods=['GET'])
def list_products_in_set_route():
    product_set_id = __get_main_product_set_ids()[0]
    products, status =  list_products_in_product_set(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"), product_set_id)
    return products, status


@app.route('/vision/reference_images/<product_id>', methods=['GET'])
def list_reference_images_for_product_route(product_id):
    images, status =  list_reference_images_for_product(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT"), 
        location=os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"),
        product_id=product_id)
    print('The images are', images)
    return images, status


@app.route('/vision/createProductSet', methods=['POST'])
def create_product_set_route():
    product_set_id = request.json['product_set_id']
    product_set_display_name = request.json['product_set_display_name']
    response_dict, status = create_product_set(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"), product_set_id, product_set_display_name)
    return response_dict, status

@app.route('/vision/createProduct', methods=['POST'])
def create_product_route():
    product_id = request.json['product_id']
    product_display_name = request.json['product_display_name']
    product_category = 'general-v1'
    response_dict, status = create_product(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"), product_id, product_display_name, product_category)
    return response_dict, status

@app.route('/vision/addProductToProductSet', methods=['POST'])
def add_product_to_product_set_route():
    product_id = request.json['product_id']
    product_set_id = request.json['product_set_id']
    response_dict, status = add_product_to_product_set(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"), product_id, product_set_id)
    return response_dict, status

@app.route('/vision/createProductAndAddToProductSet', methods=['POST'])
def create_product_and_add_to_product_set_route():
    product_id = request.json['product_id']
    product_display_name = request.json['product_display_name']
    product_category = 'general-v1'
    product_set_id = request.json['product_set_id']
    response_dict, status = create_product(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"), product_id, product_display_name, product_category)
    if status == 200:
        response_dict, status = add_product_to_product_set(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"), product_id, product_set_id)
        return response_dict, status
    else:
        status = 500
        return response_dict, status


@app.route('/vision/removeProductFromProductSet', methods=['POST'])
def remove_product_from_product_set_route():
    product_id = request.json['product_id']
    product_set_id = request.json['product_set_id']
    response_dict, status = remove_product_from_product_set(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"), product_id, product_set_id)
    return response_dict, status


@app.route('/vision/createReferenceImage', methods=['POST'])
def create_reference_image_route():
    product_id = request.json['product_id']
    reference_image_id = request.json['reference_image_id']
    gcs_uri = request.json['gcs_uri']
    response_dict, status = create_reference_image(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"), product_id, reference_image_id, gcs_uri)
    return response_dict, status

@app.route('/vision/uploadImageAndSearchSimilarProducts', methods=['POST'])
def upload_image_and_search_similar_products_route():
    result_dict, status = upload_file(files=request.files, size=request.content_length,
    session=SessionLocal())
    print('uploaded image.', status)
    if status == 200:
        print('trying to find matching products')
        print('the product set id is', request.form['product_set_id'])
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'img', request.files['file'].filename))
        matched_products, status = search_products(
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT"), 
            location=os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"),
            product_set_id=request.form['product_set_id'], 
            product_category="general-v1", 
            image_path=image_path)
        matched_product_info = [
            {
                "name":prod["product_name"], 
                "display":prod["product_display_name"],
                "score": round(prod["score"],4)
            } for prod in matched_products]
        print('mathed product', matched_product_info)
        return jsonify(matched_product_info), status
    else:
        status = 500
        print(result_dict)
        return result_dict, status


@app.route('/vision/uploadImageToProduct', methods=['POST'])
def upload_image_to_product_route():
    result_dict, status = upload_file(files=request.files, size=request.content_length, session=SessionLocal())
    if status == 200:
        product_id = request.form['product_id']
        blob_name = request.files['file'].filename
        gcs_uri = f"gs://{VISION_BUCKET_NAME}/{blob_name}"
        response_dict, status = create_reference_image(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"), product_id, gcs_uri)
        return response_dict, status
    else:
        status = 500
        return result_dict, status
    
@app.route('/vision/createProductAndReferenceImages', methods=['POST'])
def create_product_and_ref_images():
    ## First create the product
    product_id = request.json['product_id']
    product_display_name = request.json['product_display_name']
    product_category = 'general-v1'
    product_set_id = request.json['product_set_id']
    response_dicts = {}
    response_dict, status = create_product(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"), product_id, product_display_name, product_category)
    response_dicts.update({"create_product":response_dict})
    if status == 200:
        print('product has been added')
        response_dict, status = add_product_to_product_set(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"), product_id, product_set_id)
    else:
        print('product has not been added')
        status = 500
        return response_dict, status
    
    response_dicts.update({"add_product_to_product_set":response_dict})
    ## add reference images
    create_ref_images_response = []
    blob_names = request.json['files']
    main_cid = ""
    for blob_name in blob_names:
        gcs_uri = f"gs://{VISION_BUCKET_NAME}/{blob_name}"
        
        response_dict, status = create_reference_image(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"), product_id, gcs_uri)
        

        # mint the token
        db_image_data = db_fetch_image_from_filename(session=SessionLocal(), filename=blob_name)
        main_cid = db_image_data["cid"]
        tx, address = mint_token(address=None, cid=main_cid, product_id=product_id)


        create_ref_images_response.append({"gc_ref":response_dict, "cid":main_cid})

    response_dicts.update({"create_reference_images":create_ref_images_response})
    return response_dicts, status

@app.route('/vision/uploadToIPFS', methods=['GET'])
def upload_to_ipfs_route():
    resp, status = upload_image_to_ipfs('img/carrot2.jpg')
    return jsonify(resp), status


@app.route('/createTables', methods=['GET'])
def create_tables_route(): 
    return create_tables(Base, engine)


if __name__ == '__main__':
    print("Starting Flask app...")
    CORS(app)
    app.run(debug=True, port=5000)