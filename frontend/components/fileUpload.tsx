import React from 'react';

interface Props {
    selectedFile: File | null;
    setSelectedFile: React.Dispatch<React.SetStateAction<File | null>>;
    fileInputRef: React.RefObject<HTMLInputElement>;
}

const FileUploadComponent: React.FC<Props> = ({ selectedFile, setSelectedFile, fileInputRef }) => {

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            setSelectedFile(e.target.files[0]);
        }
    };

    return (
        <div>
            <label className="btn btn-primary w-100">
                Choose File
                <input 
                    type="file"
                    ref={fileInputRef}
                    style={{ display: 'none' }}
                    onChange={handleFileChange} 
                />
            </label>
        </div>
    );
}

export default FileUploadComponent;
