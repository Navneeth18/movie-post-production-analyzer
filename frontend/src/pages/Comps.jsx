import { COMP_FILMS } from '../utils/constants';

export default function Comps({ film }) {
  return (
    <div className="fade-up">
      <div className="page-header">
        <div className="page-title">Film <span>Comps</span> <span className="unique-badge">Unique</span></div>
        <div className="page-sub">Comparable films & performance benchmarks</div>
      </div>
      <div className="divider" />
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Comparable <span>Films</span> for "{film.title}"</div>
        <div style={{ display: "grid", gap: 16 }}>
          {COMP_FILMS.map((c, i) => (
            <div key={i} className="film-card" style={{ padding: 20 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
                <div>
                  <div style={{ fontFamily: "Cormorant Garamond", fontSize: 18, color: "#e8e0d0", fontWeight: 600, marginBottom: 4 }}>{c.title}</div>
                  <div style={{ fontSize: 10, color: "#666" }}>{c.genre} · {c.year}</div>
                </div>
                <div style={{ fontFamily: "Bebas Neue", fontSize: 32, color: "#4ade80" }}>{c.roi}</div>
              </div>
              <div className="grid-2" style={{ marginBottom: 12 }}>
                <div>
                  <div style={{ fontSize: 9, color: "#555", marginBottom: 4 }}>BUDGET</div>
                  <div style={{ fontSize: 11, color: "#e8e0d0" }}>{c.budget}</div>
                </div>
                <div>
                  <div style={{ fontSize: 9, color: "#555", marginBottom: 4 }}>COLLECTION</div>
                  <div style={{ fontSize: 11, color: "#e8e0d0" }}>{c.collection}</div>
                </div>
              </div>
              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: 9, color: "#555", marginBottom: 6 }}>STRATEGY</div>
                <div style={{ fontSize: 10, color: "#c9a84c" }}>{c.strategy}</div>
              </div>
              <div>
                <div style={{ fontSize: 9, color: "#555", marginBottom: 6 }}>KEYWORDS</div>
                {c.keywords.map(k => <span key={k} className="tag tag-gray">{k}</span>)}
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="card">
        <div className="card-title">Performance <span>Insights</span></div>
        <div style={{ fontSize: 11, color: "#aaa", padding: "20px 0" }}>
          Based on comparable films, your project has strong potential for a 3-5x ROI with the right distribution strategy.
        </div>
      </div>
    </div>
  );
}
