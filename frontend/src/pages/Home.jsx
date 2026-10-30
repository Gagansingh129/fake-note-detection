import React from 'react';
import { ShieldCheck, Camera, Layers, ArrowRight, ShieldAlert, Cpu, Sparkles } from 'lucide-react';

export default function Home({ onNavigate }) {
  return (
    <div>
      {/* Hero Section */}
      <section style={{ textAlign: 'center', padding: '3.5rem 1rem 2.5rem' }}>
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.35rem 0.9rem',
            borderRadius: '9999px',
            background: 'rgba(59, 130, 246, 0.12)',
            border: '1px solid rgba(59, 130, 246, 0.25)',
            color: '#60a5fa',
            fontSize: '0.85rem',
            fontWeight: 600,
            marginBottom: '1.25rem',
          }}
        >
          <Sparkles size={15} /> Computer Vision Screening Pipeline
        </div>

        <h1
          style={{
            fontSize: 'clamp(2.2rem, 5vw, 3.5rem)',
            fontWeight: 800,
            lineHeight: 1.15,
            letterSpacing: '-0.02em',
            maxWidth: '850px',
            margin: '0 auto',
            background: 'linear-gradient(135deg, #ffffff 40%, #93c5fd 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          AI-Powered Currency Authenticity Screening
        </h1>

        <p
          style={{
            color: 'var(--text-secondary)',
            fontSize: 'clamp(1rem, 2vw, 1.2rem)',
            maxWidth: '650px',
            margin: '1.25rem auto 2.5rem',
          }}
        >
          Analyze Indian currency banknotes using Deep Learning and Computer Vision.
          Identify denominations and screen authenticity with Explainable AI diagnostics.
        </p>

        {/* Hero CTA Buttons */}
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <button className="btn btn-primary" onClick={() => onNavigate('analyze', 'upload')}>
            Analyze Note <ArrowRight size={18} />
          </button>
          <button className="btn btn-secondary" onClick={() => onNavigate('analyze', 'camera')}>
            <Camera size={18} /> Use Live Camera
          </button>
        </div>
      </section>

      {/* Feature Highlights Grid */}
      <section
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '1.5rem',
          marginTop: '2rem',
        }}
      >
        <div className="glass-card">
          <div
            style={{
              width: '44px',
              height: '44px',
              borderRadius: '0.625rem',
              background: 'rgba(59, 130, 246, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '1rem',
            }}
          >
            <Cpu size={22} color="#3b82f6" />
          </div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
            Two-Stage Deep Learning
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
            Powered by <strong>EfficientNetB0</strong> transfer learning.
            Stage 1 identifies banknote denominations (₹100, ₹200, ₹500), while Stage 2 evaluates authenticity cues.
          </p>
        </div>

        <div className="glass-card">
          <div
            style={{
              width: '44px',
              height: '44px',
              borderRadius: '0.625rem',
              background: 'rgba(16, 185, 129, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '1rem',
            }}
          >
            <Camera size={22} color="#10b981" />
          </div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
            Live Device Camera
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
            WebRTC video streaming with on-screen framing alignment.
            Includes automatic pre-screening for motion blur, brightness, and surface reflection.
          </p>
        </div>

        <div className="glass-card">
          <div
            style={{
              width: '44px',
              height: '44px',
              borderRadius: '0.625rem',
              background: 'rgba(147, 51, 234, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '1rem',
            }}
          >
            <Layers size={22} color="#c084fc" />
          </div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
            Explainable AI (Grad-CAM)
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
            Inspects the deepest convolutional layer activations to render heatmaps revealing which visual areas
            guided the model's classification.
          </p>
        </div>
      </section>

      {/* College Project Academic Disclaimer */}
      <div className="disclaimer-banner" style={{ marginTop: '3.5rem' }}>
        <ShieldAlert size={22} style={{ flexShrink: 0, marginTop: '2px' }} />
        <div>
          <strong>Academic Computer Vision Project:</strong> NoteGuard AI is developed for academic screening research.
          Predictions are non-binding statistical approximations that can be influenced by lighting conditions, camera blur, and dataset variance.
          Official currency authentication requires authorized Reserve Bank of India (RBI) physical inspections.
        </div>
      </div>
    </div>
  );
}
