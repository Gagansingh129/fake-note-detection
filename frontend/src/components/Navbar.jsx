import React, { useState, useEffect } from 'react';
import { ShieldCheck, Camera, History, Info, Activity, Sparkles } from 'lucide-react';
import { api } from '../services/api';

export default function Navbar({ activePage, setActivePage }) {
  const [backendStatus, setBackendStatus] = useState('checking');

  useEffect(() => {
    let mounted = true;
    const verifyHealth = async () => {
      const res = await api.checkHealth();
      if (mounted) {
        setBackendStatus(res.status === 'healthy' ? 'online' : 'offline');
      }
    };
    verifyHealth();
    const interval = setInterval(verifyHealth, 15000);
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <div className="brand" onClick={() => setActivePage('home')}>
          <ShieldCheck size={28} color="#3b82f6" />
          <span>NoteGuard AI</span>
          <span className="brand-badge">Academic Screening</span>
        </div>

        <nav className="nav-links">
          <button
            className={`nav-btn ${activePage === 'home' ? 'active' : ''}`}
            onClick={() => setActivePage('home')}
          >
            <Sparkles size={16} /> Home
          </button>
          <button
            className={`nav-btn ${activePage === 'analyze' ? 'active' : ''}`}
            onClick={() => setActivePage('analyze')}
          >
            <Camera size={16} /> Analyze Note
          </button>
          <button
            className={`nav-btn ${activePage === 'history' ? 'active' : ''}`}
            onClick={() => setActivePage('history')}
          >
            <History size={16} /> History
          </button>
          <button
            className={`nav-btn ${activePage === 'about' ? 'active' : ''}`}
            onClick={() => setActivePage('about')}
          >
            <Info size={16} /> About
          </button>

          {/* Backend Status Pill */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              marginLeft: '0.75rem',
              fontSize: '0.75rem',
              padding: '0.25rem 0.6rem',
              borderRadius: '9999px',
              background: backendStatus === 'online' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
              color: backendStatus === 'online' ? '#10b981' : '#ef4444',
              border: `1px solid ${backendStatus === 'online' ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
            }}
          >
            <Activity size={12} className={backendStatus === 'online' ? 'pulse' : ''} />
            <span>{backendStatus === 'online' ? 'API Online' : 'API Offline'}</span>
          </div>
        </nav>
      </div>
    </header>
  );
}
