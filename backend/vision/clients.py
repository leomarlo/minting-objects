import os
from google.cloud import vision_v1p3beta1 as gvision
from google.cloud import storage
from google.oauth2 import service_account

def __get_vision_client():
    credentials_path = os.getenv("GOOGLE_CREDENTIAL_PATH")
    if not credentials_path:
        raise Exception("GOOGLE_CREDENTIAL_PATH not found in environment variables")
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    # creds = Credentials.from_service_account_file(credentials_path)
    return gvision.ProductSearchClient(credentials=credentials)

def __get_storage_client():
    credentials_path = os.getenv("GOOGLE_CREDENTIAL_PATH")
    if not credentials_path:
        raise Exception("GOOGLE_CREDENTIAL_PATH not found in environment variables")
    return storage.Client.from_service_account_json(credentials_path)