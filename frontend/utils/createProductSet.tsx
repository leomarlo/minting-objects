// Date: 09/07/21
import React from 'react';

const createProductSet = () => {
    const url = '/vision/createProductSet';
    const data = {
      product_set_id: 'your_product_set_id',
      product_set_display_name: 'your_display_name'
    };
  
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      console.log(data); // Do something with the response data
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }
  

export default createProductSet;