import React, { useState, useEffect } from 'react';
import { ShieldCheck, Activity, User as UserIcon, LogOut, LogIn, ArrowRight } from 'lucide-react';
import { api } from '../services/api';
import { auth } from '../services/auth';

export default function Navbar({ activePage, setActivePage, onOpenLogin }) {
  const [backendStatus, setBackendStatus] = useState('checking');
  const [currentUser, setCurrentUser] = useState(auth.getCurrentUser());

  useEffect(() => {
    const unsubscribe = auth.subscribe(setCurrentUser);
    auth.fetchCurrentUser().then(setCurrentUser);

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
      unsubscribe();
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <header
      style={{
        position: 'sticky',
        top: 0,
        zIndex: 50,
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(12px)',
        borderBottom: '1px solid #e2e8f0',
      }}
    >
      <div
        style={{
          maxWidth: '1240px',
          margin: '0 auto',
          padding: '0.85rem 1.5rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        {/* Brand */}
        <div
          onClick={() => setActivePage('home')}
          style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', cursor: 'pointer' }}
        >
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '0.625rem',
              background: '#ecfdf5',
              border: '1px solid #a7f3d0',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <ShieldCheck size={22} color="#10b981" />
          </div>
          <span style={{ fontSize: '1.2rem', fontWeight: 800, color: '#0f172a', letterSpacing: '-0.02em' }}>
            NoteGuard AI
          </span>
          <span
            style={{
              fontSize: '0.68rem',
              fontWeight: 700,
              letterSpacing: '0.05em',
              textTransform: 'uppercase',
              color: '#2563eb',
              background: '#eff6ff',
              border: '1px solid #bfdbfe',
              padding: '0.2rem 0.55rem',
              borderRadius: '9999px',
            }}
          >
            Academic Screening
          </span>
        </div>

        {/* Center Nav Links */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
          {[
            { id: 'home', label: 'Home' },
            { id: 'analyze', label: 'Analyze Note' },
            { id: 'history', label: 'History' },
            { id: 'about', label: 'About' },
          ].map((item) => {
            const isActive = activePage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActivePage(item.id)}
                style={{
                  padding: '0.45rem 0.95rem',
                  borderRadius: '9999px',
                  border: 'none',
                  background: isActive ? '#e2e8f0' : 'transparent',
                  color: isActive ? '#0f172a' : '#475569',
                  fontWeight: isActive ? 700 : 500,
                  fontSize: '0.88rem',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                }}
                onMouseEnter={(e) => {
                  if (!isActive) e.currentTarget.style.background = '#f1f5f9';
                }}
                onMouseLeave={(e) => {
                  if (!isActive) e.currentTarget.style.background = 'transparent';
                }}
              >
                {item.label}
              </button>
            );
          })}
        </nav>

        {/* Right Actions: API Status + User Auth + CTA */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          {/* API Status Pill */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.45rem',
              fontSize: '0.78rem',
              fontWeight: 600,
              padding: '0.3rem 0.75rem',
              borderRadius: '9999px',
              background: '#ffffff',
              color: backendStatus === 'online' ? '#059669' : '#dc2626',
              border: '1px solid #e2e8f0',
              boxShadow: '0 1px 2px rgba(0,0,0,0.04)',
            }}
          >
            <span
              style={{
                width: '7px',
                height: '7px',
                borderRadius: '9999px',
                background: backendStatus === 'online' ? '#10b981' : '#ef4444',
                display: 'inline-block',
                boxShadow: backendStatus === 'online' ? '0 0 6px #10b981' : 'none',
              }}
            />
            <span>{backendStatus === 'online' ? 'API online' : 'API offline'}</span>
          </div>

          {/* User Auth Button */}
          {currentUser ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem',
                  background: '#f8fafc',
                  border: '1px solid #e2e8f0',
                  padding: '0.3rem 0.65rem',
                  borderRadius: '9999px',
                  fontSize: '0.82rem',
                  fontWeight: 600,
                  color: '#334155',
                }}
              >
                <div
                  style={{
                    width: '24px',
                    height: '24px',
                    borderRadius: '9999px',
                    background: '#2563eb',
                    color: '#ffffff',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '0.72rem',
                    fontWeight: 700,
                  }}
                >
                  {(currentUser.full_name || currentUser.username || 'U')[0].toUpperCase()}
                </div>
                <span>{currentUser.username}</span>
              </div>
              <button
                onClick={() => auth.logout()}
                title="Sign Out"
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: '#64748b',
                  cursor: 'pointer',
                  padding: '0.35rem',
                  borderRadius: '9999px',
                }}
              >
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <button
              onClick={onOpenLogin}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.4rem',
                padding: '0.45rem 0.85rem',
                borderRadius: '9999px',
                background: '#ffffff',
                border: '1px solid #cbd5e1',
                color: '#334155',
                fontSize: '0.84rem',
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.15s',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = '#f8fafc')}
              onMouseLeave={(e) => (e.currentTarget.style.background = '#ffffff')}
            >
              <LogIn size={15} />
              <span>Sign in</span>
            </button>
          )}

          {/* Primary CTA */}
          <button
            onClick={() => setActivePage('analyze')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.45rem',
              padding: '0.5rem 1.15rem',
              borderRadius: '9999px',
              background: '#0f172a',
              color: '#ffffff',
              border: 'none',
              fontSize: '0.88rem',
              fontWeight: 600,
              cursor: 'pointer',
              boxShadow: '0 2px 4px rgba(15, 23, 42, 0.15)',
              transition: 'all 0.15s ease',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.background = '#1e293b')}
            onMouseLeave={(e) => (e.currentTarget.style.background = '#0f172a')}
          >
            <span>Analyze note</span>
          </button>
        </div>
      </div>
    </header>
  );
}
