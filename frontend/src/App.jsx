import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Home from './pages/Home';
import Analyze from './pages/Analyze';
import History from './pages/History';
import About from './pages/About';
import LoginModal from './components/LoginModal';

export default function App() {
  const [activePage, setActivePage] = useState('home');
  const [analyzeInitialMode, setAnalyzeInitialMode] = useState('upload');
  const [isLoginOpen, setIsLoginOpen] = useState(false);

  const handleNavigate = (page, mode = 'upload') => {
    setAnalyzeInitialMode(mode);
    setActivePage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Dual layout:
  // 1. Home landing page uses top sticky Navbar + full-width hero & sections (PDF Page 1)
  // 2. Application workspaces (Analyze, History, About) use left dark navy Sidebar + right light canvas (PDF Pages 2, 3, 4, 5)
  const isHomePage = activePage === 'home';

  return (
    <div className="app-root">
      {isHomePage ? (
        // --- Full-width Landing Page Layout (PDF Page 1) ---
        <div className="landing-layout">
          <Navbar 
            activePage={activePage} 
            setActivePage={setActivePage} 
            onOpenLogin={() => setIsLoginOpen(true)} 
          />

          <main className="landing-main">
            <Home onNavigate={handleNavigate} />
          </main>

          <footer
            style={{
              borderTop: '1px solid #e2e8f0',
              padding: '2rem 1.5rem',
              textAlign: 'center',
              fontSize: '0.85rem',
              color: '#64748b',
              background: '#ffffff',
            }}
          >
            <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
              <div style={{ fontWeight: 700, color: '#0f172a' }}>
                NoteGuard AI · Indian currency note authenticity detection system
              </div>
              <div style={{ marginTop: '0.35rem', fontSize: '0.8rem', color: '#94a3b8' }}>
                Academic computer vision project · TensorFlow 2.x · EfficientNetB0 · Grad-CAM · FastAPI · React + Vite
              </div>
            </div>
          </footer>
        </div>
      ) : (
        // --- Workspace Layout with Left Sidebar (PDF Pages 2, 3, 4, 5) ---
        <div className="workspace-layout">
          <Sidebar 
            activePage={activePage} 
            setActivePage={setActivePage} 
            onOpenLogin={() => setIsLoginOpen(true)} 
          />

          <main className="workspace-main">
            {activePage === 'analyze' && <Analyze initialMode={analyzeInitialMode} />}
            {activePage === 'history' && <History />}
            {activePage === 'about' && <About />}
          </main>
        </div>
      )}

      {/* User Login & Registration Modal */}
      <LoginModal 
        isOpen={isLoginOpen} 
        onClose={() => setIsLoginOpen(false)} 
      />
    </div>
  );
}
