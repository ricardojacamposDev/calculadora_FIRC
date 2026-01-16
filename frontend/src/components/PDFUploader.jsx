import React, { useRef } from 'react';
import './PDFUploader.css';

function PDFUploader({ onFileUpload, loading }) {
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = React.useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      const file = files[0];
      if (file.type === 'application/pdf') {
        onFileUpload(file);
      } else {
        alert('Por favor, selecione um arquivo PDF válido');
      }
    }
  };

  const handleChange = (e) => {
    const files = e.target.files;
    if (files && files[0]) {
      onFileUpload(files[0]);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="uploader-container">
      <div
        className={`upload-area ${dragActive ? 'active' : ''} ${loading ? 'disabled' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleChange}
          disabled={loading}
          style={{ display: 'none' }}
        />

        <div className="upload-content">
          {loading ? (
            <>
              <div className="spinner"></div>
              <p>Processando PDF...</p>
            </>
          ) : (
            <>
              <div className="upload-icon">📄</div>
              <h2>Clique para selecionar ou arraste um PDF</h2>
              <p>Formatos aceitos: PDF</p>
              <button className="btn btn-primary" disabled={loading}>
                Selecionar PDF
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default PDFUploader;
