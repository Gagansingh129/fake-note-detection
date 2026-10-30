import React, { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, X, AlertTriangle, ArrowRight, Loader2 } from 'lucide-react';

export default function ImageUpload({ onAnalyze, isLoading }) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  const handleFiles = (file) => {
    setError(null);
    if (!file) return;

    // Validate type
    const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      setError('Please upload a valid JPG, PNG, or WEBP image.');
      return;
    }

    // Validate size (10 MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('Image file exceeds the 10 MB limit.');
      return;
    }

    setSelectedFile(file);
    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);
  };

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
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files[0]);
    }
  };

  const clearSelection = () => {
    setSelectedFile(null);
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    setError(null);
    if (inputRef.current) inputRef.current.value = '';
  };

  const handleSubmit = () => {
    if (selectedFile && !isLoading) {
      onAnalyze(selectedFile);
    }
  };

  return (
    <div className="glass-card" style={{ maxWidth: '640px', margin: '0 auto' }}>
      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp"
        style={{ display: 'none' }}
        onChange={(e) => handleFiles(e.target.files[0])}
      />

      {!previewUrl ? (
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          style={{
            border: `2px dashed ${dragActive ? 'var(--accent-blue)' : 'var(--border-color)'}`,
            borderRadius: '0.75rem',
            padding: '3rem 1.5rem',
            textAlign: 'center',
            cursor: 'pointer',
            background: dragActive ? 'rgba(59, 130, 246, 0.05)' : 'rgba(0, 0, 0, 0.2)',
            transition: 'all 0.2s ease',
          }}
        >
          <UploadCloud size={44} color="#60a5fa" style={{ margin: '0 auto 1rem' }} />
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Upload Currency Note Image</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.4rem' }}>
            Drag and drop your note photo here, or click to browse
          </p>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.75rem', marginTop: '0.75rem' }}>
            Supports JPG, PNG, WEBP (Up to 10 MB)
          </p>
        </div>
      ) : (
        <div>
          <div style={{ position: 'relative', borderRadius: '0.75rem', overflow: 'hidden', background: '#000' }}>
            <img
              src={previewUrl}
              alt="Currency note preview"
              style={{ width: '100%', maxHeight: '340px', objectFit: 'contain', display: 'block' }}
            />
            <button
              onClick={clearSelection}
              disabled={isLoading}
              style={{
                position: 'absolute',
                top: '0.75rem',
                right: '0.75rem',
                background: 'rgba(0, 0, 0, 0.65)',
                color: '#fff',
                border: 'none',
                borderRadius: '9999px',
                width: '32px',
                height: '32px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
              }}
            >
              <X size={18} />
            </button>
          </div>

          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginTop: '1rem',
              fontSize: '0.85rem',
              color: 'var(--text-secondary)',
            }}
          >
            <span>{selectedFile?.name}</span>
            <span>{(selectedFile?.size / (1024 * 1024)).toFixed(2)} MB</span>
          </div>

          <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1.25rem' }}>
            <button className="btn btn-secondary" onClick={clearSelection} disabled={isLoading} style={{ flex: 1 }}>
              Choose Different
            </button>
            <button className="btn btn-primary" onClick={handleSubmit} disabled={isLoading} style={{ flex: 2 }}>
              {isLoading ? (
                <>
                  <Loader2 size={18} className="pulse" /> Screening Note...
                </>
              ) : (
                <>
                  Analyze Note Authenticity <ArrowRight size={18} />
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {error && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            marginTop: '1rem',
            padding: '0.75rem',
            borderRadius: '0.5rem',
            background: 'rgba(239, 68, 68, 0.1)',
            color: '#f87171',
            fontSize: '0.85rem',
          }}
        >
          <AlertTriangle size={16} /> {error}
        </div>
      )}
    </div>
  );
}
