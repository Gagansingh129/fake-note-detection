import React from 'react';
import { 
  Cpu, 
  Camera, 
  Layers, 
  ArrowRight, 
  CheckCircle2, 
  AlertTriangle,
  Cog
} from 'lucide-react';

export default function Home({ onNavigate }) {
  return (
    <div style={{ background: '#f8fafc', color: '#0f172a', minHeight: '100vh' }}>
      
      {/* Hero Section */}
      <section style={{ maxWidth: '1240px', margin: '0 auto', padding: '3.5rem 1.5rem 2.5rem' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))', gap: '3rem', alignItems: 'center' }}>
          
          {/* Left Hero Content */}
          <div>
            {/* Pill Tag */}
            <div
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.45rem',
                padding: '0.35rem 0.85rem',
                borderRadius: '9999px',
                background: '#eff6ff',
                border: '1px solid #bfdbfe',
                color: '#2563eb',
                fontSize: '0.82rem',
                fontWeight: 600,
                marginBottom: '1.5rem',
              }}
            >
              <Cog size={15} color="#2563eb" />
              <span>Computer vision screening pipeline</span>
            </div>

            {/* Main Headline */}
            <h1
              style={{
                fontSize: 'clamp(2.5rem, 4.5vw, 3.8rem)',
                fontWeight: 900,
                lineHeight: 1.12,
                letterSpacing: '-0.03em',
                color: '#0f172a',
                marginBottom: '1.25rem',
              }}
            >
              AI-powered currency{' '}
              <span
                style={{
                  background: '#d1fae5',
                  color: '#065f46',
                  padding: '0.05rem 0.85rem',
                  borderRadius: '9999px',
                  display: 'inline-block',
                }}
              >
                authenticity
              </span>{' '}
              screening
            </h1>

            {/* Subtitle */}
            <p
              style={{
                color: '#475569',
                fontSize: '1.05rem',
                lineHeight: 1.6,
                maxWidth: '540px',
                marginBottom: '2rem',
              }}
            >
              Analyze Indian currency banknotes using deep learning and computer vision. 
              Identify the denomination, screen authenticity cues, and see exactly where the model looked with Explainable AI.
            </p>

            {/* CTA Buttons */}
            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
              <button
                onClick={() => onNavigate('analyze', 'upload')}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  padding: '0.8rem 1.6rem',
                  borderRadius: '0.625rem',
                  background: '#0f172a',
                  color: '#ffffff',
                  border: 'none',
                  fontSize: '0.95rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  boxShadow: '0 4px 6px -1px rgba(15, 23, 42, 0.2)',
                  transition: 'all 0.15s ease',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.background = '#1e293b')}
                onMouseLeave={(e) => (e.currentTarget.style.background = '#0f172a')}
              >
                <span>Analyze note</span>
                <ArrowRight size={17} />
              </button>

              <button
                onClick={() => onNavigate('analyze', 'camera')}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  padding: '0.8rem 1.5rem',
                  borderRadius: '0.625rem',
                  background: '#ffffff',
                  color: '#0f172a',
                  border: '1px solid #cbd5e1',
                  fontSize: '0.95rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
                  transition: 'all 0.15s ease',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.background = '#f8fafc')}
                onMouseLeave={(e) => (e.currentTarget.style.background = '#ffffff')}
              >
                <Camera size={18} color="#0f172a" />
                <span>Use live camera</span>
              </button>
            </div>
          </div>

          {/* Right Hero Preview Card */}
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <div
              style={{
                width: '100%',
                maxWidth: '480px',
                background: '#ffffff',
                borderRadius: '1.25rem',
                border: '1px solid #e2e8f0',
                boxShadow: '0 20px 40px -15px rgba(0, 0, 0, 0.1), 0 0 1px 1px rgba(0,0,0,0.04)',
                padding: '1.75rem',
              }}
            >
              {/* Card Header */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <span style={{ fontSize: '0.9rem', fontWeight: 600, color: '#334155' }}>
                  Screening result
                </span>
                <span
                  style={{
                    fontSize: '0.72rem',
                    fontWeight: 700,
                    color: '#475569',
                    background: '#f1f5f9',
                    padding: '0.2rem 0.55rem',
                    borderRadius: '0.375rem',
                    border: '1px solid #e2e8f0',
                  }}
                >
                  EfficientNetB0 v2.1
                </span>
              </div>

              {/* Detected Denomination & Pill */}
              <div style={{ marginBottom: '1.25rem' }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                  Detected denomination
                </div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '0.25rem' }}>
                  <div style={{ fontSize: '2.5rem', fontWeight: 900, color: '#0f172a', letterSpacing: '-0.02em', lineHeight: 1 }}>
                    ₹10
                  </div>
                  <div
                    style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '0.35rem',
                      background: '#dcfce7',
                      color: '#15803d',
                      border: '1px solid #bbf7d0',
                      padding: '0.35rem 0.8rem',
                      borderRadius: '9999px',
                      fontSize: '0.82rem',
                      fontWeight: 700,
                    }}
                  >
                    <CheckCircle2 size={15} color="#16a34a" />
                    <span>Likely genuine</span>
                  </div>
                </div>
              </div>

              {/* Progress Bars */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', marginBottom: '1.5rem' }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', fontWeight: 600, color: '#475569', marginBottom: '0.35rem' }}>
                    <span>Denomination confidence</span>
                    <span style={{ fontWeight: 800, color: '#0f172a' }}>100%</span>
                  </div>
                  <div style={{ height: '6px', background: '#e2e8f0', borderRadius: '9999px', overflow: 'hidden' }}>
                    <div style={{ height: '100%', width: '100%', background: '#2563eb', borderRadius: '9999px' }} />
                  </div>
                </div>

                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', fontWeight: 600, color: '#475569', marginBottom: '0.35rem' }}>
                    <span>Authenticity confidence</span>
                    <span style={{ fontWeight: 800, color: '#0f172a' }}>100%</span>
                  </div>
                  <div style={{ height: '6px', background: '#e2e8f0', borderRadius: '9999px', overflow: 'hidden' }}>
                    <div style={{ height: '100%', width: '100%', background: '#10b981', borderRadius: '9999px' }} />
                  </div>
                </div>
              </div>

              {/* Dual Visual Previews (Input note + Grad-CAM) */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.85rem' }}>
                <div
                  style={{
                    background: '#111827',
                    borderRadius: '0.75rem',
                    padding: '0.75rem',
                    textAlign: 'center',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '0.5rem',
                  }}
                >
                  <div
                    style={{
                      width: '100%',
                      height: '75px',
                      background: 'radial-gradient(ellipse at center, #8d5b4c 0%, #4a2810 100%)',
                      borderRadius: '0.45rem',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-around',
                      border: '1px solid rgba(255,255,255,0.1)',
                      position: 'relative',
                    }}
                  >
                    <div style={{ width: '28px', height: '28px', borderRadius: '9999px', background: 'rgba(255,255,255,0.15)' }} />
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', width: '40%' }}>
                      <div style={{ height: '4px', background: 'rgba(255,255,255,0.2)', borderRadius: '2px' }} />
                      <div style={{ height: '4px', background: 'rgba(255,255,255,0.15)', borderRadius: '2px' }} />
                      <div style={{ height: '4px', background: 'rgba(255,255,255,0.15)', borderRadius: '2px' }} />
                    </div>
                  </div>
                  <span style={{ fontSize: '0.72rem', color: '#94a3b8', fontWeight: 500 }}>
                    Input note
                  </span>
                </div>

                <div
                  style={{
                    background: '#111827',
                    borderRadius: '0.75rem',
                    padding: '0.75rem',
                    textAlign: 'center',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '0.5rem',
                  }}
                >
                  <div
                    style={{
                      width: '100%',
                      height: '75px',
                      background: 'radial-gradient(circle at 35% 50%, #ef4444 0%, #eab308 30%, #3b82f6 70%, #1e1b4b 100%)',
                      borderRadius: '0.45rem',
                      border: '1px solid rgba(255,255,255,0.1)',
                    }}
                  />
                  <span style={{ fontSize: '0.72rem', color: '#94a3b8', fontWeight: 500 }}>
                    Grad-CAM saliency
                  </span>
                </div>
              </div>

            </div>
          </div>

        </div>
      </section>

      {/* 3 Capabilities Feature Highlights Grid */}
      <section style={{ maxWidth: '1240px', margin: '0 auto', padding: '1rem 1.5rem 3.5rem' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
          
          {/* Card 1 */}
          <div
            style={{
              background: '#ffffff',
              borderRadius: '1rem',
              border: '1px solid #e2e8f0',
              padding: '1.75rem',
              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.02)',
            }}
          >
            <div
              style={{
                width: '46px',
                height: '46px',
                borderRadius: '0.75rem',
                background: '#eff6ff',
                border: '1px solid #dbeafe',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '1.25rem',
              }}
            >
              <Cpu size={24} color="#2563eb" />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: '#0f172a', marginBottom: '0.5rem' }}>
              Two-stage deep learning
            </h3>
            <p style={{ color: '#475569', fontSize: '0.88rem', lineHeight: 1.6 }}>
              Powered by <strong>EfficientNetB0</strong> transfer learning. Stage 1 identifies the banknote denomination, while Stage 2 evaluates authenticity cues.
            </p>
          </div>

          {/* Card 2 */}
          <div
            style={{
              background: '#ffffff',
              borderRadius: '1rem',
              border: '1px solid #e2e8f0',
              padding: '1.75rem',
              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.02)',
            }}
          >
            <div
              style={{
                width: '46px',
                height: '46px',
                borderRadius: '0.75rem',
                background: '#ecfdf5',
                border: '1px solid #d1fae5',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '1.25rem',
              }}
            >
              <Camera size={24} color="#10b981" />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: '#0f172a', marginBottom: '0.5rem' }}>
              Live device camera
            </h3>
            <p style={{ color: '#475569', fontSize: '0.88rem', lineHeight: 1.6 }}>
              WebRTC video streaming with on-screen framing alignment. Automatic pre-screening for motion blur, brightness and surface reflection.
            </p>
          </div>

          {/* Card 3 */}
          <div
            style={{
              background: '#ffffff',
              borderRadius: '1rem',
              border: '1px solid #e2e8f0',
              padding: '1.75rem',
              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.02)',
            }}
          >
            <div
              style={{
                width: '46px',
                height: '46px',
                borderRadius: '0.75rem',
                background: '#faf5ff',
                border: '1px solid #f3e8ff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '1.25rem',
              }}
            >
              <Layers size={24} color="#9333ea" />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: '#0f172a', marginBottom: '0.5rem' }}>
              Explainable AI (Grad-CAM)
            </h3>
            <p style={{ color: '#475569', fontSize: '0.88rem', lineHeight: 1.6 }}>
              Inspects the deepest convolutional layer activations to render heatmaps that reveal which visual areas guided the model's classification.
            </p>
          </div>

        </div>
      </section>

      {/* HOW IT WORKS Section (Dark Slate Navy container) */}
      <section style={{ maxWidth: '1240px', margin: '0 auto', padding: '0 1.5rem 3.5rem' }}>
        <div
          style={{
            background: '#0a1320',
            borderRadius: '1.5rem',
            padding: '3rem 2.5rem',
            color: '#f8fafc',
            border: '1px solid rgba(255, 255, 255, 0.06)',
          }}
        >
          <div style={{ marginBottom: '2.5rem' }}>
            <span
              style={{
                fontSize: '0.75rem',
                fontWeight: 800,
                letterSpacing: '0.1em',
                textTransform: 'uppercase',
                color: '#10b981',
                display: 'block',
                marginBottom: '0.5rem',
              }}
            >
              HOW IT WORKS
            </span>
            <h2
              style={{
                fontSize: 'clamp(1.75rem, 3.5vw, 2.4rem)',
                fontWeight: 900,
                letterSpacing: '-0.02em',
                lineHeight: 1.2,
                color: '#ffffff',
              }}
            >
              From a single photo to an<br />explained result
            </h2>
          </div>

          {/* 4 Step Cards */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
              gap: '1.25rem',
            }}
          >
            {/* Step 1 */}
            <div
              style={{
                background: '#111d2e',
                borderRadius: '1rem',
                border: '1px solid rgba(255, 255, 255, 0.06)',
                padding: '1.5rem',
                display: 'flex',
                flexDirection: 'column',
              }}
            >
              <div style={{ fontSize: '1.15rem', fontWeight: 800, color: '#10b981', marginBottom: '0.65rem' }}>
                01
              </div>
              <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#ffffff', marginBottom: '0.5rem' }}>
                Capture
              </h4>
              <p style={{ color: '#94a3b8', fontSize: '0.84rem', lineHeight: 1.5, margin: 0 }}>
                Upload a photo or stream from your device camera with live framing and quality pre-checks.
              </p>
            </div>

            {/* Step 2 */}
            <div
              style={{
                background: '#111d2e',
                borderRadius: '1rem',
                border: '1px solid rgba(255, 255, 255, 0.06)',
                padding: '1.5rem',
                display: 'flex',
                flexDirection: 'column',
              }}
            >
              <div style={{ fontSize: '1.15rem', fontWeight: 800, color: '#10b981', marginBottom: '0.65rem' }}>
                02
              </div>
              <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#ffffff', marginBottom: '0.5rem' }}>
                Stage 1: Denomination
              </h4>
              <p style={{ color: '#94a3b8', fontSize: '0.84rem', lineHeight: 1.5, margin: 0 }}>
                EfficientNetB0 identifies the banknote value and reports its confidence.
              </p>
            </div>

            {/* Step 3 */}
            <div
              style={{
                background: '#111d2e',
                borderRadius: '1rem',
                border: '1px solid rgba(255, 255, 255, 0.06)',
                padding: '1.5rem',
                display: 'flex',
                flexDirection: 'column',
              }}
            >
              <div style={{ fontSize: '1.15rem', fontWeight: 800, color: '#10b981', marginBottom: '0.65rem' }}>
                03
              </div>
              <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#ffffff', marginBottom: '0.5rem' }}>
                Stage 2: Authenticity
              </h4>
              <p style={{ color: '#94a3b8', fontSize: '0.84rem', lineHeight: 1.5, margin: 0 }}>
                Visual authenticity cues and computer-vision feature checks give a screening verdict.
              </p>
            </div>

            {/* Step 4 */}
            <div
              style={{
                background: '#111d2e',
                borderRadius: '1rem',
                border: '1px solid rgba(255, 255, 255, 0.06)',
                padding: '1.5rem',
                display: 'flex',
                flexDirection: 'column',
              }}
            >
              <div style={{ fontSize: '1.15rem', fontWeight: 800, color: '#10b981', marginBottom: '0.65rem' }}>
                04
              </div>
              <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#ffffff', marginBottom: '0.5rem' }}>
                Explain
              </h4>
              <p style={{ color: '#94a3b8', fontSize: '0.84rem', lineHeight: 1.5, margin: 0 }}>
                A Grad-CAM heatmap shows which regions of the note influenced the decision.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Academic Disclaimer Box */}
      <section style={{ maxWidth: '1240px', margin: '0 auto', padding: '0 1.5rem 3.5rem' }}>
        <div
          style={{
            background: '#fffbeb',
            border: '1px solid #fde68a',
            borderRadius: '1rem',
            padding: '1.25rem 1.5rem',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '1rem',
          }}
        >
          <AlertTriangle size={22} color="#b45309" style={{ flexShrink: 0, marginTop: '0.15rem' }} />
          <p style={{ color: '#92400e', fontSize: '0.84rem', lineHeight: 1.5, margin: 0 }}>
            <strong>Academic computer vision project.</strong> NoteGuard AI is built for screening research. Predictions are non-binding statistical estimates that lighting, camera blur and dataset variance can influence. Official currency authentication requires an authorized physical inspection by the Reserve Bank of India.
          </p>
        </div>
      </section>

      {/* Clean Footer */}
      <footer
        style={{
          borderTop: '1px solid #e2e8f0',
          padding: '2rem 1.5rem',
          textAlign: 'center',
          fontSize: '0.82rem',
          color: '#64748b',
          background: '#ffffff',
        }}
      >
        <div style={{ maxWidth: '1240px', margin: '0 auto' }}>
          <div style={{ fontWeight: 600, color: '#334155' }}>
            NoteGuard AI · Indian currency note authenticity detection system
          </div>
          <div style={{ marginTop: '0.35rem', fontSize: '0.78rem', color: '#94a3b8' }}>
            Academic computer vision project · TensorFlow 2.x · EfficientNetB0 · Grad-CAM · FastAPI · React + Vite
          </div>
        </div>
      </footer>

    </div>
  );
}
