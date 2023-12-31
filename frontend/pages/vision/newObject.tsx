import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { BACKEND_URL } from '../../utils/global';
import { SIMILARITY_THRESHOLD } from '../../utils/constants';
import { MIN_UPLOADS_PER_OBJECT, PRODUCT_IDS } from '../../utils/global'
import getLastWordOfPath from '../../utils/parsing';
import LoadingSpinner from "../../components/LoadingSpinner"
// import TablePrimitive  from "../../components/table"
import FileUploadComponent from "../../components/fileUpload"
import createObjectWithReferenceImages from "../../utils/createObjectWithRefImages"
// import Web3ModalComponent from "../../components/web3connect"
import { useWeb3Modal } from '../../contexts/web3Context';
import ControlledCheckbox from "../../components/checkBox";
import PasswordInput from "../../components/passwordInput"

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
  const [selectedObjectSet, setSelectedObjectSet] = useState(PRODUCT_IDS[0]);
  const [useCustodialWallet, setUseCustodialWallet] = useState(false);
  const toggleWeb3Modal = (checked: boolean) => {
    setUseCustodialWallet(checked);
  };
  const [custodialPassword, setCustodialPassword] = useState<string>("");

  const fileInputRef = useRef<HTMLInputElement | null>(null);


  const { web3, connect, disconnect , account} = useWeb3Modal();

  const handleDeleteSelectedFile = () => {
      setSelectedFile(null);
      if (fileInputRef.current) {
          fileInputRef.current.value = '';
      }
  };

  const handleSelectChange = (event: any) => {
    console.log('selected object set is', event.target.value)
    setSelectedObjectSet(event.target.value);
  };


  useEffect(() => {

    const aboveThreshold = tableData.some(item => item.score > SIMILARITY_THRESHOLD);
    setUpLoadDisabled(aboveThreshold || selectedFile===null);
  }, [tableData, selectedFile]);


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
    console.log('selected Object Set is', selectedObjectSet)
    const formData = new FormData();
    if (selectedFile){
      formData.append('file', selectedFile);
      formData.append('product_set_id', selectedObjectSet);  // Add other required key-values
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

  const checkPasswordFormat = (pw: string) => {
    if (pw.length>0) {
      return true
    }
    return false
  }


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
    createObjectWithReferenceImages(validFiles, selectedObjectSet, objectDisplayName, objectName)
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
            <h2>Mint new Object</h2>
            <hr />
            <select 
              className="form-control" 
              value={selectedObjectSet} 
              onChange={handleSelectChange}
              defaultValue={PRODUCT_IDS[0]}
              style={{
                backgroundColor: '#e4ea90',
                borderWidth: '2px',
                borderRadius: '4px',
                padding: '8px 12px',
                appearance: 'none',  // Remove default appearance
                backgroundImage: 'url("data:image/svg+xml;utf8,<svg fill=\'%23000\' viewBox=\'0 0 24 24\' width=\'24\' height=\'24\' xmlns=\'http://www.w3.org/2000/svg\'><path d=\'M7 10l5 5 5-5z\'/></svg>")',
                backgroundRepeat: 'no-repeat',
                backgroundPosition: 'right 8px center',
                backgroundSize: '16px 16px'
              }}>
              {objectSets.map((set: any) =>
                <option key={set} value={set} disabled={!PRODUCT_IDS.includes(set)}>
                  {set}
                </option>
              )}
            </select>
            <hr />
            <h4>Upload Reference Images</h4>
            <div className="row mt-3">
              <div className="col-4">
                <button className="btn btn-success w-100" onClick={handleUpload}>Check</button>
              </div>
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
            <button className='btn btn-success mb-4 w-100' onClick={handleAddObject} disabled={upLoadDisabled}>Add</button>
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
            <h4>Object Information</h4>
            <div className="row mt-3">
              <div className="col-6">
                <input className="mx-2 my-2 w-100" placeholder="Object Name" value={objectName} onChange={(e) => setObjectName(e.target.value)} />
              </div>
              <div className="col-6">
                <input className="mx-2 my-2 w-100" placeholder="Object Display Name" value={objectDisplayName} onChange={(e) => setObjectDisplayName(e.target.value)} />
              </div>
            </div>
            <hr />
            <ControlledCheckbox isChecked={useCustodialWallet} onChange={toggleWeb3Modal} /> Use custodial wallet.
            {/* <br />
            <Web3ModalComponent /> */}
            <br />
            {submitInfo + (account ? ` Connected to ${account}.` : "")}
            <br />
            {useCustodialWallet ? 
              <div>
                <button className='btn btn-success w-100' onClick={(e)=>{
                  if (checkPasswordFormat(custodialPassword)) {
                    handleSubmit()
                  } else {
                    throw "Password invalid"
                  }
                }}>Mint object to custodial wallet</button>
                <br />
                <PasswordInput 
                  classNames="" 
                  password={custodialPassword} 
                  setPassword={setCustodialPassword} />
                
              </div> :
              <button 
                className='btn btn-success w-100' 
                onClick={(e)=> {
                  connect();
                  // handleSubmit()
                }}
                >Mint object to my wallet</button> 
            }
            
            
            {/* <button className="btn btn-primary w-100" onClick={handleSubmit}disabled={disableSubmit}>Mint Object</button> */}
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
