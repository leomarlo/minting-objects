import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BACKEND_URL } from '../../utils/global';

function ProductCreation() {
  const [productSets, setProductSets] = useState([]);
  const [selectedFile, setSelectedFile] = useState<null | any>(null);
  const [tableData, setTableData] = useState<Array<any>>([]);
  const [productName, setProductName] = useState('');
  const [productDisplayName, setProductDisplayName] = useState('');

  useEffect(() => {
    axios.get(BACKEND_URL + '/vision/listProductSets').then((response) => {
      console.log('response from product sets', response.data);
      let allSets = response.data.map((set: any) => {
        let id_key: string = Object.keys(set)[1] as string
        let id = set[id_key as string];
        console.log(id)
        return id;});
      setProductSets(allSets);
    });
  }, []);

  const handleUpload = () => {
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('product_set_id', 'veggies');  // Add other required key-values

    axios.post(BACKEND_URL +  '/vision/uploadImageAndSearchSimilarProducts', formData)
      .then((response) => {
        setTableData([...tableData, response.data]);
      });
  };

  const handleSubmit = () => {
    axios.post(BACKEND_URL + '/vision/createProductAndAddToProductSet', {
      product_id: productName,
      product_display_name: productDisplayName,
      product_set_id: 'veggies',
      // add other required data
    });
  };

  return (
    <div className="container">
      <div className="row">
        <div className="col-2"></div>
        <div className="col-8">
          <h2>Create New Object</h2>
          <hr />
          <select>
            {/* <option value="veggies">Veggies</option> */}
            {productSets.map((set: any) =>
              <option key={set} value={set} disabled={set !== 'veggies'}>
                {set}
              </option>
            )}
          </select>
          <hr />
          <input type="file" onChange={(e: any) => setSelectedFile(e.target.files[0] as any)} />
          <button onClick={handleUpload}>Upload</button>
          <table>
            {/* Table headers and rows go here */}
          </table>
          <hr />
          <input placeholder="Product Name" value={productName} onChange={(e) => setProductName(e.target.value)} />
          <input placeholder="Product Display Name" value={productDisplayName} onChange={(e) => setProductDisplayName(e.target.value)} />
          <hr />
          <button onClick={handleSubmit}>Submit</button>
        </div>
        <div className="col-2"></div>
      </div>
    </div>
  );
}

export default ProductCreation;
