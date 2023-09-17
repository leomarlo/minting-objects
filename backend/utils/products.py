from utils.path import current_environment
from config.glob import TEST_PRODUCT_IDS, DEV_PRODUCT_IDS, MAIN_PRODUCT_IDS

def __get_main_product_set_ids():
    if current_environment()== 'local' or current_environment() == 'local_without_db':
        return TEST_PRODUCT_IDS
    elif current_environment() == 'development':
        return DEV_PRODUCT_IDS
    elif current_environment() == 'production':
        return MAIN_PRODUCT_IDS
    else:
        raise Exception("Environment not found")