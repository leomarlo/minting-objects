import os
from vision.clients import __get_storage_client
from flask import jsonify
from config.glob import (
    ALLOWED_UPLOAD_EXTENSIONS,
    IMAGE_UPLOAD_FOLDER,
    IMAGE_THUMB_FOLDER,
    IMAGE_UPLOAD_SIZE_LIMIT,
    VISION_BUCKET_NAME
)
from vision.compression import compress_image
# from utils.path import export_credential_path


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    print('inside upload blob')
    storage_client = __get_storage_client()
    print('storage client')
    bucket = storage_client.bucket(bucket_name)
    print('bucket', bucket)
    print('destination_blob_name', destination_blob_name)
    print('source_file_name', source_file_name)
    blob = bucket.blob(destination_blob_name)
    print('blob', blob)
    blob.upload_from_filename(source_file_name)
    print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))
    

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = __get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()
    print("File {} deleted.".format(blob_name))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS


def upload_file(files, size, with_thumbnail=True):
    """Uploads a file to the bucket."""
    
    if 'file' not in files:
        return jsonify({"error": "No file part"}), 400
    file = files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # check size
    if int(size) > IMAGE_UPLOAD_SIZE_LIMIT:
        return jsonify({"error": f'File size too large: {size}'}), 400
    
    # print the size of the file
    print(f'File size: {size}')
    # source_file_name = os.path.join(os.path.dirname(__file__), 'img', 'SocksOrNot.jpg')
    filename = os.path.join(IMAGE_UPLOAD_FOLDER, file.filename)
    file.save(filename)
    
    print(f'File name: {filename}')

    allowed_flag = allowed_file(file.filename)

    if not allowed_flag:
        return jsonify({"error": "File type not allowed"}), 400
    
    # save to thumbnails
    if with_thumbnail:
      thumbnail = os.path.join(IMAGE_THUMB_FOLDER, 'thumb_' + file.filename)
      compress_image(filename, thumbnail)
    # Upload directly to GCS
    destination_blob_name = file.filename  # or any other name you want to give

    # Use the in-memory file
    success_flag :bool = False 
    error_message = ""
    try:
        # Here, instead of reading from a file path, you are reading the content of the file directly
        upload_blob(VISION_BUCKET_NAME, filename, destination_blob_name)
        success_flag = True
    except Exception as e:
        success_flag = False
        error_message = str(e)

    # Delete the file from the server
    os.remove(filename)

    if success_flag:
        print('uploaded successfully')
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        
        print('didnt upload successfully')
        return jsonify({"error": error_message}), 500