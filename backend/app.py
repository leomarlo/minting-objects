import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from config.glob import (
    ALLOWED_UPLOAD_EXTENSIONS,
    IMAGE_UPLOAD_FOLDER
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
from vision.query import list_product_sets
from vision.addimage import create_reference_image
from vision.createset import create_product_set
from vision.manage import create_product, add_product_to_product_set, remove_product_from_product_set
from vision.storage import upload_blob, delete_blob, allowed_file


# save global enviornment variable to the os
load_env()
export_credential_path()

# create the flask app
app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000", "http://another.domain"])  # This will allow all origins to access your app. It's okay for development but not for production!

create_tables_if_with_db()
create_upload_directory_if_not_there(folder=IMAGE_UPLOAD_FOLDER)

@app.route('/')
def root():
    return jsonify(message="Hello from the Object Minting!")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = os.path.join(IMAGE_UPLOAD_FOLDER, file.filename)
        file.save(filename)
        return jsonify({"message": "File uploaded successfully"}), 200

    return jsonify({"error": "File type not allowed"}), 400

# @app.route('/vision/listProductSets', methods=['GET'])


@app.route('/createTables', methods=['GET'])
def create_tables_route(): 
    return create_tables(Base, engine)


if __name__ == '__main__':
    print("Starting Flask app...")
    CORS(app)
    app.run(debug=True, port=5000)