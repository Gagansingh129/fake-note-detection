import React from 'react';
import { 
  ShieldCheck, 
  AlertOctagon, 
  AlertTriangle, 
  CheckCircle2, 
  RotateCcw, 
  Clock, 
  Sparkles, 
  Layers, 
  ShieldAlert,
  Banknote,
  Info
} from 'lucide-react';
import ConfidenceBar from './ConfidenceBar';
import GradCAMViewer from './GradCAMViewer';

export default function PredictionResult({ result, onReset }) {
  if (!result) return null;

  const {
    denomination,
    denomination_label,
    circulation_status,
    denomination_confidence,
    authenticity,
    authenticity_confidence,
    confidence,
    genuine_score,
    fake_score,
    decision_status,
    status_label,
    warning,
    disclaimer,
    security_features,
    image_quality,
    original_image_url,
    gradcam_url,
    inference_time_ms,
    model_version,
  } = result;

  // Authentic vs Counterfeit states
  const isGenuine = decision_status === 'likely_genuine' || (authenticity && authenticity.toLowerCase().includes('genuine'));
  const isFake = decision_status === 'suspected_fake' || (authenticity && authenticity.toLowerCase().includes('fake'));
  const isUncertain = !isGenuine && !isFake;

  const bannerColor = isGenuine ? '#10b981' : isFake ? '#ef4444' : '#f59e0b';
  const displayTitle = isGenuine
    ? 'Likely Genuine'
    : isFake
    ? 'Suspected Fake'
    : 'Uncertain / Unable to Verify';

  // Format denomination display
  const displayDenomLabel = denomination_label || (denomination ? `₹${denomination}` : 'Unknown Denomination');
  const isUnknownDenom = !denomination || denomination === 'Unknown' || (denomination_confidence !== undefined && denomination_confidence < 0.40);
  
  // Format confidences
  const denomConfPct = Math.round((denomination_confidence ?? 0.85) * 100);
  const authConfPct = Math.round((authenticity_confidence ?? confidence ?? 0.85) * 100);

  // Status color for circulation pill
  let circBadgeBg = 'rgba(59, 130, 246, 0.15)';
  let circBadgeColor = '#60a5fa';
  let circBadgeBorder = 'rgba(59, 130, 246, 0.3)';

  if (circulation_status) {
    if (circulation_status.toLowerCase().includes('circulating') || circulation_status.toLowerCase().includes('legal tender')) {
      circBadgeBg = 'rgba(16, 185, 129, 0.15)';
      circBadgeColor = '#34d399';
      circBadgeBorder = 'rgba(16, 185, 129, 0.3)';
    } else if (circulation_status.toLowerCase().includes('withdrawn') || circulation_status.toLowerCase().includes('demonetized')) {
      circBadgeBg = 'rgba(168, 85, 247, 0.15)';
      circBadgeColor = '#c084fc';
      circBadgeBorder = 'rgba(168, 85, 247, 0.3)';
    } else if (circulation_status.toLowerCase().includes('counterfeit') || circulation_status.toLowerCase().includes('bogus')) {
      circBadgeBg = 'rgba(239, 68, 68, 0.15)';
      circBadgeColor = '#f87171';
      circBadgeBorder = 'rgba(239, 68, 68, 0.3)';
    }
  }

  return (
    <div style={{ maxWidth: '840px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      
      {/* Top Controls & Meta Bar */}
      <div 
        style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center', 
          flexWrap: 'wrap', 
          gap: '0.75rem',
          padding: '0.5rem 0.25rem'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
          {model_version && (
            <span
              style={{
                fontSize: '0.78rem',
                padding: '0.25rem 0.65rem',
                borderRadius: '0.375rem',
                background: 'rgba(255, 255, 255, 0.06)',
                color: 'var(--text-muted)',
                border: '1px solid rgba(255, 255, 255, 0.08)',
              }}
            >
              Models: {model_version}
            </span>
          )}

          {inference_time_ms && (
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
              <Clock size={13} /> {inference_time_ms} ms
            </span>
          )}
        </div>

        <button className="btn btn-secondary" onClick={onReset} style={{ fontSize: '0.85rem', padding: '0.45rem 0.95rem' }}>
          <RotateCcw size={15} /> Screen Another Note
        </button>
      </div>

      {/* Primary Dual-Panel Hero Card (Denomination + Authenticity) */}
      <div
        className="glass-card"
        style={{
          borderLeft: `6px solid ${bannerColor}`,
          position: 'relative',
          overflow: 'hidden',
          padding: '1.5rem',
          background: isGenuine
            ? 'linear-gradient(135deg, rgba(16, 185, 129, 0.09) 0%, rgba(15, 23, 42, 0.85) 100%)'
            : isFake
            ? 'linear-gradient(135deg, rgba(239, 68, 68, 0.09) 0%, rgba(15, 23, 42, 0.85) 100%)'
            : 'linear-gradient(135deg, rgba(245, 158, 11, 0.09) 0%, rgba(15, 23, 42, 0.85) 100%)',
        }}
      >
        {/* Prominent Two-Column Hero Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: '1.5rem',
            alignItems: 'stretch',
          }}
        >
          {/* Hero Column 1: Detected Denomination */}
          <div
            style={{
              padding: '1.25rem',
              borderRadius: '0.75rem',
              background: 'rgba(0, 0, 0, 0.35)',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}
          >
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem', color: '#94a3b8', fontSize: '0.82rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                <Banknote size={18} color="#60a5fa" />
                Detected Denomination
              </div>

              <div
                style={{
                  fontSize: '2.4rem',
                  fontWeight: 900,
                  fontFamily: 'var(--font-mono, monospace)',
                  color: isUnknownDenom ? '#f59e0b' : '#60a5fa',
                  lineHeight: '1.2',
                  margin: '0.25rem 0 0.5rem 0',
                }}
              >
                {displayDenomLabel}
              </div>

              {circulation_status && (
                <div style={{ marginTop: '0.35rem', marginBottom: '0.85rem' }}>
                  <span
                    style={{
                      fontSize: '0.74rem',
                      fontWeight: 600,
                      padding: '0.2rem 0.55rem',
                      borderRadius: '0.3rem',
                      background: circBadgeBg,
                      color: circBadgeColor,
                      border: `1px solid ${circBadgeBorder}`,
                      display: 'inline-block',
                    }}
                  >
                    {circulation_status}
                  </span>
                </div>
              )}
            </div>

            {/* Denomination Confidence Track */}
            <div style={{ marginTop: '0.75rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '0.35rem' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Denomination Confidence</span>
                <span style={{ fontWeight: 700, fontFamily: 'var(--font-mono)', color: '#60a5fa' }}>
                  {denomConfPct}%
                </span>
              </div>
              <div style={{ height: '7px', borderRadius: '4px', background: 'rgba(255,255,255,0.08)', overflow: 'hidden' }}>
                <div 
                  style={{ 
                    width: `${Math.min(100, Math.max(5, denomConfPct))}%`, 
                    height: '100%', 
                    background: '#3b82f6', 
                    borderRadius: '4px',
                    boxShadow: '0 0 8px rgba(59, 130, 246, 0.5)',
                    transition: 'width 0.6s ease' 
                  }} 
                />
              </div>
            </div>
          </div>

          {/* Hero Column 2: Authenticity Result */}
          <div
            style={{
              padding: '1.25rem',
              borderRadius: '0.75rem',
              background: 'rgba(0, 0, 0, 0.35)',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}
          >
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem', color: '#94a3b8', fontSize: '0.82rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                <ShieldCheck size={18} color={bannerColor} />
                Authenticity Result
              </div>

              <div
                style={{
                  fontSize: '2rem',
                  fontWeight: 900,
                  color: bannerColor,
                  lineHeight: '1.25',
                  margin: '0.25rem 0 0.4rem 0',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                }}
              >
                {isGenuine ? (
                  <CheckCircle2 size={28} color="#10b981" style={{ flexShrink: 0 }} />
                ) : isFake ? (
                  <AlertOctagon size={28} color="#ef4444" style={{ flexShrink: 0 }} />
                ) : (
                  <AlertTriangle size={28} color="#f59e0b" style={{ flexShrink: 0 }} />
                )}
                <span>{displayTitle}</span>
              </div>

              <div style={{ color: 'var(--text-secondary)', fontSize: '0.82rem', marginBottom: '0.85rem', lineHeight: '1.35' }}>
                {status_label || (isGenuine ? 'Visual features match genuine security baseline' : 'Discrepancy detected in banknote features')}
              </div>
            </div>

            {/* Authenticity Confidence Track */}
            <div style={{ marginTop: '0.75rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '0.35rem' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Authenticity Confidence</span>
                <span style={{ fontWeight: 700, fontFamily: 'var(--font-mono)', color: bannerColor }}>
                  {authConfPct}%
                </span>
              </div>
              <div style={{ height: '7px', borderRadius: '4px', background: 'rgba(255,255,255,0.08)', overflow: 'hidden' }}>
                <div 
                  style={{ 
                    width: `${Math.min(100, Math.max(5, authConfPct))}%`, 
                    height: '100%', 
                    background: bannerColor, 
                    borderRadius: '4px',
                    boxShadow: `0 0 8px ${bannerColor}80`,
                    transition: 'width 0.6s ease' 
                  }} 
                />
              </div>
            </div>
          </div>
        </div>

        {/* Predictive Probability Breakdown */}
        {genuine_score !== undefined && fake_score !== undefined && (
          <div
            style={{
              marginTop: '1.25rem',
              padding: '0.85rem 1rem',
              borderRadius: '0.5rem',
              background: 'rgba(0, 0, 0, 0.4)',
              border: '1px solid var(--border-color)',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '0.4rem' }}>
              <span style={{ color: '#10b981', fontWeight: 600 }}>Genuine Alignment Score: {Math.round(genuine_score * 100)}%</span>
              <span style={{ color: '#ef4444', fontWeight: 600 }}>Counterfeit Discrepancy Score: {Math.round(fake_score * 100)}%</span>
            </div>
            <div style={{ height: '8px', borderRadius: '4px', background: '#374151', display: 'flex', overflow: 'hidden' }}>
              <div style={{ width: `${Math.round(genuine_score * 100)}%`, background: '#10b981', transition: 'width 0.4s ease' }} />
              <div style={{ width: `${Math.round(fake_score * 100)}%`, background: '#ef4444', transition: 'width 0.4s ease' }} />
            </div>
          </div>
        )}

        {/* Warning / Advisory Notice */}
        {warning && (
          <div
            style={{
              marginTop: '1.25rem',
              padding: '0.75rem 1rem',
              borderRadius: '0.5rem',
              background: isUncertain
                ? 'rgba(245, 158, 11, 0.12)'
                : isFake
                ? 'rgba(239, 68, 68, 0.1)'
                : 'rgba(59, 130, 246, 0.08)',
              border: `1px solid ${
                isUncertain
                  ? 'rgba(245, 158, 11, 0.3)'
                  : isFake
                  ? 'rgba(239, 68, 68, 0.3)'
                  : 'rgba(59, 130, 246, 0.2)'
              }`,
              fontSize: '0.88rem',
              color: isUncertain ? '#fbbf24' : isFake ? '#f87171' : '#93c5fd',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
            }}
          >
            <AlertTriangle size={18} style={{ flexShrink: 0 }} />
            <span>{warning}</span>
          </div>
        )}
      </div>

      {/* OpenCV Computer Vision Security Feature Diagnostics */}
      {security_features && (
        <div className="glass-card">
          <h3 style={{ fontSize: '1.05rem', fontWeight: 600, marginBottom: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Layers size={18} color="#60a5fa" /> Computer Vision Security Feature Analysis (Supporting Evidence)
          </h3>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
              gap: '1rem',
              marginBottom: '1rem',
            }}
          >
            <div style={{ background: 'rgba(0,0,0,0.3)', padding: '0.85rem', borderRadius: '0.5rem', border: '1px solid var(--border-color)' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>Banknote Aspect Ratio</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'var(--font-mono)', marginTop: '0.2rem' }}>
                {security_features.aspect_ratio?.measured} <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>(ref: {security_features.aspect_ratio?.expected_reference})</span>
              </div>
              <div style={{ fontSize: '0.75rem', marginTop: '0.3rem', color: security_features.aspect_ratio?.is_valid ? '#10b981' : '#f59e0b' }}>
                {security_features.aspect_ratio?.status}
              </div>
            </div>

            <div style={{ background: 'rgba(0,0,0,0.3)', padding: '0.85rem', borderRadius: '0.5rem', border: '1px solid var(--border-color)' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>Security Thread Region</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'var(--font-mono)', marginTop: '0.2rem' }}>
                Gradient: {security_features.security_thread?.edge_gradient_intensity}
              </div>
              <div style={{ fontSize: '0.75rem', marginTop: '0.3rem', color: security_features.security_thread?.is_valid ? '#10b981' : '#f59e0b' }}>
                {security_features.security_thread?.status}
              </div>
            </div>

            <div style={{ background: 'rgba(0,0,0,0.3)', padding: '0.85rem', borderRadius: '0.5rem', border: '1px solid var(--border-color)' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>Micro-Texture Sharpness</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'var(--font-mono)', marginTop: '0.2rem' }}>
                Variance: {security_features.print_texture?.micro_texture_variance}
              </div>
              <div style={{ fontSize: '0.75rem', marginTop: '0.3rem', color: security_features.print_texture?.is_valid ? '#10b981' : '#f59e0b' }}>
                {security_features.print_texture?.status}
              </div>
            </div>

            <div style={{ background: 'rgba(0,0,0,0.3)', padding: '0.85rem', borderRadius: '0.5rem', border: '1px solid var(--border-color)' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>Portrait Dynamic Range</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'var(--font-mono)', marginTop: '0.2rem' }}>
                Contrast: {security_features.portrait_contrast?.contrast_variance}
              </div>
              <div style={{ fontSize: '0.75rem', marginTop: '0.3rem', color: security_features.portrait_contrast?.is_valid ? '#10b981' : '#f59e0b' }}>
                {security_features.portrait_contrast?.status}
              </div>
            </div>
          </div>

          {/* Transparent forensic notice regarding features not verifiable by camera */}
          <div
            style={{
              padding: '0.75rem 1rem',
              borderRadius: '0.5rem',
              background: 'rgba(15, 23, 42, 0.6)',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              fontSize: '0.8rem',
              color: 'var(--text-secondary)',
            }}
          >
            <div style={{ fontWeight: 600, color: '#e2e8f0', marginBottom: '0.3rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <ShieldAlert size={14} color="#f59e0b" /> Hardware-Dependent Security Features (Not Verifiable on Camera):
            </div>
            <ul style={{ margin: '0.2rem 0 0 1.2rem', padding: 0, lineHeight: '1.45' }}>
              {security_features.physical_features_unavailable_on_camera?.map((item, idx) => (
                <li key={idx}>
                  <strong style={{ color: '#cbd5e1' }}>{item.feature}:</strong> {item.reason}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Image Quality Pre-Screening Diagnostics */}
      {image_quality && (
        <div className="glass-card">
          <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Sparkles size={16} color="#60a5fa" /> Image Quality Screening Diagnostics
          </h3>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))',
              gap: '1rem',
            }}
          >
            <div style={{ background: 'rgba(0,0,0,0.25)', padding: '0.75rem', borderRadius: '0.5rem' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>Sharpness (Laplacian)</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                {image_quality.blur_score}
              </div>
              <div style={{ fontSize: '0.7rem', color: image_quality.blur_score >= 60 ? '#10b981' : '#f59e0b' }}>
                {image_quality.blur_score >= 60 ? 'Sharp Edge Fidelity' : 'Borderline Soft Focus'}
              </div>
            </div>

            <div style={{ background: 'rgba(0,0,0,0.25)', padding: '0.75rem', borderRadius: '0.5rem' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>Illumination (HSV Value)</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                {Math.round(image_quality.brightness * 100)}%
              </div>
              <div style={{ fontSize: '0.7rem', color: image_quality.brightness >= 0.22 && image_quality.brightness <= 0.92 ? '#10b981' : '#ef4444' }}>
                {image_quality.brightness >= 0.22 ? 'Adequate Light' : 'Low Light'}
              </div>
            </div>

            <div style={{ background: 'rgba(0,0,0,0.25)', padding: '0.75rem', borderRadius: '0.5rem' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>Specular Glare</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                {Math.round(image_quality.glare_ratio * 100)}%
              </div>
              <div style={{ fontSize: '0.7rem', color: image_quality.glare_ratio <= 0.20 ? '#10b981' : '#f59e0b' }}>
                {image_quality.glare_ratio <= 0.20 ? 'No Flash Interference' : 'High Surface Reflection'}
              </div>
            </div>

            <div style={{ background: 'rgba(0,0,0,0.25)', padding: '0.75rem', borderRadius: '0.5rem' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>Quality Status</div>
              <div
                style={{
                  fontSize: '1.1rem',
                  fontWeight: 700,
                  color: image_quality.status === 'Good' ? '#10b981' : image_quality.status === 'Acceptable' ? '#f59e0b' : '#ef4444',
                }}
              >
                {image_quality.status}
              </div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>
                {image_quality.is_acceptable ? 'Sufficient for Screening' : 'Recapture Recommended'}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Grad-CAM Explainable AI Visualization */}
      <GradCAMViewer originalImageUrl={original_image_url} gradcamUrl={gradcam_url} />

      {/* Standard Legal & Screening Disclaimer */}
      <div className="disclaimer-banner">
        <AlertTriangle size={22} style={{ flexShrink: 0, marginTop: '2px', color: '#f59e0b' }} />
        <div>
          <strong style={{ color: '#fff' }}>Official Currency Screening Disclaimer:</strong>{' '}
          {disclaimer || (
            "This AI result is a preliminary screening estimate, not official currency authentication. " +
            "Camera images cannot verify every physical security feature. " +
            "If authenticity is uncertain, inspect the note's security features and consult an appropriate bank."
          )}
        </div>
      </div>
    </div>
  );
}
