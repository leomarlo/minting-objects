import os, json
from config.glob import (
    PRODUCTION_CHAIN, 
    TEST_CHAIN)
from utils.path import current_environment



def get_chain():
    if current_environment()=="production":
        return PRODUCTION_CHAIN   ## this is usually polygon
    else:
        return TEST_CHAIN  ## this is usually goerli
    

def get_rpc_endpoint():
    chain = get_chain()
    if chain=='polygon':
        return os.getenv("POLYGON_RPC_ENDPOINT")
    elif chain=='goerli':
        return os.getenv("GOERLI_RPC_ENDPOINT")
    else:
        raise Exception("Chain not found")