import { useState, useEffect } from 'react';
import { callAI } from '../utils/aiHelper';
import { analyticsAPI, calculatorAPI } from '../services/api';

export default function Dashboard({ film }) {
  const [aiLoading, setAiLoading] = useState(false);
  const [aiResult, setAiResult] = useState("");
  const [hwsScore, setHwsScore] = useState(null);
  const [sentiment, setSentiment] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, [film]);

  const loadDashboardData = async () => {
    try {
      // Load sentiment data
      const sentimentRes = await analyticsAPI.getSentiment(film.title);
      setSentiment(sentimentRes.data);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    }
  };

  const runAI = async () => {
    setAiLoading(true);
    setAiResult("");
    const prompt = `Film: "${film.title}", Genre: ${film.genre}, Budget: ${film.budget}, Language: ${film.lang}, Themes: ${film.themes}, Region: ${film.region}. Give 3 key strategic priorities for this film's marketing and distribution in the Indian market.`;
    const result = await callAI(prompt);
    setAiResult(result);
    setAiLoading(false);
  };

  return (
    <div className="fade-up">
      <div className="page-header">
        <div className="page-title">Producer <span>Intelligence</span></div>
        <div className="page-sub">Overview — {film.title}</div>
      </div>
      <div className="divider" />
      <div className="grid-4" style={{ marginBottom: 24 }}>
        {[
          { num: "87", label: "Audience Fit Score", change: "+12 vs avg", up: true },
          { num: "3.2x", label: "Projected Campaign ROI", change: "Based on comps", up: true },
          { num: "6", label: "Festivals Matched", change: "2 high priority", up: true },
          { num: "₹3.4Cr", label: "Est. OTT Deal Value", change: "Netflix + Prime", up: true },
        ].map((s, i) => (
          <div key={i} className="card hero-stat">
            <div className="stat-num">{s.num}</div>
            <div className="stat-label">{s.label}</div>
            <div className="stat-change">{s.change}</div>
          </div>
        ))}
      </div>
      <div className="grid-2" style={{ marginBottom: 24 }}>
        <div className="card">
          <div className="card-title">Audience Reach by Channel</div>
          <div className="chart-bar">
            {[["Social", 72], ["OTT Promo", 65], ["Festivals", 48], ["Press", 38], ["Influencer", 55], ["Trailer", 90]].map(([l, v]) => (
              <div key={l} className="bar-col">
                <div className="bar-fill" style={{ height: `${v * 0.8}%` }} />
                <div className="bar-label">{l}</div>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 12 }}>
            <div className="film-strip">
              {Array.from({ length: 24 }, (_, i) => <div key={i} className={`film-frame ${i < 17 ? "filled" : ""}`} />)}
            </div>
            <div style={{ fontSize: 9, color: "#555", letterSpacing: 1 }}>OVERALL VISIBILITY SCORE — 71%</div>
          </div>
        </div>
        <div className="card">
          <div className="card-title">Strategic <span>Action Items</span></div>
          <div className="timeline">
            {[
              { title: "Submit to MAMI Mumbai", sub: "Deadline in 18 days — Match: 94%", done: false },
              { title: "Lock Trailer Cut", sub: "Target: 90s emotional hook", done: false },
              { title: "Engage 3 Micro-Influencers", sub: "Film culture niche — ₹40K budget", done: true },
              { title: "OTT Pitch Deck Ready", sub: "Netflix + MUBI priority", done: true },
              { title: "Press Kit Distribution", sub: "15 film journalists targeted", done: false },
            ].map((item, i) => (
              <div key={i} className="timeline-item">
                <div className={`timeline-dot ${item.done ? "" : "gray"}`} />
                <div className="timeline-title" style={{ color: item.done ? "#555" : "#e8e0d0", textDecoration: item.done ? "line-through" : "none" }}>{item.title}</div>
                <div className="timeline-sub">{item.sub}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="card">
        <div className="card-title">Quick <span>AI Insight</span></div>
        <button className="btn btn-gold" onClick={runAI} style={{ marginBottom: 16 }}>
          {aiLoading ? "Analyzing..." : "Generate AI Brief"}
        </button>
        {(aiLoading || aiResult) && (
          <div className="ai-box">
            <div className="ai-text">{aiLoading ? <span className="loading-dots">Thinking</span> : aiResult}</div>
          </div>
        )}
      </div>
    </div>
  );
}
