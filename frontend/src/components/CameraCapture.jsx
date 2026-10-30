import React, { useState, useRef, useEffect } from 'react';
import { Camera, RefreshCw, CheckCircle, AlertTriangle, ArrowRight, VideoOff, Loader2 } from 'lucide-react';

export default function CameraCapture({ onAnalyze, isLoading }) {
  const [streamActive, setStreamActive] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [cameraError, setCameraError] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  // Stop camera stream on unmount
  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  const startCamera = async () => {
    setCameraError(null);
    try {
      if (!window.isSecureContext && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        throw new Error('INSECURE_CONTEXT');
      }

      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('NO_MEDIA_DEVICES');
      }

      const constraints = {
        video: {
          facingMode: 'environment', // Prefer back camera on mobile devices
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
      };

      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        videoRef.current.play();
      }
      setStreamActive(true);
      setCapturedImage(null);
    } catch (err) {
      console.error('[Camera Access Error]:', err);
      let msg = 'Failed to access device camera. Please check camera permissions.';
      if (err.message === 'INSECURE_CONTEXT' || err.message === 'NO_MEDIA_DEVICES') {
        msg = 'Browser Security Restriction: Web browsers block camera access on plain HTTP (http://) IP addresses. To use the camera, open "chrome://flags/#unsafely-treat-insecure-origin-as-secure" in Chrome/Edge, add "http://' + window.location.host + '", enable it, and relaunch your browser.';
      } else if (err.name === 'NotAllowedError') {
        msg = 'Camera permission was denied. Please click the camera/lock icon in your browser address bar and allow camera access.';
      } else if (err.name === 'NotFoundError') {
        msg = 'No video camera detected on this system.';
      }
      setCameraError(msg);
      setStreamActive(false);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach((track) => track.stop());
      videoRef.current.srcObject = null;
    }
    setStreamActive(false);
  };

  const captureFrame = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;

    const vWidth = video.videoWidth || 640;
    const vHeight = video.videoHeight || 480;

    // Isolate the central guide box area (78% width, 52% height)
    // This physically excludes the user's head, face, hair, and room background
    const cropW = Math.round(vWidth * 0.78);
    const cropH = Math.round(vHeight * 0.52);
    const cropX = Math.round((vWidth - cropW) / 2);
    // Align with the guide frame, safely below the user's head
    const cropY = Math.round((vHeight - cropH) / 2 + vHeight * 0.04);

    canvas.width = cropW;
    canvas.height = cropH;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, cropX, cropY, cropW, cropH, 0, 0, cropW, cropH);

    // Get high-quality base64 JPEG of the cropped banknote
    const dataUrl = canvas.toDataURL('image/jpeg', 0.95);
    setCapturedImage(dataUrl);
    stopCamera();
  };

  const retake = () => {
    setCapturedImage(null);
    startCamera();
  };

  const handleAnalyze = () => {
    if (capturedImage && !isLoading) {
      onAnalyze(capturedImage);
    }
  };

  return (
    <div className="glass-card" style={{ maxWidth: '680px', margin: '0 auto' }}>
      <canvas ref={canvasRef} style={{ display: 'none' }} />

      {/* Viewport: Live Stream or Freeze-frame Preview */}
      <div className="camera-viewport">
        {capturedImage ? (
          <img
            src={capturedImage}
            alt="Captured currency note"
            style={{ width: '100%', height: '100%', objectFit: 'contain' }}
          />
        ) : (
          <>
            <video
              ref={videoRef}
              playsInline
              muted
              className="camera-video"
              style={{ display: streamActive ? 'block' : 'none' }}
            />
            {streamActive && (
              <div className="camera-guide-overlay">
                <div className="camera-guide-box">
                  <div className="camera-corner corner-tl" />
                  <div className="camera-corner corner-tr" />
                  <div className="camera-corner corner-bl" />
                  <div className="camera-corner corner-br" />
                </div>
                <div className="camera-guide-text">
                  Place currency note flat inside frame
                </div>
              </div>
            )}
            {!streamActive && !capturedImage && (
              <div style={{ textAlign: 'center', padding: '2rem' }}>
                <Camera size={54} color="#60a5fa" style={{ margin: '0 auto 1rem', opacity: 0.8 }} />
                <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Webcam Currency Scanner</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.5rem', maxWidth: '380px' }}>
                  Position the note under direct room light and ensure Mahatma Gandhi portrait and security thread are visible.
                </p>
              </div>
            )}
          </>
        )}
      </div>

      {/* Guidance Checklist */}
      <div
        style={{
          marginTop: '1.25rem',
          padding: '0.85rem 1rem',
          borderRadius: '0.625rem',
          background: 'rgba(0, 0, 0, 0.25)',
          border: '1px solid var(--border-color)',
          fontSize: '0.8rem',
          color: 'var(--text-secondary)',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
          gap: '0.5rem',
        }}
      >
        <span>• Keep the entire note visible</span>
        <span>• Hold camera steady (avoid blur)</span>
        <span>• Avoid strong reflection / glare</span>
        <span>• Use even, flat illumination</span>
      </div>

      {/* Action Controls */}
      <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1.25rem' }}>
        {!streamActive && !capturedImage && (
          <button className="btn btn-primary" onClick={startCamera} style={{ width: '100%' }}>
            <Camera size={18} /> Start Camera
          </button>
        )}

        {streamActive && (
          <>
            <button className="btn btn-secondary" onClick={stopCamera} style={{ flex: 1 }}>
              <VideoOff size={18} /> Cancel
            </button>
            <button className="btn btn-primary" onClick={captureFrame} style={{ flex: 2 }}>
              <Camera size={18} /> Capture Note
            </button>
          </>
        )}

        {capturedImage && (
          <>
            <button className="btn btn-secondary" onClick={retake} disabled={isLoading} style={{ flex: 1 }}>
              <RefreshCw size={18} /> Retake
            </button>
            <button className="btn btn-primary" onClick={handleAnalyze} disabled={isLoading} style={{ flex: 2 }}>
              {isLoading ? (
                <>
                  <Loader2 size={18} className="pulse" /> Analyzing Note...
                </>
              ) : (
                <>
                  Analyze Note Authenticity <ArrowRight size={18} />
                </>
              )}
            </button>
          </>
        )}
      </div>

      {/* Camera Errors */}
      {cameraError && (
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
          <AlertTriangle size={16} /> {cameraError}
        </div>
      )}
    </div>
  );
}
