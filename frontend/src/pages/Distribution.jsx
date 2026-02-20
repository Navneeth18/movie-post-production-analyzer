import { useState } from 'react';
import { callAI } from '../utils/aiHelper';
import { PLATFORM_SCORES } from '../utils/constants';

export default function Distribution({ film }) {
  const [aiLoading, setAiLoading] = useState(false);
  const [aiResult, setAiResult] = useState("");

  const platformsForGenre = PLATFORM_SCORES[film.genre] || PLATFORM_SCORES["Drama"];

  const runAI = async () => {
    setAiLoading(true);
    setAiResult("");
    const prompt = `For "${film.title}" (${film.genre}, Budget: ${film.budget}), generate 5 specific negotiation talking points a producer should use when approaching a streaming platform. Include leverage points, realistic deal terms, and red lines to avoid.`;
    const result = await callAI(prompt);
    setAiResult(result);
    setAiLoading(false);
  };

  return (
    <div className="fade-up">
      <div className="page-header">
        <div className="page-title">Distribution <span>Intelligence</span></div>
        <div className="page-sub">Platform matching & deal simulator</div>
      </div>
      <div className="divider" />
      <div className="grid-2">
        <div className="card">
          <div className="card-title">Platform <span>Match Scores</span></div>
          {platformsForGenre.map((p, i) => (
            <div key={i} className="platform-score">
              <div>
                <div className="platform-name">{p.name}</div>
                <div style={{ fontSize: 9, color: "#555", marginTop: 2 }}>{p.window}</div>
                <div className="progress-bar" style={{ marginTop: 6, width: 160 }}>
                  <div className={`progress-fill ${p.score > 80 ? "green" : ""}`} style={{ width: `${p.score}%` }} />
                </div>
              </div>
              <div>
                <div className={`score-badge ${p.score > 80 ? "score-high" : p.score > 65 ? "score-mid" : "score-low"}`}>{p.score}</div>
                <div style={{ fontSize: 8, color: "#555", textAlign: "right" }}>{p.deal}</div>
              </div>
            </div>
          ))}
        </div>
        <div className="card">
          <div className="card-title">Deal <span>Simulation</span> & Negotiation Points</div>
          <div style={{ marginBottom: 16 }}>
            <label>Select Platform</label>
            <select>
              {platformsForGenre.map(p => <option key={p.name}>{p.name}</option>)}
            </select>
          </div>
          <div style={{ marginBottom: 16 }}>
            <label>Revenue Model Preference</label>
            <select>
              <option>Flat Fee (Licensing)</option>
              <option>Revenue Share (60/40)</option>
              <option>Hybrid (Advance + Royalty)</option>
              <option>Day-and-Date Co-release</option>
            </select>
          </div>
          <button className="btn btn-gold" style={{ marginBottom: 16 }} onClick={runAI}>Simulate Negotiation</button>
          {(aiLoading || aiResult) && <div className="ai-box"><div className="ai-text">{aiLoading ? <span className="loading-dots">Simulating</span> : aiResult}</div></div>}
        </div>
      </div>
      <div className="card" style={{ marginTop: 20 }}>
        <div className="card-title">Distribution <span>Strategy</span> Paths</div>
        <div className="grid-3">
          {[
            { path: "Festival → OTT", risk: "Low", roi: "High", time: "12–18 months", desc: "Build critical acclaim and awards momentum, then approach OTTs with validated content. Best for art-house and drama.", recommended: film.genre === "Drama" },
            { path: "Theatrical → OTT", risk: "Medium", roi: "Highest", time: "8–12 months", desc: "Traditional path with theatrical window. Requires marketing investment upfront but maximizes total revenue.", recommended: film.genre === "Thriller" },
            { path: "Direct OTT", risk: "Low", roi: "Medium", time: "3–6 months", desc: "Skip theatrical entirely. Best for limited-budget films where marketing spends can't justify multiplex competition.", recommended: false },
          ].map((s, i) => (
            <div key={i} className={`card ${s.recommended ? "film-card selected" : "film-card"}`} style={{ background: "#0a0a0a" }}>
              {s.recommended && <div className="badge">Recommended</div>}
              <div style={{ fontFamily: "Cormorant Garamond", fontSize: 18, color: "#e8e0d0", marginBottom: 8, marginTop: s.recommended ? 8 : 0 }}>{s.path}</div>
              <div style={{ fontSize: 10, color: "#aaa", marginBottom: 12, lineHeight: 1.6 }}>{s.desc}</div>
              {[["Risk", s.risk], ["ROI Potential", s.roi], ["Timeline", s.time]].map(([k, v]) => (
                <div key={k} style={{ display: "flex", justifyContent: "space-between", padding: "4px 0", borderBottom: "1px solid #141414" }}>
                  <span style={{ fontSize: 9, color: "#555" }}>{k}</span>
                  <span style={{ fontSize: 9, color: v === "High" || v === "Highest" || v === "Low" ? "#4ade80" : "#c9a84c" }}>{v}</span>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
