import subprocess

def upload_image_to_ipfs(image_path):
    try:
        
        result = subprocess.run(['node', 'uploadToIPFS.js', image_path], capture_output=True, text=True, check=True)
        cid = result.stdout.strip()
        gateway_url = f"http://ipfs:8080/ipfs/{cid}"
        return gateway_url
    except subprocess.CalledProcessError as e:
        print(f"Error uploading to IPFS: {e}")
        return None

# Test the function
if __name__ == "__main__":
    image_path = '../img/carrot1.jpg'
    url = upload_image_to_ipfs(image_path)
    if url:
        print(f"Image uploaded to IPFS and accessible at: {url}")
