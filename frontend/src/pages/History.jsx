import React, { useState, useEffect } from 'react';
import { History as HistoryIcon, RefreshCw, AlertCircle, Loader2 } from 'lucide-react';
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

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <HistoryIcon size={24} color="#3b82f6" /> Screening Audit History
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '0.2rem' }}>
            Chronological audit trail of analyzed banknotes and diagnostics stored in SQLite.
          </p>
        </div>

        <button className="btn btn-secondary" onClick={() => fetchHistory(activeFilter)} disabled={isLoading} style={{ fontSize: '0.85rem' }}>
          <RefreshCw size={14} className={isLoading ? 'pulse' : ''} /> Refresh Records
        </button>
      </div>

      {isLoading ? (
        <div className="glass-card" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
          <Loader2 size={32} color="#3b82f6" className="pulse" style={{ margin: '0 auto 0.75rem' }} />
          <p style={{ color: 'var(--text-secondary)' }}>Loading screening history...</p>
        </div>
      ) : error ? (
        <div className="glass-card" style={{ textAlign: 'center', padding: '3rem 1.5rem', color: '#f87171' }}>
          <AlertCircle size={32} style={{ margin: '0 auto 0.5rem' }} />
          <p>{error}</p>
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
