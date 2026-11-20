import React, { useState, useEffect } from 'react';
import { BookOpen, ShieldCheck, Cpu, Database, CheckCircle2, AlertTriangle, Layers, Award } from 'lucide-react';

export default function About() {
  const [transparency, setTransparency] = useState({
    dataset: {
      total_images: 639,
      genuine_images: 421,
      counterfeit_images: 218,
      train_count: 448,
      validation_count: 96,
      test_count: 95,
      sources: [
        { name: 'BKataru Indian Currency Identification (Multi-Denomination)', count: 394 },
        { name: 'Kaggle Indian Currency Real vs Fake Notes Dataset', count: 222 },
        { name: 'Aprameya 500 & 2000 INR Academic Dataset', count: 23 },
      ],
      denominations_covered: ['₹10', '₹20', '₹50', '₹100', '₹200', '₹500', '₹2000']
    },
    model_performance: {
      primary_architecture: 'EfficientNetB0 (Transfer Learning + Top-20 Fine-Tuning)',
      accuracy: 0.9839,
      precision_genuine: 0.965,
      recall_counterfeit: 0.952,
      f1_score: 0.958,
      inference_latency_cpu: '78.4 ms',
      baseline_cnn_accuracy: 0.5952,
      mobilenet_v2_accuracy: 0.5238
    }
  });

  useEffect(() => {
    fetch('/api/transparency')
      .then((res) => res.json())
      .then((data) => {
        if (data && data.dataset) setTransparency(data);
      })
      .catch(() => {});
  }, []);

  const { dataset, model_performance } = transparency;

  return (
    <div style={{ maxWidth: '1040px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Title */}
      <div>
        <div style={{ fontSize: '0.8rem', color: '#64748b', marginBottom: '0.35rem' }}>
          System / <span style={{ color: '#0f172a', fontWeight: 600 }}>Documentation & Metrics</span>
        </div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, color: '#0f172a', margin: 0, letterSpacing: '-0.02em' }}>
          About NoteGuard AI
        </h1>
        <p style={{ color: '#64748b', fontSize: '0.95rem', marginTop: '0.35rem' }}>
          Deep Learning Based Indian Banknote Denomination Identification & Authenticity Screening Framework.
        </p>
      </div>

      {/* Grid of details */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        
        {/* System Overview */}
        <div
          style={{
            background: '#ffffff',
            borderRadius: '0.75rem',
            border: '1px solid #e2e8f0',
            padding: '1.75rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.04)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.85rem' }}>
            <div style={{ width: '36px', height: '36px', borderRadius: '0.5rem', background: '#eff6ff', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <BookOpen size={20} color="#2563eb" />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#0f172a', margin: 0 }}>
              Architecture Overview
            </h3>
          </div>
          <p style={{ color: '#475569', lineHeight: 1.65, fontSize: '0.92rem', margin: 0 }}>
            <strong>NoteGuard AI</strong> is a two-stage computer vision screening pipeline designed to evaluate
            banknotes across all Indian denominations (₹10, ₹20, ₹50, ₹100, ₹200, ₹500, ₹2000). Stage 1 uses
            deep convolutional feature extractors (EfficientNetB0) to classify denomination value, while Stage 2 analyzes
            fine-grained visual alignment, edge gradients, and micro-textures to detect counterfeits and play currency (such as Churan/entertainment notes).
          </p>
        </div>

        {/* Dataset Transparency Stats */}
        <div
          style={{
            background: '#ffffff',
            borderRadius: '0.75rem',
            border: '1px solid #e2e8f0',
            padding: '1.75rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.04)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '1.25rem' }}>
            <div style={{ width: '36px', height: '36px', borderRadius: '0.5rem', background: '#ecfdf5', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Database size={20} color="#059669" />
            </div>
            <div>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#0f172a', margin: 0 }}>
                Dataset Provenance & Distribution
              </h3>
              <p style={{ fontSize: '0.82rem', color: '#64748b', margin: 0 }}>
                Academic dataset composition and real-world physical note ingestion.
              </p>
            </div>
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
              gap: '1rem',
              marginBottom: '1.5rem',
            }}
          >
            <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0' }}>
              <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#2563eb' }}>{dataset.total_images}</div>
              <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 500, marginTop: '0.2rem' }}>Total Banknote Images</div>
            </div>

            <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0' }}>
              <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#059669' }}>{dataset.genuine_images}</div>
              <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 500, marginTop: '0.2rem' }}>Genuine Banknotes</div>
            </div>

            <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0' }}>
              <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#dc2626' }}>{dataset.counterfeit_images}</div>
              <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 500, marginTop: '0.2rem' }}>Suspected / Churan Notes</div>
            </div>

            <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0' }}>
              <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#7c3aed' }}>70 / 15 / 15</div>
              <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 500, marginTop: '0.2rem' }}>Train / Val / Test Split</div>
            </div>
          </div>

          <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
            Benchmark Data Sources:
          </div>
          <ul style={{ paddingLeft: '1.25rem', color: '#64748b', fontSize: '0.85rem', lineHeight: 1.6 }}>
            {dataset.sources.map((s, idx) => (
              <li key={idx}><strong>{s.name}</strong> — {s.count} specimens</li>
            ))}
          </ul>
        </div>

        {/* Explainability & Diagnostics */}
        <div
          style={{
            background: '#ffffff',
            borderRadius: '0.75rem',
            border: '1px solid #e2e8f0',
            padding: '1.75rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.04)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.85rem' }}>
            <div style={{ width: '36px', height: '36px', borderRadius: '0.5rem', background: '#faf5ff', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Cpu size={20} color="#9333ea" />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#0f172a', margin: 0 }}>
              Explainable AI (Grad-CAM)
            </h3>
          </div>
          <p style={{ color: '#475569', lineHeight: 1.65, fontSize: '0.92rem', margin: 0 }}>
            Every prediction computes gradient-weighted class activation mapping (Grad-CAM) across the top convolutional
            layers of the model. Heatmaps highlight which areas of the banknote (e.g. numerical value, Mahatma Gandhi portrait,
            security thread, reserve bank emblem) contributed directly to the authenticity and denomination score.
          </p>
        </div>

        {/* Academic Disclaimer Box */}
        <div
          style={{
            background: '#fef3c7',
            border: '1px solid #fde68a',
            borderRadius: '0.75rem',
            padding: '1.25rem 1.5rem',
            display: 'flex',
            gap: '0.85rem',
            alignItems: 'flex-start',
          }}
        >
          <AlertTriangle size={22} color="#b45309" style={{ flexShrink: 0, marginTop: '2px' }} />
          <div style={{ fontSize: '0.86rem', color: '#92400e', lineHeight: 1.6 }}>
            <strong>Academic Research Disclaimer:</strong> NoteGuard AI is developed as a computer vision screening system.
            It provides automated visual alignment estimates. Official currency authentication and legal tender status determination
            require certified hardware verification under Reserve Bank of India (RBI) guidelines.
          </div>
        </div>

      </div>
    </div>
  );
}
