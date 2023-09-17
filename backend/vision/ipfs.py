import subprocess, os, sys
from flask import jsonify
from utils.ipfs import __get_ipfs_service_name
from utils.logging import log

def upload_image_to_ipfs(image_path):
    try:
        # create a path using os.path.join and abspath to the uploadToIPFS.js script
        ipfs_service_name = __get_ipfs_service_name() # 'localhost' or 'ipfs'

        upload_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'blockchain','ipfsConnect.js'))
        result = subprocess.run(['node', upload_path, image_path, ipfs_service_name], capture_output=True, text=True, check=True)

        # Print the output
        print(result.stdout)

        # If you want to store the output in a variable:
        cid = result.stdout.strip()  # Using strip() to remove any trailing newlines or spaces

        gateway_url = f"http://{ipfs_service_name}:8080/ipfs/{cid}"
        print('gateway url',gateway_url)
        return jsonify({'gateway_url':gateway_url, 'cid':cid}), 200
    except subprocess.CalledProcessError as e:
        errormessage = f"Error uploading to IPFS: {e}"
        log(errormessage)
        return jsonify({"message": errormessage}), 500
