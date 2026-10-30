import React, { useState } from 'react';
import { Eye, Layers, ZoomIn, AlertCircle } from 'lucide-react';
import { resolveImageUrl } from '../services/api';

export default function GradCAMViewer({ originalImageUrl, gradcamUrl }) {
  const [activeView, setActiveView] = useState('side-by-side');

  if (!gradcamUrl) {
    return (
      <div className="glass-card" style={{ marginTop: '1.5rem', textAlign: 'center', padding: '1.5rem' }}>
        <AlertCircle size={24} color="#f59e0b" style={{ margin: '0 auto 0.5rem' }} />
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Grad-CAM visual explanation is currently generating or unavailable for this record.
        </p>
      </div>
    );
  }

  const fullOriginalUrl = resolveImageUrl(originalImageUrl);
  const fullGradcamUrl = resolveImageUrl(gradcamUrl);

  return (
    <div className="glass-card" style={{ marginTop: '1.75rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Layers size={18} color="#3b82f6" /> Explainable AI (Grad-CAM Diagnostic)
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.2rem' }}>
            Highlights image regions that influenced the neural network's screening decision.
          </p>
        </div>

        {/* View Switcher */}
        <div style={{ display: 'flex', background: 'rgba(0,0,0,0.3)', borderRadius: '0.5rem', padding: '0.2rem' }}>
          <button
            onClick={() => setActiveView('side-by-side')}
            style={{
              background: activeView === 'side-by-side' ? 'rgba(59, 130, 246, 0.25)' : 'transparent',
              color: activeView === 'side-by-side' ? '#fff' : 'var(--text-secondary)',
              border: 'none',
              padding: '0.35rem 0.75rem',
              borderRadius: '0.35rem',
              fontSize: '0.8rem',
              cursor: 'pointer',
              fontWeight: 500,
            }}
          >
            Side-by-Side
          </button>
          <button
            onClick={() => setActiveView('composite')}
            style={{
              background: activeView === 'composite' ? 'rgba(59, 130, 246, 0.25)' : 'transparent',
              color: activeView === 'composite' ? '#fff' : 'var(--text-secondary)',
              border: 'none',
              padding: '0.35rem 0.75rem',
              borderRadius: '0.35rem',
              fontSize: '0.8rem',
              cursor: 'pointer',
              fontWeight: 500,
            }}
          >
            Composite Heatmap
          </button>
        </div>
      </div>

      {/* Side-by-Side Display */}
      {activeView === 'side-by-side' && (
        <div className="gradcam-grid">
          <div className="gradcam-card">
            <img src={fullOriginalUrl} alt="Original currency note" />
            <h4>Input Currency Note</h4>
          </div>
          <div className="gradcam-card">
            <img src={fullGradcamUrl} alt="Grad-CAM diagnostic" />
            <h4>Activation Overlay (Saliency Map)</h4>
          </div>
        </div>
      )}

      {/* Composite Display */}
      {activeView === 'composite' && (
        <div style={{ marginTop: '1.25rem', textAlign: 'center' }}>
          <img
            src={fullGradcamUrl}
            alt="Full Grad-CAM Analysis"
            style={{ width: '100%', maxHeight: '380px', objectFit: 'contain', borderRadius: '0.75rem', background: '#000' }}
          />
          <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginTop: '0.5rem' }}>
            Original Image (Left) | Salient Heatmap (Center) | Alpha-Blended Overlay (Right)
          </p>
        </div>
      )}

      {/* Transparency Note */}
      <div
        style={{
          marginTop: '1rem',
          padding: '0.6rem 0.9rem',
          borderRadius: '0.5rem',
          background: 'rgba(59, 130, 246, 0.08)',
          border: '1px solid rgba(59, 130, 246, 0.15)',
          fontSize: '0.8rem',
          color: '#93c5fd',
        }}
      >
        <strong>Interpreting Grad-CAM:</strong> Warm areas (red, yellow) indicate high neural activation weight. Cooler areas (blue) had negligible influence.
      </div>
    </div>
  );
}
