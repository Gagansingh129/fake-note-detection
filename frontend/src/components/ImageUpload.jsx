import React, { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, X, AlertTriangle, ArrowRight, Loader2, Info } from 'lucide-react';

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
    <div style={{ width: '100%' }}>
      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp"
        style={{ display: 'none' }}
        onChange={(e) => handleFiles(e.target.files[0])}
      />

      {!previewUrl ? (
        <div>
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => inputRef.current?.click()}
            style={{
              border: `2px dashed ${dragActive ? '#2563eb' : '#cbd5e1'}`,
              borderRadius: '1.25rem',
              padding: '4.5rem 2rem',
              textAlign: 'center',
              cursor: 'pointer',
              background: dragActive ? '#f0fdf4' : '#ffffff',
              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.02)',
              transition: 'all 0.2s ease',
            }}
          >
            {/* Cloud Icon in Blue Circle */}
            <div
              style={{
                width: '64px',
                height: '64px',
                borderRadius: '9999px',
                background: '#eff6ff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 1.25rem',
              }}
            >
              <UploadCloud size={32} color="#2563eb" />
            </div>

            <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#0f172a', marginBottom: '0.4rem' }}>
              Upload currency note image
            </h3>
            <p style={{ color: '#64748b', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
              Drag and drop your note photo here, or click to browse
            </p>

            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                inputRef.current?.click();
              }}
              style={{
                background: '#0f172a',
                color: '#ffffff',
                border: 'none',
                padding: '0.7rem 1.6rem',
                borderRadius: '0.5rem',
                fontSize: '0.9rem',
                fontWeight: 600,
                cursor: 'pointer',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                transition: 'all 0.15s',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = '#1e293b')}
              onMouseLeave={(e) => (e.currentTarget.style.background = '#0f172a')}
            >
              Choose image
            </button>

            <p style={{ color: '#94a3b8', fontSize: '0.78rem', marginTop: '1.25rem' }}>
              JPG, PNG or WEBP · up to 10 MB
            </p>
          </div>

          {/* Info note below dropzone */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.45rem',
              color: '#64748b',
              fontSize: '0.84rem',
              marginTop: '1rem',
            }}
          >
            <Info size={16} color="#3b82f6" />
            <span>Crop closely around the note's edges for the most reliable result.</span>
          </div>
        </div>
      ) : (
        /* Preview Card */
        <div
          style={{
            background: '#ffffff',
            borderRadius: '1.25rem',
            border: '1px solid #e2e8f0',
            padding: '1.5rem',
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <ImageIcon size={18} color="#2563eb" />
              <span style={{ fontSize: '0.9rem', fontWeight: 600, color: '#0f172a' }}>
                {selectedFile?.name}
              </span>
              <span style={{ fontSize: '0.78rem', color: '#64748b' }}>
                ({(selectedFile?.size / (1024 * 1024)).toFixed(2)} MB)
              </span>
            </div>

            <button
              onClick={clearSelection}
              disabled={isLoading}
              style={{
                background: '#f1f5f9',
                border: 'none',
                borderRadius: '9999px',
                width: '30px',
                height: '30px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                color: '#64748b',
              }}
            >
              <X size={16} />
            </button>
          </div>

          <div
            style={{
              width: '100%',
              height: '320px',
              borderRadius: '0.75rem',
              overflow: 'hidden',
              background: '#0f172a',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '1.25rem',
              border: '1px solid #cbd5e1',
            }}
          >
            <img
              src={previewUrl}
              alt="Banknote Preview"
              style={{
                maxWidth: '100%',
                maxHeight: '100%',
                objectFit: 'contain',
              }}
            />
          </div>

          <button
            onClick={handleSubmit}
            disabled={isLoading}
            style={{
              width: '100%',
              padding: '0.85rem',
              borderRadius: '0.625rem',
              background: '#0f172a',
              color: '#ffffff',
              border: 'none',
              fontWeight: 700,
              fontSize: '0.95rem',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem',
              boxShadow: '0 4px 6px -1px rgba(15, 23, 42, 0.2)',
            }}
          >
            {isLoading ? (
              <>
                <Loader2 size={18} className="spin" />
                <span>Screening Banknote...</span>
              </>
            ) : (
              <>
                <span>Run NoteGuard AI Screening</span>
                <ArrowRight size={18} />
              </>
            )}
          </button>
        </div>
      )}

      {error && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.75rem 1rem',
            borderRadius: '0.5rem',
            background: '#fef2f2',
            border: '1px solid #fecaca',
            color: '#dc2626',
            fontSize: '0.85rem',
            marginTop: '1rem',
          }}
        >
          <AlertTriangle size={18} />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}
