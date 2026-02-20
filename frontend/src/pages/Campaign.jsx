import { useState } from 'react';
import { callAI } from '../utils/aiHelper';
import { marketingAPI } from '../services/api';

export default function Campaign({ film }) {
  const [campaignChannel, setCampaignChannel] = useState({ social: 40, influencer: 25, ott: 20, press: 15 });
  const [aiLoading, setAiLoading] = useState(false);
  const [aiResult, setAiResult] = useState("");
  const [memeLoading, setMemeLoading] = useState(false);

  const runAI = async () => {
    setAiLoading(true);
    setAiResult("");
    const prompt = `For "${film.title}" (${film.genre}), the producer has allocated: ${JSON.stringify(campaignChannel)}% across channels. Budget: ${film.budget}. Analyze this allocation and suggest 3 specific optimizations to maximize ROI.`;
    const result = await callAI(prompt);
    setAiResult(result);
    setAiLoading(false);
  };

  const generateMeme = async () => {
    setMemeLoading(true);
    try {
      const response = await marketingAPI.generateMeme(
        `Create a viral meme for ${film.title} - ${film.genre} film`,
        'viral'
      );
      console.log('Meme generated:', response.data);
    } catch (error) {
      console.error('Meme generation failed:', error);
    } finally {
      setMemeLoading(false);
    }
  };

  return (
    <div className="fade-up">
      <div className="page-header">
        <div className="page-title">Campaign <span>ROI</span> Simulator</div>
        <div className="page-sub">Budget optimizer — {film.title}</div>
      </div>
      <div className="divider" />
      <div className="grid-2" style={{ marginBottom: 24 }}>
        <div className="card">
          <div className="card-title">Budget <span>Allocation</span> (% of Marketing Budget)</div>
          {Object.entries(campaignChannel).map(([key, val]) => (
            <div key={key} style={{ marginBottom: 16 }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                <label style={{ marginBottom: 0, color: "#888" }}>{key.toUpperCase()}</label>
                <span style={{ fontSize: 11, color: "#c9a84c" }}>{val}%</span>
              </div>
              <input type="range" min="0" max="80" value={val} onChange={e => {
                const newVal = parseInt(e.target.value);
                setCampaignChannel(prev => ({ ...prev, [key]: newVal }));
              }} style={{ padding: 0, background: "transparent", border: "none", accentColor: "#c9a84c" }} />
            </div>
          ))}
          <div style={{ padding: "12px 0", borderTop: "1px solid #1a1a1a", display: "flex", justifyContent: "space-between" }}>
            <span style={{ fontSize: 9, color: "#555", letterSpacing: 2, textTransform: "uppercase" }}>Total Allocated</span>
            <span style={{ fontSize: 11, color: Object.values(campaignChannel).reduce((a, b) => a + b, 0) > 100 ? "#f87171" : "#4ade80" }}>
              {Object.values(campaignChannel).reduce((a, b) => a + b, 0)}%
            </span>
          </div>
        </div>
        <div className="card">
          <div className="card-title">Projected <span>Returns</span></div>
          {Object.entries(campaignChannel).map(([key, val]) => {
            const roi = { social: 2.8, influencer: 1.9, ott: 3.5, press: 1.4 };
            const roiVal = (val * roi[key] / 100).toFixed(2);
            return (
              <div key={key} style={{ marginBottom: 12, padding: "10px 0", borderBottom: "1px solid #141414" }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                  <span style={{ fontSize: 10, color: "#888", letterSpacing: 1, textTransform: "uppercase" }}>{key}</span>
                  <div>
                    <span style={{ fontSize: 9, color: "#555", marginRight: 8 }}>ROI: {roi[key]}x</span>
                    <span style={{ fontSize: 11, color: "#c9a84c" }}>{roiVal}x return</span>
                  </div>
                </div>
                <div className="progress-bar">
                  <div className="progress-fill" style={{ width: `${Math.min(val * roi[key], 100)}%` }} />
                </div>
              </div>
            );
          })}
          <div style={{ padding: "16px 0 0", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <div style={{ fontSize: 9, color: "#555", letterSpacing: 2, textTransform: "uppercase" }}>Blended Campaign ROI</div>
              <div style={{ fontFamily: "Bebas Neue", fontSize: 36, color: "#c9a84c" }}>
                {(Object.entries(campaignChannel).reduce((sum, [key, val]) => {
                  const roi = { social: 2.8, influencer: 1.9, ott: 3.5, press: 1.4 };
                  return sum + (val / 100) * roi[key];
                }, 0)).toFixed(1)}x
              </div>
            </div>
            <button className="btn btn-gold" onClick={runAI}>AI Optimize</button>
          </div>
        </div>
      </div>
      {(aiLoading || aiResult) && (
        <div className="card">
          <div className="ai-box"><div className="ai-text">{aiLoading ? <span className="loading-dots">Optimizing</span> : aiResult}</div></div>
        </div>
      )}
      <div className="card">
        <div className="card-title">Channel <span>Intelligence</span></div>
        <div className="grid-3">
          {[
            { ch: "Social Media", best: "Reels, Threads, YouTube Shorts", timing: "6 weeks pre-release", tip: "Behind-the-scenes drives 40% more organic reach than promotional content", icon: "◎" },
            { ch: "OTT Promotions", best: "Pre-roll, Sponsored content", timing: "4 weeks pre-release", tip: "Partner with platform for editorial feature — free if content is exclusive", icon: "⬢" },
            { ch: "Influencer", best: "Film critics + Micro-influencers", timing: "3 weeks pre-release", tip: "10 micro-influencers (50K followers) outperform 1 macro (2M) for niche films", icon: "⬡" },
          ].map((c, i) => (
            <div key={i} className="card" style={{ background: "#0a0a0a" }}>
              <div style={{ fontFamily: "Bebas Neue", fontSize: 28, color: "#c9a84c", marginBottom: 8 }}>{c.icon} {c.ch}</div>
              <div style={{ fontSize: 9, color: "#555", marginBottom: 4, textTransform: "uppercase", letterSpacing: 1 }}>Best Format</div>
              <div style={{ fontSize: 10, color: "#aaa", marginBottom: 12 }}>{c.best}</div>
              <div style={{ fontSize: 9, color: "#555", marginBottom: 4, textTransform: "uppercase", letterSpacing: 1 }}>Timing</div>
              <div style={{ fontSize: 10, color: "#aaa", marginBottom: 12 }}>{c.timing}</div>
              <div style={{ fontSize: 9, color: "#c9a84c33", padding: "8px", background: "#c9a84c11", borderLeft: "2px solid #c9a84c44" }}>
                <span style={{ color: "#c9a84c" }}>TIP: </span>{c.tip}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
