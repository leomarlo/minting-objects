import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from config.glob import (
    ALLOWED_UPLOAD_EXTENSIONS,
    IMAGE_UPLOAD_FOLDER,
    VISION_BUCKET_NAME
)
from utils.path import (
    export_credential_path, 
    load_env, 
    create_tables_if_with_db,
    create_upload_directory_if_not_there)
from db.utils import create_tables
from db.session import engine, SessionLocal
from db.mock import mockdb
from db.models import (
    Base, 
    User
)
from vision.query import (
    list_product_sets, 
    list_products_and_product_sets,
    list_reference_images_for_product)
from vision.addimage import create_reference_image
from vision.createset import create_product_set
from vision.manage import create_product, add_product_to_product_set, remove_product_from_product_set
from vision.storage import upload_file
from vision.similarity import search_products




# save global enviornment variable to the os
load_env()
export_credential_path()
create_tables_if_with_db()
create_upload_directory_if_not_there(folder=IMAGE_UPLOAD_FOLDER)
# print('GOOGLE_CREDENTIAL_PATH', os.getenv("GOOGLE_CREDENTIAL_PATH"))


# create the flask app
app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000", "http://another.domain"])  # This will allow all origins to access your app. It's okay for development but not for production!


@app.route('/')
def root():
    return jsonify(message="Hello from the Object Minting!")


@app.route('/upload', methods=['POST'])
def upload_file_route():
    result_dict, status = upload_file(
        files=request.files, size=request.content_length)
    return result_dict, status

# @app.route('/vision/listProductSets', methods=['GET'])

@app.route('/vision/listProductSets', methods=['GET'])
def list_product_sets_route():
    sets, status =  list_product_sets(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"))
    print('The sets are', sets)
    return sets, status


@app.route('/vision/searchProductsFromFileName/<filename>/<product_set_id>', methods=['GET'])
def search_products_route(filename, product_set_id):
    # Example usage
    image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'img', filename))

    matched_products, status = search_products(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT"), 
        location=os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"),
        product_set_id=product_set_id, 
        product_category="general-v1", 
        image_path=image_path)
    
    # for result in matched_products:
    #     print(f"Matched product: {result["product_name"]}, score: {result.score}")
    print('matched products', matched_products)
    
    return jsonify([{"name":prod["product_name"], "score": prod["score"]} for prod in matched_products]), status


@app.route('/vision/listProducts', methods=['GET'])
def list_products_route():
    products, status =  list_products_and_product_sets(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"))
    print('The products are', products)
    print('We would like to return the products here')
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
    result_dict, status = upload_file(files=request.files, size=request.content_length)
    if status == 200:
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'img', request.files['file'].filename))
        matched_products, status = search_products(
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT"), 
            location=os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"),
            product_set_id=request.form['product_set_id'], 
            product_category="general-v1", 
            image_path=image_path)
        return jsonify([{"name":prod["product_name"], "score": prod["score"]} for prod in matched_products]), status
    else:
        status = 500
        return result_dict, status


@app.route('/vision/uploadImageToProduct', methods=['POST'])
def upload_image_to_product_route():
    result_dict, status = upload_file(files=request.files, size=request.content_length)
    if status == 200:
        product_id = request.form['product_id']
        blob_name = request.files['file'].filename
        gcs_uri = f"gs://{VISION_BUCKET_NAME}/{blob_name}"
        response_dict, status = create_reference_image(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("GOOGLE_CLOUD_PROJECT_LOCATION"), product_id, gcs_uri)
        return response_dict, status
    else:
        status = 500
        return result_dict, status


@app.route('/createTables', methods=['GET'])
def create_tables_route(): 
    return create_tables(Base, engine)


if __name__ == '__main__':
    print("Starting Flask app...")
    CORS(app)
    app.run(debug=True, port=5000)