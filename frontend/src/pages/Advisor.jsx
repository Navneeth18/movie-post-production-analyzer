import { useState, useEffect, useRef } from 'react';
import { callAI } from '../utils/aiHelper';

export default function Advisor({ film }) {
  const [chatHistory, setChatHistory] = useState([
    { role: "ai", text: "Hello, I'm your film strategy advisor. Ask me anything about marketing, distribution, festival strategy, or audience targeting for your project." }
  ]);
  const [chatInput, setChatInput] = useState("");
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory]);

  const sendChat = async () => {
    if (!chatInput.trim()) return;
    const userMsg = chatInput;
    setChatInput("");
    setChatHistory(h => [...h, { role: "user", text: userMsg }]);
    const context = `Film: "${film.title}" | Genre: ${film.genre} | Budget: ${film.budget} | Language: ${film.lang} | Themes: ${film.themes} | Target Region: ${film.region}`;
    const prompt = `Context: ${context}\n\nQuestion: ${userMsg}`;
    const result = await callAI(prompt);
    setChatHistory(h => [...h, { role: "ai", text: result }]);
  };

  return (
    <div className="fade-up">
      <div className="page-header">
        <div className="page-title">AI <span>Strategy</span> Advisor</div>
        <div className="page-sub">Chat with your film marketing expert</div>
      </div>
      <div className="divider" />
      <div className="card">
        <div className="chat-messages">
          {chatHistory.map((msg, i) => (
            <div key={i} className={`msg ${msg.role}`}>
              <div className="msg-label">{msg.role === "user" ? "YOU" : "AI ADVISOR"}</div>
              <div className="msg-bubble">{msg.text}</div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
        <div className="chat-input-row">
          <input 
            type="text" 
            placeholder="Ask about marketing, distribution, festivals..." 
            value={chatInput}
            onChange={e => setChatInput(e.target.value)}
            onKeyPress={e => e.key === "Enter" && sendChat()}
          />
          <button className="btn btn-gold" onClick={sendChat}>Send</button>
        </div>
      </div>
    </div>
  );
}
