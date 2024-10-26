// frontend/src/FileUpload.js
import React from 'react';

function FileUpload({ onUpload }) {
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      onUpload(file);
    }
  };

  return (
    <div>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
    </div>
  );
}

export default FileUpload;
