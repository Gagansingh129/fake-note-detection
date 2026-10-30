import React, { useState } from 'react';
import { UploadCloud, Camera, AlertCircle } from 'lucide-react';
import ImageUpload from '../components/ImageUpload';
import CameraCapture from '../components/CameraCapture';
import PredictionResult from '../components/PredictionResult';
import { api } from '../services/api';

export default function Analyze({ initialMode = 'upload' }) {
  const [activeTab, setActiveTab] = useState(initialMode);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyzeImage = async (file) => {
    setResult(null);
    setIsLoading(true);
    setError(null);
    try {
      const data = await api.predictImage(file);
      setResult(data);
    } catch (err) {
      console.error('[Upload Screening Error]:', err);
      setError(err.message || 'An error occurred while analyzing the banknote image.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnalyzeCamera = async (base64Image) => {
    setResult(null);
    setIsLoading(true);
    setError(null);
    try {
      const data = await api.predictCamera(base64Image);
      setResult(data);
    } catch (err) {
      console.error('[Camera Screening Error]:', err);
      setError(err.message || 'An error occurred while analyzing the camera snapshot.');
    } finally {
      setIsLoading(false);
    }
  };

  const resetAnalysis = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div>
      {!result ? (
        <div>
          {/* Header */}
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <h2 style={{ fontSize: '1.85rem', fontWeight: 800 }}>Currency Authenticity Screening</h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', marginTop: '0.4rem' }}>
              Choose whether to upload an image or scan live using your device's camera.
            </p>

            {/* Mode Switcher Tabs */}
            <div
              style={{
                display: 'inline-flex',
                background: 'rgba(0, 0, 0, 0.4)',
                borderRadius: '0.75rem',
                padding: '0.3rem',
                border: '1px solid var(--border-color)',
                marginTop: '1.25rem',
              }}
            >
              <button
                className={`btn ${activeTab === 'upload' ? 'btn-primary' : 'btn-secondary'}`}
                style={{ padding: '0.5rem 1.25rem', fontSize: '0.9rem' }}
                onClick={() => {
                  setActiveTab('upload');
                  setError(null);
                }}
              >
                <UploadCloud size={16} /> Upload Image
              </button>
              <button
                className={`btn ${activeTab === 'camera' ? 'btn-primary' : 'btn-secondary'}`}
                style={{ padding: '0.5rem 1.25rem', fontSize: '0.9rem' }}
                onClick={() => {
                  setActiveTab('camera');
                  setError(null);
                }}
              >
                <Camera size={16} /> Use Camera
              </button>
            </div>
          </div>

          {/* Active Input Mode Component */}
          {activeTab === 'upload' ? (
            <ImageUpload onAnalyze={handleAnalyzeImage} isLoading={isLoading} />
          ) : (
            <CameraCapture onAnalyze={handleAnalyzeCamera} isLoading={isLoading} />
          )}

          {/* Global Error Banner */}
          {error && (
            <div
              style={{
                maxWidth: '640px',
                margin: '1.5rem auto 0',
                padding: '1rem',
                borderRadius: '0.75rem',
                background: 'rgba(239, 68, 68, 0.12)',
                border: '1px solid rgba(239, 68, 68, 0.3)',
                color: '#f87171',
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                fontSize: '0.9rem',
              }}
            >
              <AlertCircle size={20} style={{ flexShrink: 0 }} />
              <div>{error}</div>
            </div>
          )}
        </div>
      ) : (
        <PredictionResult result={result} onReset={resetAnalysis} />
      )}
    </div>
  );
}
