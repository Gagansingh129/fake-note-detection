import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  Home as HomeIcon, 
  Camera, 
  History as HistoryIcon, 
  Info, 
  Activity, 
  User as UserIcon, 
  LogOut, 
  LogIn 
} from 'lucide-react';
import { auth } from '../services/auth';
import { api } from '../services/api';

export default function Sidebar({ activePage, setActivePage, onOpenLogin }) {
  const [currentUser, setCurrentUser] = useState(auth.getCurrentUser());
  const [backendStatus, setBackendStatus] = useState('checking');

  useEffect(() => {
    const unsubscribe = auth.subscribe((user) => {
      setCurrentUser(user);
    });
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

  const handleLogout = async () => {
    await auth.logout();
  };

  const navItems = [
    { id: 'home', label: 'Home', icon: HomeIcon },
    { id: 'analyze', label: 'Analyze note', icon: Camera },
    { id: 'history', label: 'History', icon: HistoryIcon },
    { id: 'about', label: 'About', icon: Info },
  ];

  return (
    <aside
      style={{
        width: '260px',
        minWidth: '260px',
        background: '#0c1524',
        borderRight: '1px solid rgba(255, 255, 255, 0.08)',
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        position: 'sticky',
        top: 0,
        zIndex: 40,
        color: '#f8fafc',
        userSelect: 'none',
      }}
    >
      {/* Brand Header */}
      <div style={{ padding: '1.75rem 1.5rem 1.25rem' }}>
        <div 
          onClick={() => setActivePage('home')}
          style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', cursor: 'pointer' }}
        >
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '0.625rem',
              background: 'rgba(16, 185, 129, 0.15)',
              border: '1px solid rgba(16, 185, 129, 0.3)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <ShieldCheck size={22} color="#10b981" />
          </div>
          <div>
            <div style={{ fontSize: '1.15rem', fontWeight: 800, color: '#ffffff', letterSpacing: '-0.02em', lineHeight: 1.1 }}>
              NoteGuard AI
            </div>
          </div>
        </div>

        <div style={{ marginTop: '0.65rem' }}>
          <span
            style={{
              display: 'inline-block',
              fontSize: '0.68rem',
              fontWeight: 700,
              letterSpacing: '0.06em',
              textTransform: 'uppercase',
              color: '#38bdf8',
              background: 'rgba(56, 189, 248, 0.12)',
              border: '1px solid rgba(56, 189, 248, 0.25)',
              padding: '0.2rem 0.55rem',
              borderRadius: '9999px',
            }}
          >
            Academic Screening
          </span>
        </div>
      </div>

      {/* Navigation List */}
      <nav style={{ flex: 1, padding: '1rem 0.85rem', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activePage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActivePage(item.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.85rem',
                width: '100%',
                padding: '0.75rem 1rem',
                borderRadius: '0.625rem',
                border: 'none',
                background: isActive ? '#172338' : 'transparent',
                color: isActive ? '#38bdf8' : '#94a3b8',
                fontWeight: isActive ? 600 : 500,
                fontSize: '0.92rem',
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'all 0.15s ease',
              }}
              onMouseEnter={(e) => {
                if (!isActive) {
                  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.04)';
                  e.currentTarget.style.color = '#f1f5f9';
                }
              }}
              onMouseLeave={(e) => {
                if (!isActive) {
                  e.currentTarget.style.background = 'transparent';
                  e.currentTarget.style.color = '#94a3b8';
                }
              }}
            >
              <Icon size={19} color={isActive ? '#38bdf8' : '#64748b'} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Bottom Section */}
      <div
        style={{
          padding: '1.25rem 1.25rem 1.5rem',
          borderTop: '1px solid rgba(255, 255, 255, 0.08)',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem',
        }}
      >
        {/* User Profile Card */}
        {currentUser ? (
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              background: 'rgba(255, 255, 255, 0.04)',
              padding: '0.65rem 0.8rem',
              borderRadius: '0.625rem',
              border: '1px solid rgba(255, 255, 255, 0.06)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', overflow: 'hidden' }}>
              <div
                style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '9999px',
                  background: 'linear-gradient(135deg, #3b82f6, #06b6d4)',
                  color: '#ffffff',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: '0.8rem',
                  flexShrink: 0,
                }}
              >
                {(currentUser.full_name || currentUser.username || 'U')[0].toUpperCase()}
              </div>
              <div style={{ overflow: 'hidden' }}>
                <div style={{ fontSize: '0.82rem', fontWeight: 600, color: '#f8fafc', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {currentUser.full_name || currentUser.username}
                </div>
                <div style={{ fontSize: '0.7rem', color: '#64748b', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {currentUser.email}
                </div>
              </div>
            </div>

            <button
              onClick={handleLogout}
              title="Sign Out"
              style={{
                background: 'transparent',
                border: 'none',
                color: '#94a3b8',
                cursor: 'pointer',
                padding: '0.35rem',
                borderRadius: '0.375rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transition: 'color 0.15s',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.color = '#ef4444')}
              onMouseLeave={(e) => (e.currentTarget.style.color = '#94a3b8')}
            >
              <LogOut size={16} />
            </button>
          </div>
        ) : (
          <button
            onClick={onOpenLogin}
            style={{
              width: '100%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem',
              padding: '0.65rem 0.85rem',
              borderRadius: '0.625rem',
              background: 'rgba(56, 189, 248, 0.1)',
              border: '1px solid rgba(56, 189, 248, 0.25)',
              color: '#38bdf8',
              fontSize: '0.84rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.15s',
            }}
          >
            <LogIn size={15} />
            <span>Sign In / Demo</span>
          </button>
        )}

        {/* API Status Pill & Model Info */}
        <div>
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.45rem',
              fontSize: '0.75rem',
              color: backendStatus === 'online' ? '#34d399' : '#f87171',
              marginBottom: '0.35rem',
            }}
          >
            <span
              style={{
                width: '7px',
                height: '7px',
                borderRadius: '9999px',
                background: backendStatus === 'online' ? '#10b981' : '#ef4444',
                display: 'inline-block',
                boxShadow: backendStatus === 'online' ? '0 0 8px #10b981' : 'none',
              }}
            />
            <span style={{ fontWeight: 600 }}>{backendStatus === 'online' ? 'API online' : 'API offline'}</span>
          </div>

          <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '0.2rem' }}>
            Model
          </div>
          <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#e2e8f0', letterSpacing: '-0.01em' }}>
            EfficientNetB0 v2.1
          </div>
        </div>
      </div>
    </aside>
  );
}

