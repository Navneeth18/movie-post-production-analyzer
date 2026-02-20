import { Link, useLocation } from 'react-router-dom';
import { useFilmStore } from '../store/filmStore';

const NAV = [
  { id: "dashboard", path: "/", icon: "◈", label: "Overview" },
  { id: "audience", path: "/audience", icon: "⬡", label: "Audience DNA", unique: true },
  { id: "campaign", path: "/campaign", icon: "◎", label: "Campaign ROI" },
  { id: "distribution", path: "/distribution", icon: "⬢", label: "Distribution" },
  { id: "festival", path: "/festival", icon: "◆", label: "Festival Radar" },
  { id: "release", path: "/release", icon: "⊕", label: "Release Timing" },
  { id: "comps", path: "/comps", icon: "⊞", label: "Film Comps", unique: true },
  { id: "advisor", path: "/advisor", icon: "◉", label: "AI Advisor" },
];

export default function Sidebar() {
  const location = useLocation();
  const { currentFilm, films, setCurrentFilm } = useFilmStore();

  return (
    <aside className="sidebar">
      <div className="logo">
        <div className="logo-title">CINTEL</div>
        <div className="logo-sub">Film Intelligence Platform</div>
      </div>
      <nav className="nav">
        <div className="nav-section">Modules</div>
        {NAV.map(n => (
          <Link 
            key={n.id} 
            to={n.path}
            className={`nav-item ${location.pathname === n.path ? "active" : ""}`}
          >
            <span className="nav-icon">{n.icon}</span>
            <span>{n.label}</span>
            {n.unique && <span className="unique-badge" style={{ marginLeft: "auto", fontSize: "6px", padding: "1px 4px" }}>AI</span>}
          </Link>
        ))}
        <div className="nav-section" style={{ marginTop: 20 }}>Project</div>
        <div style={{ padding: "8px 20px" }}>
          <select value={currentFilm.title} onChange={e => setCurrentFilm(films.find(f => f.title === e.target.value))}>
            {films.map(f => <option key={f.title}>{f.title}</option>)}
          </select>
        </div>
        <div style={{ padding: "4px 20px 16px" }}>
          {[["Genre", currentFilm.genre], ["Budget", currentFilm.budget], ["Region", currentFilm.region]].map(([k, v]) => (
            <div key={k} style={{ display: "flex", justifyContent: "space-between", padding: "4px 0", borderBottom: "1px solid #141414" }}>
              <span style={{ fontSize: 9, color: "#444", letterSpacing: 1 }}>{k}</span>
              <span style={{ fontSize: 9, color: "#c9a84c", letterSpacing: 1 }}>{v}</span>
            </div>
          ))}
        </div>
      </nav>
    </aside>
  );
}
