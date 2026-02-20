import { useState } from 'react';

export default function Release({ film }) {
  const [releaseTab, setReleaseTab] = useState("calendar");
  const [selectedDay, setSelectedDay] = useState(null);

  const calendarData = Array.from({ length: 35 }, (_, i) => {
    const day = i - 3;
    if (day <= 0 || day > 31) return null;
    const risky = [7, 8, 14, 15, 21, 22, 28, 29].includes(day);
    const optimal = [3, 4, 10, 17, 24].includes(day);
    return { day, type: risky ? "risky" : optimal ? "optimal" : "moderate" };
  });

  return (
    <div className="fade-up">
      <div className="page-header">
        <div className="page-title">Release <span>Window</span> Optimizer</div>
        <div className="page-sub">Competition analysis & timing intelligence</div>
      </div>
      <div className="divider" />
      <div className="tab-row">
        {["calendar", "competition", "analysis"].map(t => <div key={t} className={`tab ${releaseTab === t ? "active" : ""}`} onClick={() => setReleaseTab(t)}>{t}</div>)}
      </div>
      {releaseTab === "calendar" && (
        <div className="grid-2">
          <div className="card">
            <div className="card-title">Release <span>Calendar</span> — Next 5 Weeks</div>
            <div style={{ display: "flex", gap: 12, marginBottom: 12 }}>
              {[["optimal", "Optimal", "#4ade80"], ["moderate", "Moderate", "#c9a84c"], ["risky", "Risky", "#f87171"]].map(([type, label, color]) => (
                <div key={type} style={{ display: "flex", alignItems: "center", gap: 6 }}>
                  <div style={{ width: 12, height: 12, background: color + "33", border: `1px solid ${color}44` }} />
                  <span style={{ fontSize: 9, color: "#555" }}>{label}</span>
                </div>
              ))}
            </div>
            <div className="calendar-grid">
              {calendarData.map((d, i) => d ? (
                <div key={i} className={`cal-day ${d.type} ${selectedDay === d.day ? "selected-day" : ""}`} onClick={() => setSelectedDay(d.day)}>
                  {d.day}
                </div>
              ) : <div key={i} />)}
            </div>
          </div>
          <div className="card">
            <div className="card-title">Selected Date <span>Analysis</span></div>
            {selectedDay ? (
              <>
                <div style={{ fontFamily: "Bebas Neue", fontSize: 48, color: "#c9a84c", marginBottom: 8 }}>Day {selectedDay}</div>
                <div style={{ fontSize: 10, color: "#aaa", marginBottom: 16 }}>Competition: 2 major releases, 5 regional films</div>
                <div style={{ marginBottom: 12 }}>
                  <div style={{ fontSize: 9, color: "#555", marginBottom: 6 }}>AUDIENCE AVAILABILITY</div>
                  <div className="progress-bar"><div className="progress-fill green" style={{ width: "72%" }} /></div>
                </div>
                <div style={{ marginBottom: 12 }}>
                  <div style={{ fontSize: 9, color: "#555", marginBottom: 6 }}>MEDIA ATTENTION</div>
                  <div className="progress-bar"><div className="progress-fill" style={{ width: "58%" }} /></div>
                </div>
                <div style={{ marginBottom: 12 }}>
                  <div style={{ fontSize: 9, color: "#555", marginBottom: 6 }}>SCREEN AVAILABILITY</div>
                  <div className="progress-bar"><div className="progress-fill red" style={{ width: "35%" }} /></div>
                </div>
              </>
            ) : (
              <div style={{ fontSize: 11, color: "#555", padding: "40px 0", textAlign: "center" }}>Select a date to see analysis</div>
            )}
          </div>
        </div>
      )}
      {releaseTab === "competition" && (
        <div className="card">
          <div className="card-title">Upcoming <span>Releases</span> — Competition Landscape</div>
          <div style={{ fontSize: 11, color: "#aaa", padding: "20px 0" }}>Competition analysis coming soon...</div>
        </div>
      )}
      {releaseTab === "analysis" && (
        <div className="card">
          <div className="card-title">Release <span>Timing</span> Intelligence</div>
          <div style={{ fontSize: 11, color: "#aaa", padding: "20px 0" }}>Timing analysis coming soon...</div>
        </div>
      )}
    </div>
  );
}
