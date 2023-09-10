import os
from google.cloud import storage
my_password = os.getenv("Password")
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv("GOOGLE_CREDENTIAL_PATH")

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))
    

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()
    print("File {} deleted.".format(blob_name))