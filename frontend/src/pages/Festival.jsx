import { useState } from 'react';
import { callAI } from '../utils/aiHelper';
import { FESTIVALS } from '../utils/constants';

export default function Festival({ film, notify }) {
  const [aiLoading, setAiLoading] = useState(false);
  const [aiResult, setAiResult] = useState("");

  const runAI = async () => {
    setAiLoading(true);
    setAiResult("");
    const prompt = `For "${film.title}" (${film.genre}, themes: ${film.themes}, language: ${film.lang}, budget: ${film.budget}), create a festival submission strategy. Include: priority festivals, submission sequence, what makes this film competitive, how to craft the submission materials, and expected outcomes.`;
    const result = await callAI(prompt);
    setAiResult(result);
    setAiLoading(false);
  };

  return (
    <div className="fade-up">
      <div className="page-header">
        <div className="page-title">Festival <span>Radar</span></div>
        <div className="page-sub">Submission strategy & match engine</div>
      </div>
      <div className="divider" />
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Top Festival <span>Matches</span> for "{film.title}"</div>
        <div style={{ display: "grid", gap: 12 }}>
          {FESTIVALS.map((f, i) => (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 16, padding: "12px 0", borderBottom: "1px solid #141414" }}>
              <div style={{ fontFamily: "Bebas Neue", fontSize: 32, color: f.match > 85 ? "#4ade80" : f.match > 70 ? "#c9a84c" : "#f87171", width: 60, textAlign: "center", flexShrink: 0 }}>{f.match}%</div>
              <div style={{ flex: 1 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                  <span style={{ fontSize: 13, color: "#e8e0d0", fontFamily: "Cormorant Garamond", fontWeight: 600 }}>{f.name}</span>
                  <span className={`tag ${f.status === "Open" ? "tag-green" : "tag-gray"}`}>{f.status}</span>
                </div>
                <div style={{ fontSize: 9, color: "#555" }}>{f.category} · Fee: {f.fee} · Deadline: {f.deadline}</div>
              </div>
              <button className="btn btn-outline" onClick={() => notify(`Strategy generated for ${f.name}`)}>
                Strategy →
              </button>
            </div>
          ))}
        </div>
      </div>
      <div className="card">
        <div className="card-title">AI <span>Festival</span> Strategy</div>
        <button className="btn btn-gold" style={{ marginBottom: 16 }} onClick={runAI}>Generate Festival Strategy</button>
        {(aiLoading || aiResult) && <div className="ai-box"><div className="ai-text">{aiLoading ? <span className="loading-dots">Strategizing</span> : aiResult}</div></div>}
      </div>
    </div>
  );
}
