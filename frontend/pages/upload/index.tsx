import React, { useState } from 'react';
import axios from 'axios';
import { BACKEND_URL } from '../../utils/global';

function Upload() {
    const [file, setFile] = useState(null);

    const onFileChange = (e: any) => {
        setFile(e.target.files[0]);
    }

    const onUpload = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(BACKEND_URL + 'upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            console.log(response.data);
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    }

    return (
        <div>
            <input type="file" onChange={onFileChange} />
            <button onClick={onUpload}>Upload</button>
        </div>
    );
}

export default Upload;
