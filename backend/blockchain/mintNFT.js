import { ethers } from 'ethers';
import fs from 'fs';
import path from 'path';

// Load contract data from a JSON file
// filename = 'deployed.json';
// absolute file path name from root of project
// const contractData = JSON.parse(fs.readFileSync(, 'utf8'));

// Another example of resolving paths
const projectRoot = process.cwd();
const absolutePath = path.resolve(projectRoot, 'blockchain','deployed.json');
const contractData = JSON.parse(fs.readFileSync(absolutePath, 'utf8'));

async function mintNFT(cid, privateKey, endpoint, tokenName, chain) {
    // Check if arguments are provided
    if (!privateKey || !endpoint || !tokenName || !chain) {
        throw new Error('All arguments (privateKey, endpoint, tokenName, chain) are required.');
    }

    // Check if tokenName and chain are valid
    if (!contractData[tokenName] || !contractData[tokenName].address[chain]) {
        throw new Error('Invalid tokenName or chain.');
    }


    console.log('The endpoint is:', endpoint)
    // Create a provider using the endpoint
    const provider = new ethers.JsonRpcProvider(endpoint);

    // Create a wallet using the private key and connect it to the provider
    const wallet = new ethers.Wallet(privateKey, provider);

    // Extract contract ABI and address
    const contractABI = contractData[tokenName].abi;
    const contractAddress = contractData[tokenName].address[chain];

    // Create a contract instance
    const contract = new ethers.Contract(contractAddress, contractABI, wallet);

    // Mint an NFT (assuming the mint function takes an address as a parameter)
    async function mint() {
        try {
            const tx = await contract.mint(cid);
            console.log('Transaction hash:', tx.hash);
            let receipt = await tx.wait();
            console.log('NFT minted successfully!');
            return receipt
        } catch (error) {
            console.error('Error minting NFT:', error);
            return {}
        }
    }

    console.log('Minting NFT...')
    console.log('Token name:', tokenName);
    console.log('Chain:', chain);
    console.log('contract address:', contractAddress);

    // Call the mint function
    return await mint()
}

// Example usage from command line arguments
const args = process.argv.slice(2);
if (args.length !== 5) {
    console.error('Usage: node script_name.js privateKey endpoint tokenName chain cid');
    process.exit(1);
}

mintNFT(args[0], args[1], args[2], args[3], args[4]).then((cid) => {
  console.log(cid);
})
.catch(error => {
  console.error('Error occurred:', error);
});
