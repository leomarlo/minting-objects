import fs from 'fs'
import * as IPFS from 'ipfs-core'
const ipfs = await IPFS.create()
// Check for command-line arguments
const runEnvironment = process.argv[2]; // 'docker' or 'host'

let ipfsHost = 'localhost'; // Default to host

if (runEnvironment === 'docker') {
    ipfsHost = 'ipfs'; // Use the service name as defined in docker-compose or the container name
}

// const client = ipfsClient({ host: ipfsHost, port: '5001', protocol: 'http' });

async function uploadFile() {
    try {
        const file = fs.readFileSync('../img/carrot1.jpg');
        const addedFile = await ipfs.add({ content: file });
        const fileUrl = `https://ipfs.io/ipfs/${addedFile.path}`;
        console.log(fileUrl);
    } catch (error) {
        console.error('Error uploading file:', error);
    }
}

uploadFile();
