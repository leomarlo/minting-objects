from utils.path import current_environment

def __get_ipfs_service_name():
    if current_environment()== 'local' or current_environment() == 'local_without_db':
        return 'localhost'
    else:
        return 'ipfs'