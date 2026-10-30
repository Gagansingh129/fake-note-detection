import React from 'react';

export default function ConfidenceBar({ confidence = 0.0, authenticity = 'Genuine' }) {
  const percentage = Math.round(confidence * 1000) / 10;
  const isGenuine = authenticity.toLowerCase().includes('genuine');
  const isInconclusive = authenticity.toLowerCase().includes('inconclusive') || authenticity.toLowerCase().includes('uncertain');

  // Color selection based on confidence & prediction
  let barColor = '#10b981'; // green
  if (isInconclusive) {
    barColor = '#f59e0b'; // amber
  } else if (!isGenuine) {
    barColor = '#ef4444'; // red
  } else if (confidence < 0.80) {
    barColor = '#3b82f6'; // blue
  }

  return (
    <div style={{ marginTop: '1rem', width: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem', fontSize: '0.9rem' }}>
        <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>Confidence Assessment</span>
        <span style={{ fontWeight: 700, fontFamily: 'var(--font-mono)', color: barColor }}>
          {percentage.toFixed(1)}%
        </span>
      </div>

      {/* Progress Track */}
      <div
        style={{
          width: '100%',
          height: '10px',
          background: 'rgba(255, 255, 255, 0.08)',
          borderRadius: '9999px',
          overflow: 'hidden',
          position: 'relative',
        }}
      >
        <div
          style={{
            width: `${Math.min(100, Math.max(5, percentage))}%`,
            height: '100%',
            background: barColor,
            borderRadius: '9999px',
            transition: 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1)',
            boxShadow: `0 0 12px ${barColor}80`,
          }}
        />
      </div>

      {/* Threshold Marks */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          fontSize: '0.7rem',
          color: 'var(--text-muted)',
          marginTop: '0.35rem',
        }}
      >
        <span>0%</span>
        <span>60% (Threshold)</span>
        <span>80% (Confident)</span>
        <span>100%</span>
      </div>
    </div>
  );
}
