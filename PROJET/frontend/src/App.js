
import React, { useState } from 'react';
import './App.css';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [icons, setIcons] = useState([]);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    setIcons([]);
    try {
      const res = await fetch(`${API_BASE}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `HTTP ${res.status}`);
      }
      const data = await res.json();
      setIcons(data.icons || []);
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>IconForge — Générateur d'icônes</h1>
        <form onSubmit={handleSubmit} className="prompt-form">
          <input
            type="text"
            placeholder="Décris l'icône que tu veux..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="prompt-input"
          />
          <button type="submit" disabled={loading || !query.trim()}>
            {loading ? 'Génération...' : 'Générer'}
          </button>
        </form>

        {error && <div className="error">Erreur: {error}</div>}

        <div className="icons-grid">
          {icons.map((icon) => (
            <div key={icon.id} className="icon-card">
              <h3>{icon.concept || icon.id}</h3>
              <div className="icon-preview">
                <img
                  alt={icon.concept}
                  src={`${API_BASE}${icon.svg_file_url}`}
                />
              </div>
              <details>
                <summary>Voir le code SVG</summary>
                <pre className="svg-code">{icon.svg_code}</pre>
              </details>
              <a href={`${API_BASE}${icon.svg_file_url}`} target="_blank" rel="noreferrer" download>
                Télécharger SVG
              </a>
            </div>
          ))}
        </div>
      </header>
    </div>
  );
}

export default App;
