import json, os
import subprocess
from blockchain.web3utils import get_chain, get_rpc_endpoint
# from blockchain.web3connect import (w3, wallet, ALICE_PRIVATE_KEY, myaddress, get_contract_from_json, get_max_gas)



# def mint_nft_primitive(cid, contract_name="BLOOD"):
#     # Ensure you're connected to Ethereum
#     # if not w3.isConnected():
#     #     print("Error: Unable to connect to Ethereum node.")
#     #     exit()
#     # get abspath of os.path.join of current directory and "deployed.json"
#     file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "deployed.json"))

#     # return file_path
#     contract = get_contract_from_json(file_path=file_path, contract_name=contract_name)
#     # gas_estimate = contract.functions.mint(cid).estimateGas({'from': myaddress})
#     # if gas_estimate < get_max_gas():
#     #     print(f"Gas estimate to transact with mint: {gas_estimate}")
#     # else:
#     #     print("Gas cost exceeds 1M, not making transaction")

#     # Constructing raw transaction
#     transaction = contract.functions.mint(cid).build_transaction()
#     transaction.update({'nonce': w3.eth.get_transaction_count(myaddress)})
#     # {
#     #     'chainId': 137,  # Mainnet
#     #     'gasPrice': w3.toWei('20', 'gwei'),
#     #     'nonce': w3.eth.getTransactionCount(myaddress),
#     # }

#     # Sign the transaction using the wallet object
#     signed_tx = w3.eth.account.sign_transaction(transaction, ALICE_PRIVATE_KEY)

#     return {'signed_tx': signed_tx}

#     # Send the transaction
#     tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
#     print(f"Transaction hash: {tx_hash.hex()}")

#     # Wait for the transaction to be mined
#     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     print(f"Transaction receipt: {receipt}")

#     return {'tx': tx_hash, 'receipt': receipt}


def mint_nft(cid, contract_name="BLOOD"):
    
    pkAlice = os.getenv("ALICE_PRIVATE_KEY")
    minting_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'blockchain','mintNFT.js'))
    result = subprocess.run(
          [
              'node', 
              minting_path, 
              pkAlice, 
              get_rpc_endpoint(),
              contract_name,
              get_chain(),
              cid
        ], capture_output=True, text=True, check=True)
    print(result.stdout)



def mint_token(address, cid, product_id):
    if address==None:
        ## create a new address
        a = 1
    tx = ''
    address = ''
    return tx, address