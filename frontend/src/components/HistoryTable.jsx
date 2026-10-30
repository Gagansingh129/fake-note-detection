import React, { useState } from 'react';
import { Trash2, ExternalLink, Calendar, CheckCircle2, AlertOctagon, AlertTriangle, Eye, X } from 'lucide-react';
import { resolveImageUrl } from '../services/api';
import GradCAMViewer from './GradCAMViewer';

export default function HistoryTable({ records, onDeleteRecord, onFilterChange, activeFilter }) {
  const [selectedRecord, setSelectedRecord] = useState(null);

  return (
    <div>
      {/* Filter Tabs */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.25rem', flexWrap: 'wrap' }}>
        {[
          { id: 'all', label: 'All Records' },
          { id: 'genuine', label: 'Likely Genuine' },
          { id: 'fake', label: 'Suspected Fake / Churan' },
          { id: 'uncertain', label: 'Uncertain' },
        ].map(({ id, label }) => (
          <button
            key={id}
            className={`btn ${activeFilter === id ? 'btn-primary' : 'btn-secondary'}`}
            style={{ padding: '0.4rem 0.9rem', fontSize: '0.85rem' }}
            onClick={() => onFilterChange(id)}
          >
            {label}
          </button>
        ))}
      </div>

      {records.length === 0 ? (
        <div className="glass-card" style={{ textAlign: 'center', padding: '3rem 1.5rem' }}>
          <p style={{ color: 'var(--text-secondary)' }}>No screening records found matching this filter.</p>
        </div>
      ) : (
        <div className="glass-card" style={{ padding: 0, overflow: 'hidden' }}>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
              <thead>
                <tr style={{ background: 'rgba(0, 0, 0, 0.4)', borderBottom: '1px solid var(--border-color)' }}>
                  <th style={{ padding: '0.9rem 1rem' }}>Date & Time</th>
                  <th style={{ padding: '0.9rem 1rem' }}>Note Preview</th>
                  <th style={{ padding: '0.9rem 1rem' }}>Denomination</th>
                  <th style={{ padding: '0.9rem 1rem' }}>Authenticity</th>
                  <th style={{ padding: '0.9rem 1rem' }}>Confidence</th>
                  <th style={{ padding: '0.9rem 1rem' }}>Quality</th>
                  <th style={{ padding: '0.9rem 1rem', textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {records.map((rec) => {
                  const lowerAuth = (rec.authenticity || '').toLowerCase();
                  const isGenuine = lowerAuth.includes('genuine');
                  const isUncertain = lowerAuth.includes('uncertain') || lowerAuth.includes('inconclusive');
                  const badgeClass = isUncertain ? 'badge-warning' : (isGenuine ? 'badge-genuine' : 'badge-fake');
                  const Icon = isUncertain ? AlertTriangle : (isGenuine ? CheckCircle2 : AlertOctagon);
                  const formattedDate = rec.timestamp
                    ? new Date(rec.timestamp).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })
                    : 'Recent';

                  return (
                    <tr
                      key={rec.id}
                      style={{
                        borderBottom: '1px solid var(--border-color)',
                        transition: 'background 0.15s ease',
                      }}
                      onMouseEnter={(e) => (e.currentTarget.style.background = 'rgba(255, 255, 255, 0.02)')}
                      onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
                    >
                      <td style={{ padding: '0.9rem 1rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                        {formattedDate}
                      </td>

                      <td style={{ padding: '0.9rem 1rem' }}>
                        <img
                          src={resolveImageUrl(rec.original_image_url)}
                          alt="Thumbnail"
                          style={{
                            width: '56px',
                            height: '36px',
                            objectFit: 'cover',
                            borderRadius: '0.375rem',
                            border: '1px solid var(--border-color)',
                            background: '#000',
                          }}
                        />
                      </td>

                      <td style={{ padding: '0.9rem 1rem', fontWeight: 600, color: '#60a5fa' }}>
                        {rec.denomination}
                      </td>

                      <td style={{ padding: '0.9rem 1rem' }}>
                        <span className={`badge ${badgeClass}`}>
                          <Icon size={12} />
                          {rec.authenticity}
                        </span>
                      </td>

                      <td style={{ padding: '0.9rem 1rem', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                        {(rec.confidence * 100).toFixed(1)}%
                      </td>

                      <td style={{ padding: '0.9rem 1rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                        {rec.image_quality?.status || 'Good'}
                      </td>

                      <td style={{ padding: '0.9rem 1rem', textAlign: 'right' }}>
                        <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                          <button
                            onClick={() => setSelectedRecord(rec)}
                            style={{
                              background: 'rgba(59, 130, 246, 0.15)',
                              color: '#60a5fa',
                              border: 'none',
                              padding: '0.4rem 0.6rem',
                              borderRadius: '0.375rem',
                              cursor: 'pointer',
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '0.3rem',
                              fontSize: '0.8rem',
                            }}
                          >
                            <Eye size={14} /> View
                          </button>
                          <button
                            onClick={() => onDeleteRecord(rec.id)}
                            style={{
                              background: 'rgba(239, 68, 68, 0.15)',
                              color: '#f87171',
                              border: 'none',
                              padding: '0.4rem 0.6rem',
                              borderRadius: '0.375rem',
                              cursor: 'pointer',
                              display: 'inline-flex',
                              alignItems: 'center',
                              fontSize: '0.8rem',
                            }}
                          >
                            <Trash2 size={14} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Record Detail Modal */}
      {selectedRecord && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0, 0, 0, 0.75)',
            backdropFilter: 'blur(8px)',
            zIndex: 100,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '1.5rem',
          }}
        >
          <div
            className="glass-card"
            style={{
              maxWidth: '720px',
              width: '100%',
              maxHeight: '90vh',
              overflowY: 'auto',
              position: 'relative',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>
                Screening Audit Detail #{selectedRecord.id}
              </h3>
              <button
                onClick={() => setSelectedRecord(null)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--text-secondary)',
                  cursor: 'pointer',
                }}
              >
                <X size={22} />
              </button>
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
              <span className="badge badge-genuine" style={{ fontSize: '0.85rem' }}>
                Denomination: {selectedRecord.denomination}
              </span>
              {(() => {
                const modalAuth = (selectedRecord.authenticity || '').toLowerCase();
                const mUncertain = modalAuth.includes('uncertain') || modalAuth.includes('inconclusive');
                const mGenuine = modalAuth.includes('genuine');
                const mClass = mUncertain ? 'badge-warning' : (mGenuine ? 'badge-genuine' : 'badge-fake');
                return (
                  <span className={`badge ${mClass}`} style={{ fontSize: '0.85rem' }}>
                    {selectedRecord.authenticity} ({(selectedRecord.confidence * 100).toFixed(1)}%)
                  </span>
                );
              })()}
            </div>

            <GradCAMViewer
              originalImageUrl={selectedRecord.original_image_url}
              gradcamUrl={selectedRecord.gradcam_url}
            />

            <div style={{ marginTop: '1.5rem', textAlign: 'right' }}>
              <button className="btn btn-secondary" onClick={() => setSelectedRecord(null)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
