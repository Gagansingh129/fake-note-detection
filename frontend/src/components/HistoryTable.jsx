import React, { useState } from 'react';
import { 
  Trash2, 
  Eye, 
  Check, 
  AlertTriangle, 
  HelpCircle, 
  X, 
  ChevronLeft, 
  ChevronRight,
  ShieldCheck,
  FileText
} from 'lucide-react';
import { resolveImageUrl } from '../services/api';
import PredictionResult from './PredictionResult';

// Banknote Thumbnail Generator matching PDF Page 5
function BanknoteThumbnail({ denomination, imageUrl }) {
  if (imageUrl) {
    return (
      <img
        src={resolveImageUrl(imageUrl)}
        alt={`₹${denomination}`}
        style={{
          width: '52px',
          height: '30px',
          objectFit: 'cover',
          borderRadius: '4px',
          border: '1px solid #cbd5e1',
          boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
          background: '#f1f5f9',
          display: 'block',
        }}
        onError={(e) => {
          e.currentTarget.style.display = 'none';
        }}
      />
    );
  }

  // Color schemes matching Indian currency denominations in PDF Page 5
  const colorMap = {
    '10': { bg: '#c8a27a', border: '#a57c52', text: '#543d23' },    // Chocolate Brown
    '20': { bg: '#a3c48f', border: '#7e9f6c', text: '#3c5a2c' },    // Greenish Yellow
    '50': { bg: '#7cc0d8', border: '#5ba2bc', text: '#215264' },    // Fluorescent Blue
    '100': { bg: '#a5b4fc', border: '#818cf8', text: '#3730a3' },   // Lavender
    '200': { bg: '#fbbf24', border: '#d97706', text: '#78350f' },   // Bright Yellow
    '500': { bg: '#cbd5e1', border: '#94a3b8', text: '#334155' },   // Stone Grey
    '2000': { bg: '#f472b6', border: '#db2777', text: '#831843' },  // Magenta
  };

  const denomStr = String(denomination || '10').replace(/[^0-9]/g, '');
  const colors = colorMap[denomStr] || { bg: '#cbd5e1', border: '#94a3b8', text: '#334155' };

  return (
    <div
      style={{
        width: '52px',
        height: '30px',
        borderRadius: '4px',
        background: colors.bg,
        border: `1.5px solid ${colors.border}`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 4px',
        boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          width: '12px',
          height: '12px',
          borderRadius: '9999px',
          background: 'rgba(0,0,0,0.12)',
        }}
      />
      <div
        style={{
          width: '2px',
          height: '100%',
          background: 'rgba(0,0,0,0.15)',
        }}
      />
      <div
        style={{
          fontSize: '0.62rem',
          fontWeight: 800,
          color: colors.text,
          letterSpacing: '-0.02em',
        }}
      >
        ₹{denomStr || '10'}
      </div>
    </div>
  );
}

export default function HistoryTable({ records, onDeleteRecord, onFilterChange, activeFilter }) {
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;

  // Pagination calculation
  const totalPages = Math.ceil(records.length / pageSize) || 1;
  const startIndex = (currentPage - 1) * pageSize;
  const paginatedRecords = records.slice(startIndex, startIndex + pageSize);

  const formatDateTime = (timestamp) => {
    if (!timestamp) return '2 Nov, 6:34 AM';
    try {
      const date = new Date(timestamp);
      return date.toLocaleDateString('en-GB', {
        day: 'numeric',
        month: 'short',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
      });
    } catch {
      return '2 Nov, 6:34 AM';
    }
  };

  return (
    <div>
      {/* Table Container Card (Page 5 design) */}
      <div
        style={{
          background: '#ffffff',
          borderRadius: '0.75rem',
          border: '1px solid #e2e8f0',
          boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.05)',
          overflow: 'hidden',
        }}
      >
        {records.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '4rem 1.5rem', color: '#64748b' }}>
            <FileText size={40} color="#cbd5e1" style={{ margin: '0 auto 0.75rem' }} />
            <div style={{ fontSize: '1rem', fontWeight: 600, color: '#334155' }}>No screening records found</div>
            <p style={{ fontSize: '0.85rem', marginTop: '0.25rem' }}>
              Run a note scan from the Analyze tab to generate audit records.
            </p>
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #e2e8f0', background: '#ffffff' }}>
                  <th style={{ padding: '0.9rem 1.25rem', fontSize: '0.75rem', fontWeight: 600, color: '#64748b', textTransform: 'none' }}>
                    Date and time
                  </th>
                  <th style={{ padding: '0.9rem 1.25rem', fontSize: '0.75rem', fontWeight: 600, color: '#64748b', textTransform: 'none' }}>
                    Note
                  </th>
                  <th style={{ padding: '0.9rem 1.25rem', fontSize: '0.75rem', fontWeight: 600, color: '#64748b', textTransform: 'none' }}>
                    Denomination
                  </th>
                  <th style={{ padding: '0.9rem 1.25rem', fontSize: '0.75rem', fontWeight: 600, color: '#64748b', textTransform: 'none' }}>
                    Authenticity
                  </th>
                  <th style={{ padding: '0.9rem 1.25rem', fontSize: '0.75rem', fontWeight: 600, color: '#64748b', textTransform: 'none' }}>
                    Confidence
                  </th>
                  <th style={{ padding: '0.9rem 1.25rem', fontSize: '0.75rem', fontWeight: 600, color: '#64748b', textTransform: 'none' }}>
                    Quality
                  </th>
                  <th style={{ padding: '0.9rem 1.25rem', fontSize: '0.75rem', fontWeight: 600, color: '#64748b', textTransform: 'none', textAlign: 'right' }}>
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {paginatedRecords.map((rec) => {
                  const lowerAuth = (rec.authenticity || '').toLowerCase();
                  const isGenuine = lowerAuth.includes('genuine');
                  const isFake = lowerAuth.includes('fake') || lowerAuth.includes('counterfeit');
                  const isUncertain = !isGenuine && !isFake;

                  const confVal = Math.round((rec.confidence ?? 0.98) * 1000) / 10;
                  const confWidth = Math.min(Math.max(confVal, 10), 100);

                  // Colors matching PDF Page 5
                  let pillBg = '#ecfdf5';
                  let pillBorder = '#a7f3d0';
                  let pillText = '#047857';
                  let barColor = '#059669';
                  let statusText = 'Likely genuine';
                  let StatusIcon = Check;

                  if (isFake) {
                    pillBg = '#fee2e2';
                    pillBorder = '#fecaca';
                    pillText = '#b91c1c';
                    barColor = '#dc2626';
                    statusText = 'Suspected fake';
                    StatusIcon = AlertTriangle;
                  } else if (isUncertain) {
                    pillBg = '#fef3c7';
                    pillBorder = '#fde68a';
                    pillText = '#b45309';
                    barColor = '#d97706';
                    statusText = 'Uncertain';
                    StatusIcon = HelpCircle;
                  }

                  const quality = rec.image_quality?.status || 'Good';
                  const isQualityGood = quality.toLowerCase() === 'good';

                  const denomDisplay = String(rec.denomination || '10').startsWith('₹') 
                    ? rec.denomination 
                    : `₹${rec.denomination || '10'}`;

                  return (
                    <tr
                      key={rec.id}
                      style={{
                        borderBottom: '1px solid #f1f5f9',
                        transition: 'background 0.15s ease',
                      }}
                      onMouseEnter={(e) => (e.currentTarget.style.background = '#f8fafc')}
                      onMouseLeave={(e) => (e.currentTarget.style.background = '#ffffff')}
                    >
                      {/* Date & Time */}
                      <td style={{ padding: '0.9rem 1.25rem', fontSize: '0.85rem', color: '#475569', whiteSpace: 'nowrap' }}>
                        {formatDateTime(rec.timestamp)}
                      </td>

                      {/* Note Thumbnail */}
                      <td style={{ padding: '0.9rem 1.25rem' }}>
                        <BanknoteThumbnail
                          denomination={rec.denomination}
                          imageUrl={rec.original_image_url}
                        />
                      </td>

                      {/* Denomination (Bold Blue) */}
                      <td style={{ padding: '0.9rem 1.25rem', fontWeight: 800, color: '#2563eb', fontSize: '0.95rem' }}>
                        {denomDisplay}
                      </td>

                      {/* Authenticity Pill */}
                      <td style={{ padding: '0.9rem 1.25rem' }}>
                        <span
                          style={{
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '0.35rem',
                            padding: '0.22rem 0.65rem',
                            borderRadius: '9999px',
                            background: pillBg,
                            border: `1px solid ${pillBorder}`,
                            color: pillText,
                            fontSize: '0.78rem',
                            fontWeight: 600,
                            whiteSpace: 'nowrap',
                          }}
                        >
                          <StatusIcon size={12} strokeWidth={2.5} />
                          {statusText}
                        </span>
                      </td>

                      {/* Confidence Bar + Percentage */}
                      <td style={{ padding: '0.9rem 1.25rem', whiteSpace: 'nowrap' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                          <div
                            style={{
                              width: '72px',
                              height: '6px',
                              background: '#e2e8f0',
                              borderRadius: '9999px',
                              overflow: 'hidden',
                            }}
                          >
                            <div
                              style={{
                                width: `${confWidth}%`,
                                height: '100%',
                                background: barColor,
                                borderRadius: '9999px',
                              }}
                            />
                          </div>
                          <span style={{ fontSize: '0.82rem', fontWeight: 700, color: '#0f172a', fontFamily: 'var(--font-mono)' }}>
                            {confVal.toFixed(1)}%
                          </span>
                        </div>
                      </td>

                      {/* Quality */}
                      <td style={{ padding: '0.9rem 1.25rem', fontSize: '0.82rem', color: '#334155', whiteSpace: 'nowrap' }}>
                        <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.45rem' }}>
                          <span
                            style={{
                              width: '7px',
                              height: '7px',
                              borderRadius: '9999px',
                              background: isQualityGood ? '#10b981' : '#f59e0b',
                              display: 'inline-block',
                            }}
                          />
                          {quality}
                        </span>
                      </td>

                      {/* Actions */}
                      <td style={{ padding: '0.9rem 1.25rem', textAlign: 'right', whiteSpace: 'nowrap' }}>
                        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}>
                          <button
                            onClick={() => setSelectedRecord(rec)}
                            style={{
                              padding: '0.25rem 0.75rem',
                              borderRadius: '0.375rem',
                              background: '#eff6ff',
                              border: '1px solid #bfdbfe',
                              color: '#2563eb',
                              fontSize: '0.78rem',
                              fontWeight: 600,
                              cursor: 'pointer',
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '0.25rem',
                              transition: 'all 0.15s ease',
                            }}
                            onMouseEnter={(e) => {
                              e.currentTarget.style.background = '#dbeafe';
                            }}
                            onMouseLeave={(e) => {
                              e.currentTarget.style.background = '#eff6ff';
                            }}
                          >
                            View
                          </button>

                          <button
                            onClick={() => onDeleteRecord(rec.id)}
                            title="Delete Record"
                            style={{
                              padding: '0.3rem',
                              borderRadius: '0.375rem',
                              background: 'transparent',
                              border: 'none',
                              color: '#f87171',
                              cursor: 'pointer',
                              display: 'inline-flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              transition: 'all 0.15s ease',
                            }}
                            onMouseEnter={(e) => {
                              e.currentTarget.style.color = '#ef4444';
                              e.currentTarget.style.background = '#fee2e2';
                            }}
                            onMouseLeave={(e) => {
                              e.currentTarget.style.color = '#f87171';
                              e.currentTarget.style.background = 'transparent';
                            }}
                          >
                            <Trash2 size={15} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination Footer (Page 5 design) */}
        {records.length > 0 && (
          <div
            style={{
              padding: '0.85rem 1.25rem',
              borderTop: '1px solid #e2e8f0',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              background: '#ffffff',
              fontSize: '0.82rem',
              color: '#64748b',
              flexWrap: 'wrap',
              gap: '0.75rem',
            }}
          >
            <div>
              Showing {Math.min(paginatedRecords.length, pageSize)} most recent records
              {records.length > pageSize && ` (Page ${currentPage} of ${totalPages})`}
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <button
                disabled={currentPage <= 1}
                onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                style={{
                  padding: '0.35rem 0.75rem',
                  borderRadius: '0.375rem',
                  background: '#ffffff',
                  border: '1px solid #cbd5e1',
                  color: currentPage <= 1 ? '#94a3b8' : '#0f172a',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  cursor: currentPage <= 1 ? 'not-allowed' : 'pointer',
                  opacity: currentPage <= 1 ? 0.6 : 1,
                }}
              >
                Previous
              </button>

              <button
                disabled={currentPage >= totalPages}
                onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                style={{
                  padding: '0.35rem 0.75rem',
                  borderRadius: '0.375rem',
                  background: '#ffffff',
                  border: '1px solid #cbd5e1',
                  color: currentPage >= totalPages ? '#94a3b8' : '#0f172a',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  cursor: currentPage >= totalPages ? 'not-allowed' : 'pointer',
                  opacity: currentPage >= totalPages ? 0.6 : 1,
                }}
              >
                Next
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Record View Modal */}
      {selectedRecord && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(15, 23, 42, 0.75)',
            backdropFilter: 'blur(8px)',
            zIndex: 100,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '1.5rem',
            overflowY: 'auto',
          }}
          onClick={() => setSelectedRecord(null)}
        >
          <div
            style={{
              background: '#f8fafc',
              borderRadius: '1rem',
              width: '100%',
              maxWidth: '960px',
              maxHeight: '90vh',
              overflowY: 'auto',
              border: '1px solid #e2e8f0',
              boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
              padding: '2rem',
              position: 'relative',
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <ShieldCheck size={22} color="#2563eb" />
                <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#0f172a', margin: 0 }}>
                  Audit Record #{selectedRecord.id}
                </h3>
              </div>
              <button
                onClick={() => setSelectedRecord(null)}
                style={{
                  background: '#f1f5f9',
                  border: 'none',
                  borderRadius: '9999px',
                  width: '32px',
                  height: '32px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: 'pointer',
                  color: '#475569',
                }}
              >
                <X size={18} />
              </button>
            </div>

            <PredictionResult
              result={selectedRecord}
              onReset={() => setSelectedRecord(null)}
            />
          </div>
        </div>
      )}
    </div>
  );
}
