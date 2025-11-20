import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ReportPage from './pages/ReportPage';
import TrackPage from './pages/TrackPage';
import DashboardPage from './pages/DashboardPage';
import VerifyPage from './pages/VerifyPage';
import './App.css';

function App() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [language, setLanguage] = useState('en');

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const translations = {
    en: {
      appName: 'CitiTrack',
      tagline: 'Municipal Service Tracking',
      report: 'Report Issue',
      track: 'Track Ticket',
      dashboard: 'Dashboard',
      verify: 'Verify',
      offline: 'You are offline. Reports will be queued.',
      online: 'Connected'
    },
    zu: {
      appName: 'CitiTrack',
      tagline: 'Ukulandelela Kwezinsizakalo',
      report: 'Bika Inkinga',
      track: 'Landelela Ithikithi',
      dashboard: 'Ibhodi',
      verify: 'Qinisekisa',
      offline: 'Awukaxhunyiwe. Imibiko izofakwa emgqeni.',
      online: 'Kuxhunyiwe'
    },
    st: {
      appName: 'CitiTrack',
      tagline: 'Tlhahlobo ea Litšebeletso',
      report: 'Tlaleha Bothata',
      track: 'Latela Tekete',
      dashboard: 'Boto',
      verify: 'Netefatsa',
      offline: 'Ha o na le inthanete. Litlaleho li tla beoa moleng.',
      online: 'E hokahantsoe'
    },
    af: {
      appName: 'CitiTrack',
      tagline: 'Munisipale Dienste Opsporing',
      report: 'Rapporteer Probleem',
      track: 'Volg Kaartjie',
      dashboard: 'Dashboard',
      verify: 'Verifieer',
      offline: 'Jy is vanlyn. Verslae sal in die ry geplaas word.',
      online: 'Gekoppel'
    }
  };

  const t = translations[language];

  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <div className="header-content">
            <div className="logo-section">
              <h1>{t.appName}</h1>
              <p className="tagline">{t.tagline}</p>
            </div>
            
            <nav className="main-nav">
              <Link to="/" className="nav-link">{t.report}</Link>
              <Link to="/track" className="nav-link">{t.track}</Link>
              <Link to="/dashboard" className="nav-link">{t.dashboard}</Link>
              <Link to="/verify" className="nav-link">{t.verify}</Link>
            </nav>

            <div className="header-controls">
              <select 
                value={language} 
                onChange={(e) => setLanguage(e.target.value)}
                className="language-selector"
              >
                <option value="en">English</option>
                <option value="zu">isiZulu</option>
                <option value="st">Sesotho</option>
                <option value="af">Afrikaans</option>
              </select>

              <div className={`status-indicator ${isOnline ? 'online' : 'offline'}`}>
                <span className="status-dot"></span>
                <span className="status-text">
                  {isOnline ? t.online : t.offline}
                </span>
              </div>
            </div>
          </div>
        </header>

        <main className="app-main">
          <Routes>
            <Route path="/" element={<ReportPage language={language} isOnline={isOnline} />} />
            <Route path="/track" element={<TrackPage language={language} />} />
            <Route path="/dashboard" element={<DashboardPage language={language} />} />
            <Route path="/verify" element={<VerifyPage language={language} />} />
          </Routes>
        </main>

        <footer className="app-footer">
          <p>© 2024 CitiTrack | Empowering Communities Through Transparency</p>
          <p className="footer-tech">AI-Powered • Blockchain-Verified • Offline-Capable</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;