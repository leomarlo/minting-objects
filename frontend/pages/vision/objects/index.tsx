import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Link from 'next/link';
import { BACKEND_URL } from '../../../utils/global';

type ObjectInfo = {
  id: string;
  name: string;
  displayname: string;
  nrimages: number;
};


function Objects() {
  const [objects, setObjects] = useState<ObjectInfo[]>([]);
  const objectsPerPage = 11;

  useEffect(() => {
    // Fetch the objects. I'm assuming an array is returned.
    axios.get(BACKEND_URL +  '/vision/listProductsInProductSet').then((response) => {
      console.log('response data', response.data)
      setObjects(response.data);
    });
  }, []);


  return (
    <div className="container">
      <div className="row">
        <div className="col-2"></div>
        <div className="col-8">
          {/* Pagination */}
          {/* <div className="d-flex justify-content-between mb-2">
            <button 
              className="btn btn-secondary" 
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
            >
              Previous
            </button>

            <button 
              className="btn btn-secondary" 
              disabled={indexOfLastProduct >= objects.length}
              onClick={() => setCurrentPage((prev) => (indexOfLastProduct >= objects.length ? prev : prev + 1))}
            >
              Next
            </button>
          </div> */}

          <div className="mt-4" >
            <table className="table table-dark">
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Object</th>
                  <th scope="col">Description</th>
                  <th scope="col">Creation Time</th>
                  <th scope="col">Minted</th>
                </tr>
              </thead>
              <tbody>
                {objects.map((object, index) => (
                  <tr key={object.id}>
                    <th scope="row">{index + 1}</th>
                    <td>
                        <a href={`/vision/objects/${object.id}`}>{object.id}</a>
                    </td>
                    <td>{object.displayname}</td>
                    <td>Some time</td>
                    <td>dunno</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        <div className="col-2"></div>
      </div>
    </div>
  );
}

export default Objects;
