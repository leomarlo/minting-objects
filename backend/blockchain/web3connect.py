import os, json
from dotenv import load_dotenv
from web3 import Web3
from config.glob import (
    PRODUCTION_CHAIN, 
    TEST_CHAIN, 
    PRODUCTION_MAX_GAS, 
    TEST_MAX_GAS)
from utils.path import current_environment
from web3.middleware import geth_poa_middleware

# Load environment variables from .env file
load_dotenv()

# Get Infura endpoint and Alice's private key from .env

ALICE_PRIVATE_KEY = os.getenv("ALICE_PRIVATE_KEY")


def get_rpc_endpoint():
    chain = get_chain()
    if chain=='polygon':
        return os.getenv("POLYGON_RPC_ENDPOINT")
    elif chain=='goerli':
        return os.getenv("GOERLI_RPC_ENDPOINT")

def current_chain_is_poa():
    if (get_chain()=="goerli"):
        return True
    return False
  

def get_w3_object():
    # Initialize web3 instance with Infura endpoint
    w3 = Web3(Web3.HTTPProvider(get_rpc_endpoint()))
    if current_chain_is_poa():
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def get_contract_from_json(file_path, contract_name):
    with open(file_path, 'r') as f:
        contract_abi = json.load(f)

    chain = get_chain()
    return get_contract(
        contract_address=contract_abi[contract_name]["address"][chain],
        contract_abi=contract_abi[contract_name]["abi"])

def get_contract(contract_address, contract_abi):
    print('before getting contract')
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    print('after getting contract')
    return contract


def get_chain():
    if current_environment()=="production":
        return PRODUCTION_CHAIN
    else:
        return TEST_CHAIN
    
def get_max_gas():
    if current_environment()=="production":
        return PRODUCTION_MAX_GAS
    else:
        return TEST_MAX_GAS
    

w3 = get_w3_object()
# Create a wallet using Alice's private key
wallet = w3.eth.account.from_key(ALICE_PRIVATE_KEY)

myaddress = wallet.address


print('WE are getting the following chain', get_chain())
print('We have the following endpoint', )