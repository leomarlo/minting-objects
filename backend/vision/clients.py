import os
from google.cloud import vision_v1p3beta1 as gvision
from google.cloud import storage
from google.oauth2 import service_account


def __get_credentials():
    credentials_path = os.getenv("GOOGLE_CREDENTIAL_PATH")
    if not credentials_path:
        raise Exception("GOOGLE_CREDENTIAL_PATH not found in environment variables")
    return service_account.Credentials.from_service_account_file(credentials_path)


def __get_vision_client():
    credentials = __get_credentials()
    return gvision.ProductSearchClient(credentials=credentials)


def __get_storage_client():
    credentials_path = os.getenv("GOOGLE_CREDENTIAL_PATH")
    if not credentials_path:
        raise Exception("GOOGLE_CREDENTIAL_PATH not found in environment variables")
    return storage.Client.from_service_account_json(credentials_path)


def __get_annotator_client():
    credentials = __get_credentials()
    return gvision.ImageAnnotatorClient(credentials=credentials)