import { useState } from 'react';
import { callAI } from '../utils/aiHelper';
import { AUDIENCE_DATA } from '../utils/constants';

export default function Audience({ film }) {
  const [audienceTab, setAudienceTab] = useState("profile");
  const [aiLoading, setAiLoading] = useState(false);
  const [aiResult, setAiResult] = useState("");

  const audienceForGenre = AUDIENCE_DATA[film.genre] || AUDIENCE_DATA["Drama"];
  const dna = audienceForGenre.dna;

  const radarPath = (values) => {
    const points = values.map((v, i) => {
      const angle = (Math.PI * 2 * i) / values.length - Math.PI / 2;
      const r = (v / 100) * 55;
      return `${70 + r * Math.cos(angle)},${70 + r * Math.sin(angle)}`;
    });
    return `M${points.join("L")}Z`;
  };

  const radarAxes = (values) => {
    const labels = ["Emotion", "Action", "Visual", "Story", "Comedy", "Drama"];
    return values.map((v, i) => {
      const angle = (Math.PI * 2 * i) / values.length - Math.PI / 2;
      return {
        x1: 70, y1: 70,
        x2: 70 + 55 * Math.cos(angle),
        y2: 70 + 55 * Math.sin(angle),
        lx: 70 + 68 * Math.cos(angle),
        ly: 70 + 68 * Math.sin(angle),
        label: labels[i]
      };
    });
  };

  const runAI = async () => {
    setAiLoading(true);
    setAiResult("");
    const prompt = `Analyze the ideal audience for a ${film.genre} film titled "${film.title}" with themes: ${film.themes}. Give psychographic insights, consumption habits, and 3 specific ways to reach them.`;
    const result = await callAI(prompt);
    setAiResult(result);
    setAiLoading(false);
  };

  return (
    <div className="fade-up">
      <div className="page-header">
        <div className="page-title">Audience <span>DNA</span> Profiler <span className="unique-badge">Unique</span></div>
        <div className="page-sub">Psychographic mapping — {film.title}</div>
      </div>
      <div className="divider" />
      <div className="tab-row">
        {["profile", "segments", "behavior"].map(t => <div key={t} className={`tab ${audienceTab === t ? "active" : ""}`} onClick={() => setAudienceTab(t)}>{t}</div>)}
      </div>
      {audienceTab === "profile" && (
        <div className="grid-2">
          <div className="card">
            <div className="card-title">Film <span>DNA Radar</span></div>
            <svg className="radar" viewBox="0 0 140 140">
              {[0.25, 0.5, 0.75, 1].map(r => (
                <polygon key={r} points={radarAxes(dna).map(a => {
                  const ang = Math.atan2(a.y2 - 70, a.x2 - 70);
                  const rr = r * 55;
                  return `${70 + rr * Math.cos(ang)},${70 + rr * Math.sin(ang)}`;
                }).join(" ")} fill="none" stroke="#1a1a1a" strokeWidth="1" />
              ))}
              {radarAxes(dna).map((a, i) => (
                <g key={i}>
                  <line x1={a.x1} y1={a.y1} x2={a.x2} y2={a.y2} stroke="#222" strokeWidth="1" />
                  <text x={a.lx} y={a.ly} textAnchor="middle" fontSize="6" fill="#666" fontFamily="DM Mono">{a.label}</text>
                </g>
              ))}
              <path d={radarPath(dna)} fill="#c9a84c22" stroke="#c9a84c" strokeWidth="1.5" />
              {radarAxes(dna).map((a, i) => {
                const ang = Math.atan2(a.y2 - 70, a.x2 - 70);
                const rv = (dna[i] / 100) * 55;
                return <circle key={i} cx={70 + rv * Math.cos(ang)} cy={70 + rv * Math.sin(ang)} r="3" fill="#c9a84c" />;
              })}
            </svg>
            <div style={{ marginTop: 16 }}>
              {["Emotion", "Action", "Visual", "Story", "Comedy", "Drama"].map((l, i) => (
                <div key={l} style={{ marginBottom: 8 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                    <span style={{ fontSize: 9, color: "#555", letterSpacing: 1 }}>{l}</span>
                    <span style={{ fontSize: 9, color: "#c9a84c" }}>{dna[i]}%</span>
                  </div>
                  <div className="progress-bar"><div className="progress-fill" style={{ width: `${dna[i]}%` }} /></div>
                </div>
              ))}
            </div>
          </div>
          <div className="card">
            <div className="card-title">Audience <span>Traits</span></div>
            <div style={{ marginBottom: 20 }}>
              {audienceForGenre.traits.map((t, i) => <span key={i} className="tag tag-gold">{t}</span>)}
            </div>
            <div className="card-title" style={{ marginTop: 20 }}>Primary Demographics</div>
            {[["Core Age Range", "26–40 years"], ["Gender Split", "55% Female / 45% Male"], ["Location", "Tier 1 & 2 Cities"], ["Education", "Graduate+"], ["Income", "₹4–15L annual"]].map(([k, v]) => (
              <div key={k} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: "1px solid #141414" }}>
                <span style={{ fontSize: 10, color: "#666" }}>{k}</span>
                <span style={{ fontSize: 10, color: "#e8e0d0" }}>{v}</span>
              </div>
            ))}
            <button className="btn btn-gold" style={{ marginTop: 20, width: "100%" }} onClick={runAI}>Generate Full Audience Report</button>
            {(aiLoading || aiResult) && <div className="ai-box" style={{ marginTop: 16 }}><div className="ai-text">{aiLoading ? <span className="loading-dots">Analyzing</span> : aiResult}</div></div>}
          </div>
        </div>
      )}
      {audienceTab === "segments" && (
        <div className="grid-3">
          {audienceForGenre.segments.map((seg, i) => (
            <div key={i} className="card">
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
                <div className="card-title" style={{ marginBottom: 0 }}>Segment {i + 1}</div>
                <div style={{ fontSize: 28, fontFamily: "Bebas Neue", color: "#c9a84c" }}>{seg.size}%</div>
              </div>
              <div style={{ fontSize: 13, color: "#e8e0d0", fontFamily: "Cormorant Garamond", fontWeight: 600, marginBottom: 8 }}>{seg.name}</div>
              <div style={{ fontSize: 10, color: "#666", marginBottom: 12 }}>Age: {seg.age}</div>
              <div className="progress-bar" style={{ marginBottom: 16 }}><div className="progress-fill" style={{ width: `${seg.size}%` }} /></div>
              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: 9, color: "#444", letterSpacing: 2, marginBottom: 6, textTransform: "uppercase" }}>Interests</div>
                {seg.interest.map(x => <span key={x} className="tag tag-gray">{x}</span>)}
              </div>
              <div>
                <div style={{ fontSize: 9, color: "#444", letterSpacing: 2, marginBottom: 6, textTransform: "uppercase" }}>Platforms</div>
                {seg.platforms.map(x => <span key={x} className="tag tag-blue">{x}</span>)}
              </div>
            </div>
          ))}
        </div>
      )}
      {audienceTab === "behavior" && (
        <div className="card">
          <div className="card-title">Behavioral <span>Triggers</span> — What Moves Your Audience to Watch</div>
          <div className="grid-2">
            {[
              { trigger: "Trailer Emotional Hook", impact: 88, desc: "First 15 seconds must establish emotional stakes" },
              { trigger: "Festival Validation", impact: 74, desc: "Award or selection labels increase click-through 3x" },
              { trigger: "Friend Recommendation", impact: 91, desc: "Word-of-mouth is #1 discovery channel for drama" },
              { trigger: "Director Reputation", impact: 62, desc: "Known directors reduce marketing cost by 30%" },
              { trigger: "Cast Recognition", impact: 70, desc: "Even one known face improves opening weekend" },
              { trigger: "Review Aggregate Score", impact: 85, desc: "85%+ positive reviews = streaming success" },
            ].map((b, i) => (
              <div key={i} style={{ padding: "12px 0", borderBottom: "1px solid #141414" }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                  <span style={{ fontSize: 11, color: "#e8e0d0" }}>{b.trigger}</span>
                  <span style={{ fontSize: 11, color: b.impact > 80 ? "#4ade80" : b.impact > 65 ? "#c9a84c" : "#f87171" }}>{b.impact}/100</span>
                </div>
                <div className="progress-bar" style={{ marginBottom: 6 }}>
                  <div className="progress-fill" style={{ width: `${b.impact}%`, background: b.impact > 80 ? "linear-gradient(90deg,#22c55e,#4ade80)" : undefined }} />
                </div>
                <div style={{ fontSize: 9, color: "#555" }}>{b.desc}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
