import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { BACKEND_URL } from '../../utils/global';
import { SIMILARITY_THRESHOLD } from '../../utils/constants';
import { MIN_UPLOADS_PER_OBJECT, PRODUCT_ID } from '../../utils/global'
import getLastWordOfPath from '../../utils/parsing';
import LoadingSpinner from "../../components/LoadingSpinner"
// import TablePrimitive  from "../../components/table"
import FileUploadComponent from "../../components/fileUpload"
import createObjectWithReferenceImages from "../../utils/createObjectWithRefImages"


function ObjectCreation() {
  const [objectSets, setObjectSets] = useState([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [tableData, setTableData] = useState<Array<any>>([]);
  const [objectName, setObjectName] = useState('');
  const [objectDisplayName, setObjectDisplayName] = useState('');
  const [uploadInfo, setUploadInfo] = useState('Info: Please upload an image file');
  const [submitInfo, setSubmitInfo] = useState(`You need at least ${MIN_UPLOADS_PER_OBJECT} images to submit a new object.`);
  const [isLoading, setIsLoading] = useState(false); // new state
  const [isMinting, setIsMinting] = useState(false); // new state
  const [upLoadDisabled, setUpLoadDisabled] = useState(true)
  const [disableSubmit, setDisableSubmit] = useState(true)
  const [validFiles, setValidFiles] = useState<Array<string>>([])

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleDeleteSelectedFile = () => {
      setSelectedFile(null);
      if (fileInputRef.current) {
          fileInputRef.current.value = '';
      }
  };


  useEffect(() => {

    const aboveThreshold = tableData.some(item => item.score > SIMILARITY_THRESHOLD);
    setUpLoadDisabled(aboveThreshold);
  }, [tableData]);


  useEffect(() => {

    const condition1 = validFiles.length>=MIN_UPLOADS_PER_OBJECT
    const condition2 = objectName.length>0 && objectDisplayName.length >0
    if (condition1 && condition2){
      setDisableSubmit(false)
    } else {
      setDisableSubmit(true)
    }
  }, [validFiles, objectName, objectDisplayName]);


  useEffect(() => {
    axios.get(BACKEND_URL + '/vision/listProductSets').then((response) => {
      console.log('response from product sets', response.data);
      let allSets = response.data.map((set: any) => {
        let id_key: string = Object.keys(set)[1] as string
        let id = set[id_key as string];
        console.log(id)
        return id;});
      setObjectSets(allSets);
    });
  }, []);

  const handleUpload = () => {
    setIsLoading(true)
    const formData = new FormData();
    if (selectedFile){
      formData.append('file', selectedFile);
      formData.append('product_set_id', PRODUCT_ID);  // Add other required key-values
    }
      

    axios.post(BACKEND_URL +  '/vision/uploadImageAndSearchSimilarProducts', formData)
      .then((response) => {
        let temp_resp = response.data.map((item: any) => {
          return {name: getLastWordOfPath(item["name"]), score: item["score"]}
        })
        const aboveThreshold = temp_resp.some((item: any) => item.score > SIMILARITY_THRESHOLD);
        let furtherInfo = aboveThreshold ? `, but it appears that one of the existing objects is very similar, i.e. it has more than ${SIMILARITY_THRESHOLD*100}% agreement according to the algorithm. (The "Add" button has therefore been disabled)` : '. None of the existing objects are very similar.'
        setUploadInfo('Info: successful upload' + furtherInfo)
        setTableData([...tableData, ...temp_resp]); 
      })
      .catch((error) => {
        setUploadInfo('Info: upload failed')
        console.log(error);
      })
      .finally(() => {
        setIsLoading(false); // stop loading whether request is successful or failed
      });
  };


  const handleAddObject = () => {
    // set the uploaded file as valid
    if (selectedFile) {
      setValidFiles([...validFiles, selectedFile.name]);
    }
    // erase the selected file
    handleDeleteSelectedFile();
    // reset the table
    setTableData([]);

  }
  
  const handleSubmit = () => {
    setIsMinting(true)
    console.log('the submitted files are', validFiles)

    createObjectWithReferenceImages(validFiles, PRODUCT_ID, objectDisplayName, objectName)
    .then(data => {
      // Do something with the data
      console.log(data)
      setSubmitInfo('You submitted successfully')
      setValidFiles([])
      // alert with jsonized data 
      alert(JSON.stringify(data))
    })
    .catch(error => {
      // Handle the error
      console.log(error)
      setSubmitInfo('Submission was unsuccessful.')
    }).finally(() => {
      setIsMinting(false)
    })
  }




  return (
    <div className="container">
      <div className="row">
        <div className="col-2"></div>
        <div className="col-8">
          <div className="mt-4">
            <h2>Create New Object</h2>
            <hr />
            <select>
              {objectSets.map((set: any) =>
                <option key={set} value={set} disabled={set !== PRODUCT_ID}>
                  {set}
                </option>
              )}
            </select>
            <hr />
            <h4>Upload Reference Images</h4>
            <div className="row mt-3">
              <div className="col-4">
              <FileUploadComponent 
                  selectedFile={selectedFile} 
                  setSelectedFile={setSelectedFile}
                  fileInputRef={fileInputRef} 
              />
              </div>
              <div className="col-4">
              {selectedFile && (
                  <div className="mt-3">
                      <span className="mr-3">{selectedFile.name}</span>
                  </div>
              )}
              </div>
              <div className="col-4">
              <button className="btn btn-success w-100" onClick={handleUpload}>Check</button></div>
            </div>
            <br />
            {isLoading && <LoadingSpinner />}
            <br />
            {uploadInfo}
            <br />
            {tableData.length > 0 &&
            <table className="table table-dark">
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Name</th>
                  <th scope="col">Score</th>
                </tr>
              </thead>
              <tbody>
              {tableData.map((td, index) => {
                  // console.log('inside table row creation!');
                  // console.log(td);
                  return (
                      <tr key={index}>
                          <th scope="row">{index + 1}</th> {/* This will always be 1, you might want to replace it with `index + 1` or some other unique identifier */}
                          <td>{td["name"]}</td>
                          <td>{td["score"]}</td>
                      </tr>
                  );
              })}
              </tbody>
            </table>}
            <button className='btn btn-success mb-4' onClick={handleAddObject} disabled={upLoadDisabled}>Add</button>
            <table className="table table-dark">
              <thead>
                <tr>
                  <th scope='col'>#</th>
                  <th scope='col'>File</th>
                </tr>
              </thead>
              <tbody>
                {validFiles.map((fl, index)=>{
                  return (
                    <tr>
                      <th scope='row'>{index+1}</th>
                      <td>{fl}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>

            <hr />
            <input className="mx-2" placeholder="Object Name" value={objectName} onChange={(e) => setObjectName(e.target.value)} />
            <input className="mx-2" placeholder="Object Display Name" value={objectDisplayName} onChange={(e) => setObjectDisplayName(e.target.value)} />
            <hr />
            {submitInfo}
            <br />
            <button className="btn btn-primary w-100" onClick={handleSubmit}disabled={disableSubmit}>Mint Object</button>
            <br />
            {isMinting && <LoadingSpinner />}
          </div>
        </div>
        <div className="col-2"></div>
      </div>
    </div>
  );
}

export default ObjectCreation;
