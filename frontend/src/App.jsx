import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Analyze from './pages/Analyze';
import History from './pages/History';
import About from './pages/About';

export default function App() {
  const [activePage, setActivePage] = useState('home');
  const [analyzeInitialMode, setAnalyzeInitialMode] = useState('upload');

  const handleNavigate = (page, mode = 'upload') => {
    setAnalyzeInitialMode(mode);
    setActivePage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="app-container">
      <Navbar activePage={activePage} setActivePage={setActivePage} />

      <main className="main-content">
        {activePage === 'home' && <Home onNavigate={handleNavigate} />}
        {activePage === 'analyze' && <Analyze initialMode={analyzeInitialMode} />}
        {activePage === 'history' && <History />}
        {activePage === 'about' && <About />}
      </main>

      <footer
        style={{
          borderTop: '1px solid var(--border-color)',
          padding: '1.75rem 1.5rem',
          textAlign: 'center',
          fontSize: '0.85rem',
          color: 'var(--text-muted)',
          background: 'rgba(11, 15, 25, 0.95)',
        }}
      >
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <strong>NoteGuard AI</strong> — Indian Currency Note Authenticity Detection System
          <div style={{ marginTop: '0.4rem', fontSize: '0.78rem' }}>
            Academic Computer Vision Project • TensorFlow 2.x • EfficientNetB0 • Grad-CAM • FastAPI • React + Vite
          </div>
        </div>
      </footer>
    </div>
  );
}
