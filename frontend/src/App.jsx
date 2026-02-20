import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Audience from './pages/Audience';
import Campaign from './pages/Campaign';
import Distribution from './pages/Distribution';
import Festival from './pages/Festival';
import Release from './pages/Release';
import Comps from './pages/Comps';
import Advisor from './pages/Advisor';
import { useFilmStore } from './store/filmStore';
import './styles/global.css';

export default function App() {
  const { currentFilm, setCurrentFilm } = useFilmStore();
  const [notification, setNotification] = useState(null);

  const notify = (msg) => {
    setNotification(msg);
    setTimeout(() => setNotification(null), 3000);
  };

  return (
    <Router>
      {notification && <div className="notification">{notification}</div>}
      <div className="grain" />
      <div className="app">
        <Sidebar film={currentFilm} setFilm={setCurrentFilm} />
        <main className="main">
          <Routes>
            <Route path="/" element={<Dashboard film={currentFilm} />} />
            <Route path="/audience" element={<Audience film={currentFilm} />} />
            <Route path="/campaign" element={<Campaign film={currentFilm} />} />
            <Route path="/distribution" element={<Distribution film={currentFilm} />} />
            <Route path="/festival" element={<Festival film={currentFilm} notify={notify} />} />
            <Route path="/release" element={<Release film={currentFilm} />} />
            <Route path="/comps" element={<Comps film={currentFilm} />} />
            <Route path="/advisor" element={<Advisor film={currentFilm} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}