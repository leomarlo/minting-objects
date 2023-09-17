import os
from dotenv import load_dotenv
from web3 import Web3

# Load environment variables from .env file
load_dotenv()

# Get Infura endpoint and Alice's private key from .env
INFURA_ENDPOINT = os.getenv("POLYGON_RPC_ENDPOINT")
ALICE_PRIVATE_KEY = os.getenv("ALICE_PRIVATE_KEY")

# Initialize web3 instance with Infura endpoint
w3 = Web3(Web3.HTTPProvider(INFURA_ENDPOINT))

# Create a wallet using Alice's private key
alice_wallet = w3.eth.account.from_key(ALICE_PRIVATE_KEY)

# Get the nonce for Alice's address
nonce = w3.eth.get_transaction_count(alice_wallet.address)

print(f"Nonce for address {alice_wallet.address}: {nonce}")

