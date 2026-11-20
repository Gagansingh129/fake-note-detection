import React, { useState, useEffect } from 'react';
import { RotateCw, AlertCircle, Loader2 } from 'lucide-react';
import HistoryTable from '../components/HistoryTable';
import { api } from '../services/api';

export default function History() {
  const [records, setRecords] = useState([]);
  const [activeFilter, setActiveFilter] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchHistory = async (filter = activeFilter) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await api.getHistory(filter);
      setRecords(data.records || []);
    } catch (err) {
      console.error('[History Fetch Error]:', err);
      setError('Failed to load past screening records.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory(activeFilter);
  }, [activeFilter]);

  const handleDelete = async (recordId) => {
    if (!window.confirm(`Are you sure you want to delete screening record #${recordId}?`)) {
      return;
    }
    try {
      await api.deleteHistory(recordId);
      setRecords((prev) => prev.filter((r) => r.id !== recordId));
    } catch (err) {
      alert(`Could not delete record: ${err.message}`);
    }
  };

  const filterTabs = [
    { id: 'all', label: 'All records' },
    { id: 'genuine', label: 'Likely genuine' },
    { id: 'fake', label: 'Suspected fake' },
    { id: 'uncertain', label: 'Uncertain' },
  ];

  return (
    <div style={{ maxWidth: '1240px', margin: '0 auto' }}>
      {/* Header Bar matching Page 5 */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          flexWrap: 'wrap',
          gap: '1rem',
          marginBottom: '1.5rem',
        }}
      >
        <div>
          <h1
            style={{
              fontSize: '1.85rem',
              fontWeight: 800,
              color: '#0f172a',
              letterSpacing: '-0.02em',
              margin: 0,
            }}
          >
            Screening audit history
          </h1>
          <p style={{ color: '#64748b', fontSize: '0.92rem', marginTop: '0.3rem', margin: 0 }}>
            A chronological record of every analyzed banknote and its diagnostics.
          </p>
        </div>

        <button
          onClick={() => fetchHistory(activeFilter)}
          disabled={isLoading}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.45rem',
            padding: '0.5rem 0.95rem',
            borderRadius: '0.5rem',
            background: '#ffffff',
            border: '1px solid #e2e8f0',
            color: '#334155',
            fontSize: '0.85rem',
            fontWeight: 600,
            cursor: isLoading ? 'not-allowed' : 'pointer',
            boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
            transition: 'all 0.15s ease',
          }}
          onMouseEnter={(e) => {
            if (!isLoading) e.currentTarget.style.background = '#f8fafc';
          }}
          onMouseLeave={(e) => {
            if (!isLoading) e.currentTarget.style.background = '#ffffff';
          }}
        >
          <RotateCw size={14} className={isLoading ? 'pulse' : ''} />
          <span>Refresh records</span>
        </button>
      </div>

      {/* Filter Pills matching Page 5 */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
        {filterTabs.map(({ id, label }) => {
          const isActive = activeFilter === id;
          return (
            <button
              key={id}
              onClick={() => setActiveFilter(id)}
              style={{
                padding: '0.45rem 1rem',
                borderRadius: '9999px',
                fontSize: '0.84rem',
                fontWeight: 600,
                border: '1px solid transparent',
                background: isActive ? '#0f172a' : '#ffffff',
                color: isActive ? '#ffffff' : '#475569',
                borderColor: isActive ? '#0f172a' : '#e2e8f0',
                cursor: 'pointer',
                boxShadow: isActive ? '0 2px 4px rgba(15,23,42,0.15)' : '0 1px 2px rgba(0,0,0,0.04)',
                transition: 'all 0.15s ease',
              }}
              onMouseEnter={(e) => {
                if (!isActive) e.currentTarget.style.background = '#f1f5f9';
              }}
              onMouseLeave={(e) => {
                if (!isActive) e.currentTarget.style.background = '#ffffff';
              }}
            >
              {label}
            </button>
          );
        })}
      </div>

      {/* Content Area */}
      {isLoading ? (
        <div
          style={{
            background: '#ffffff',
            borderRadius: '0.75rem',
            border: '1px solid #e2e8f0',
            textAlign: 'center',
            padding: '4rem 1.5rem',
          }}
        >
          <Loader2 size={32} color="#2563eb" className="pulse" style={{ margin: '0 auto 0.75rem' }} />
          <p style={{ color: '#64748b', fontSize: '0.9rem' }}>Loading past screening audit records...</p>
        </div>
      ) : error ? (
        <div
          style={{
            background: '#ffffff',
            borderRadius: '0.75rem',
            border: '1px solid #fecaca',
            textAlign: 'center',
            padding: '3rem 1.5rem',
            color: '#dc2626',
          }}
        >
          <AlertCircle size={32} style={{ margin: '0 auto 0.5rem' }} />
          <p style={{ fontWeight: 600 }}>{error}</p>
        </div>
      ) : (
        <HistoryTable
          records={records}
          onDeleteRecord={handleDelete}
          onFilterChange={setActiveFilter}
          activeFilter={activeFilter}
        />
      )}
    </div>
  );
}
