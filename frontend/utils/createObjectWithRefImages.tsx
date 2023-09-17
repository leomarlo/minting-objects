import axios from 'axios';
import { BACKEND_URL } from './global';

const createObjectWithReferenceImages = (
  files: string[], 
  product_set_id: string, 
  product_display_name: string, 
  product_id: string
) => {

  return axios.post(`${BACKEND_URL}vision/createProductAndReferenceImages`, {
    files,
    product_set_id,
    product_display_name,
    product_id,
  })
  .then(response => {
    // Handle the response as needed
    console.log(response.data);
    return response.data;
  })
  .catch(error => {
    console.error("Error making the request:", error);
    throw error;
  });
}

export default createObjectWithReferenceImages;
