import React, { useState } from 'react';
import { UploadCloud, Camera, Check, AlertTriangle } from 'lucide-react';
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
    <div style={{ padding: '2rem 2.5rem', maxWidth: '1240px', margin: '0 auto' }}>
      {!result ? (
        <div>
          {/* Header Bar with Title and Right Mode Toggle Tabs */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              flexWrap: 'wrap',
              gap: '1rem',
              marginBottom: '2rem',
            }}
          >
            <div>
              <h2 style={{ fontSize: '1.85rem', fontWeight: 900, color: '#0f172a', letterSpacing: '-0.02em', margin: 0 }}>
                Analyze a note
              </h2>
              <p style={{ color: '#64748b', fontSize: '0.92rem', marginTop: '0.35rem', margin: 0 }}>
                Upload a photo or scan live with your device camera.
              </p>
            </div>

            {/* Top Right Toggle Tabs */}
            <div
              style={{
                display: 'inline-flex',
                background: '#ffffff',
                border: '1px solid #cbd5e1',
                borderRadius: '0.625rem',
                padding: '0.25rem',
                gap: '0.25rem',
                boxShadow: '0 1px 2px rgba(0, 0, 0, 0.04)',
              }}
            >
              <button
                type="button"
                onClick={() => {
                  setActiveTab('upload');
                  setError(null);
                }}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem',
                  padding: '0.55rem 1.15rem',
                  borderRadius: '0.45rem',
                  border: 'none',
                  fontSize: '0.88rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  background: activeTab === 'upload' ? '#f1f5f9' : 'transparent',
                  color: activeTab === 'upload' ? '#0f172a' : '#64748b',
                  transition: 'all 0.15s ease',
                }}
              >
                <UploadCloud size={16} />
                <span>Upload image</span>
              </button>

              <button
                type="button"
                onClick={() => {
                  setActiveTab('camera');
                  setError(null);
                }}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem',
                  padding: '0.55rem 1.15rem',
                  borderRadius: '0.45rem',
                  border: 'none',
                  fontSize: '0.88rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  background: activeTab === 'camera' ? '#f1f5f9' : 'transparent',
                  color: activeTab === 'camera' ? '#0f172a' : '#64748b',
                  transition: 'all 0.15s ease',
                }}
              >
                <Camera size={16} />
                <span>Use camera</span>
              </button>
            </div>
          </div>

          {/* Active Mode Body */}
          {activeTab === 'upload' ? (
            <div>
              {/* Page 2 Layout: Left Dropzone + Right Checklist & Steps */}
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: '1.25fr 0.95fr',
                  gap: '1.75rem',
                  alignItems: 'start',
                }}
              >
                {/* Left: Upload Dropzone */}
                <div>
                  <ImageUpload onAnalyze={handleAnalyzeImage} isLoading={isLoading} />
                </div>

                {/* Right: Info Cards */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                  {/* Before you scan */}
                  <div
                    style={{
                      background: '#ffffff',
                      borderRadius: '1.25rem',
                      border: '1px solid #e2e8f0',
                      padding: '1.5rem',
                      boxShadow: '0 2px 4px rgba(0, 0, 0, 0.02)',
                    }}
                  >
                    <h4 style={{ fontSize: '1.05rem', fontWeight: 800, color: '#0f172a', marginBottom: '1rem' }}>
                      Before you scan
                    </h4>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                      {[
                        'Place the note flat on a plain surface.',
                        'Fill most of the frame and keep all four edges visible.',
                        'Use even light. Avoid flash and glare.',
                        'Hold steady to avoid motion blur.',
                      ].map((tip, idx) => (
                        <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
                          <div
                            style={{
                              width: '20px',
                              height: '20px',
                              borderRadius: '9999px',
                              background: '#dcfce7',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              flexShrink: 0,
                              marginTop: '0.1rem',
                            }}
                          >
                            <Check size={13} color="#16a34a" strokeWidth={3} />
                          </div>
                          <span style={{ fontSize: '0.86rem', color: '#334155', lineHeight: 1.5 }}>
                            {tip}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* What happens next */}
                  <div
                    style={{
                      background: '#ffffff',
                      borderRadius: '1.25rem',
                      border: '1px solid #e2e8f0',
                      padding: '1.5rem',
                      boxShadow: '0 2px 4px rgba(0, 0, 0, 0.02)',
                    }}
                  >
                    <h4 style={{ fontSize: '1.05rem', fontWeight: 800, color: '#0f172a', marginBottom: '1.15rem' }}>
                      What happens next
                    </h4>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                      {/* Step 1 */}
                      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.85rem' }}>
                        <div
                          style={{
                            width: '24px',
                            height: '24px',
                            borderRadius: '0.375rem',
                            background: '#eff6ff',
                            color: '#2563eb',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontWeight: 800,
                            fontSize: '0.82rem',
                            flexShrink: 0,
                          }}
                        >
                          1
                        </div>
                        <div>
                          <div style={{ fontSize: '0.88rem', fontWeight: 700, color: '#0f172a' }}>
                            Denomination
                          </div>
                          <div style={{ fontSize: '0.82rem', color: '#64748b', marginTop: '0.15rem' }}>
                            EfficientNetB0 identifies the note's value.
                          </div>
                        </div>
                      </div>

                      {/* Step 2 */}
                      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.85rem' }}>
                        <div
                          style={{
                            width: '24px',
                            height: '24px',
                            borderRadius: '0.375rem',
                            background: '#ecfdf5',
                            color: '#10b981',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontWeight: 800,
                            fontSize: '0.82rem',
                            flexShrink: 0,
                          }}
                        >
                          2
                        </div>
                        <div>
                          <div style={{ fontSize: '0.88rem', fontWeight: 700, color: '#0f172a' }}>
                            Authenticity cues
                          </div>
                          <div style={{ fontSize: '0.82rem', color: '#64748b', marginTop: '0.15rem' }}>
                            Visual alignment and feature checks give a screening verdict.
                          </div>
                        </div>
                      </div>

                      {/* Step 3 */}
                      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.85rem' }}>
                        <div
                          style={{
                            width: '24px',
                            height: '24px',
                            borderRadius: '0.375rem',
                            background: '#faf5ff',
                            color: '#9333ea',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontWeight: 800,
                            fontSize: '0.82rem',
                            flexShrink: 0,
                          }}
                        >
                          3
                        </div>
                        <div>
                          <div style={{ fontSize: '0.88rem', fontWeight: 700, color: '#0f172a' }}>
                            Explanation
                          </div>
                          <div style={{ fontSize: '0.82rem', color: '#64748b', marginTop: '0.15rem' }}>
                            Grad-CAM shows which regions guided the decision.
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Bottom Yellow Warning Banner */}
              <div
                style={{
                  marginTop: '2rem',
                  background: '#fffbeb',
                  border: '1px solid #fde68a',
                  borderRadius: '1rem',
                  padding: '1.1rem 1.4rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.85rem',
                }}
              >
                <AlertTriangle size={20} color="#b45309" style={{ flexShrink: 0 }} />
                <span style={{ color: '#92400e', fontSize: '0.84rem', lineHeight: 1.5 }}>
                  <strong>Screening estimate only.</strong> Results are not official currency authentication. When in doubt, inspect the note's physical security features and consult a bank.
                </span>
              </div>
            </div>
          ) : (
            <div>
              {/* Page 3: Live Camera Capture */}
              <CameraCapture onAnalyze={handleAnalyzeCamera} isLoading={isLoading} />
            </div>
          )}

          {error && (
            <div
              style={{
                marginTop: '1.5rem',
                padding: '1rem',
                borderRadius: '0.75rem',
                background: '#fef2f2',
                border: '1px solid #fecaca',
                color: '#dc2626',
                fontSize: '0.88rem',
              }}
            >
              {error}
            </div>
          )}
        </div>
      ) : (
        /* Page 4: Screening Result */
        <PredictionResult result={result} onReset={resetAnalysis} />
      )}
    </div>
  );
}
