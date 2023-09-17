from utils.path import current_environment
from config.glob import TEST_PRODUCT_ID, DEV_PRODUCT_ID, MAIN_PRODUCT_ID

def __get_main_product_set_id():
    if current_environment()== 'local' or current_environment() == 'local_without_db':
        return TEST_PRODUCT_ID
    elif current_environment() == 'development':
        return DEV_PRODUCT_ID
    elif current_environment() == 'production':
        return MAIN_PRODUCT_ID
    else:
        raise Exception("Environment not found")