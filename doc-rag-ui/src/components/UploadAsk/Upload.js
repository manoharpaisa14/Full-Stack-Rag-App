// components/Upload/Upload.js
import React, { useState } from 'react';
import API from '../../api';
import Chat from './Chat';
import 'bootstrap/dist/css/bootstrap.min.css';

const Upload = () => {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResponse(null);
    setSuccess(false);
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setSuccess(false);

    try {
      const res = await API.post('/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setResponse(res.data);
      setSuccess(true);
    } catch (err) {
      setResponse({ error: 'Upload failed' });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="container mt-5">
      <div className="card p-4 shadow-sm">
        <h3 className="mb-3">📄 Upload Document</h3>

        <div className="mb-3">
          <input type="file" className="form-control" onChange={handleFileChange} />
        </div>

        <button className="btn btn-primary" onClick={handleUpload} disabled={uploading}>
          {uploading ? 'Uploading...' : 'Upload'}
        </button>

        {uploading && <div className="mt-3 text-secondary">⏳ Uploading file, please wait...</div>}
        {success && <div className="mt-3 text-success">✅ Upload successful!</div>}

      </div>

      <Chat />
    </div>
  );
};

export default Upload;
