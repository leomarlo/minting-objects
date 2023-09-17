import { create } from 'ipfs-http-client';
import fs from 'fs';

async function main() {
  // if (process.argv.length !== 4) {
  //   console.error("Usage: node script.js <path_to_image> <name_of_ipfs_service>");
  //   process.exit(1);
  // }

  const imagePath = process.argv[2];
  const ipfs_service = process.argv[3];
  const client = create({ url: `http://${ipfs_service}:5001/api/v0` });

  const file = fs.readFileSync(imagePath);
  const { cid } = await client.add(file);
  return cid.toString();
}

main().then((cid) => {
  console.log(cid);
})
.catch(error => {
  console.error('Error occurred:', error);
});
