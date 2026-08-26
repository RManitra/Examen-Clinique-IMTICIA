import React, { useState, useCallback } from 'react';
import './App.css';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

const SUGGESTIONS = [
  'Cloud computing',
  'Sécurité informatique',
  'Base de données',
  'Collaboration d\'équipe',
  'Déploiement CI/CD',
  'Musique et art',
  'Analyse de données',
  'Configuration serveur',
];

function SparkleIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2L9.5 8.5 3 12l6.5 3.5L12 22l2.5-6.5L21 12l-6.5-3.5z" />
    </svg>
  );
}

function CodeIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="16 18 22 12 16 6" />
      <polyline points="8 6 2 12 8 18" />
    </svg>
  );
}

function DownloadIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="7 10 12 15 17 10" />
      <line x1="12" y1="15" x2="12" y2="3" />
    </svg>
  );
}

function IconCard({ icon }) {
  const [showCode, setShowCode] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(icon.svg_code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      /* clipboard API unavailable */
    }
  }, [icon.svg_code]);

  return (
    <div className="icon-card">
      <div className="icon-card-header">
        <span className="icon-card-title">{icon.concept || icon.id}</span>
        <span className="icon-card-id">{icon.id}</span>
      </div>

      <div className="icon-preview">
        <img
          alt={icon.concept || icon.id}
          src={`${API_BASE}${icon.svg_file_url}`}
          loading="lazy"
        />
      </div>

      {showCode && (
        <div className="svg-code-panel">
          <div className="svg-code-header">
            <span className="svg-code-label">SVG</span>
            <button className={`copy-btn ${copied ? 'copied' : ''}`} onClick={handleCopy}>
              {copied ? 'Copié !' : 'Copier'}
            </button>
          </div>
          <div className="svg-code-content">
            <pre>{icon.svg_code}</pre>
          </div>
        </div>
      )}

      <div className="icon-card-actions">
        <button className="icon-card-btn btn-code" onClick={() => setShowCode(!showCode)}>
          <CodeIcon />
          {showCode ? 'Masquer' : 'Code'}
        </button>
        <a
          className="icon-card-btn btn-download"
          href={`${API_BASE}${icon.svg_file_url}`}
          target="_blank"
          rel="noreferrer"
          download
        >
          <DownloadIcon />
          Télécharger
        </a>
      </div>
    </div>
  );
}

function EmptyState({ onSuggestion }) {
  return (
    <div className="empty-state">
      <div className="empty-icon">
        <SparkleIcon />
      </div>
      <h2 className="empty-title">Créez des icônes uniques</h2>
      <p className="empty-description">
        Décrivez le concept que vous imaginez, et IconForge génère une famille
        d'icônes SVG cohérentes avec votre charte graphique.
      </p>
      <div className="suggestion-chips">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            className="suggestion-chip"
            onClick={() => onSuggestion(s)}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [icons, setIcons] = useState([]);
  const [error, setError] = useState(null);
  const [searched, setSearched] = useState(false);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    const q = query.trim();
    if (!q) return;

    setError(null);
    setLoading(true);
    setSearched(true);

    try {
      const res = await fetch(`${API_BASE}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q }),
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `Erreur HTTP ${res.status}`);
      }
      const data = await res.json();
      setIcons(data.icons || []);
    } catch (err) {
      setError(String(err));
      setIcons([]);
    } finally {
      setLoading(false);
    }
  }, [query]);

  const handleSuggestion = useCallback((s) => {
    setQuery(s);
  }, []);

  return (
    <div className="app">
      {/* Hero */}
      <header className="hero">
        <div className="hero-brand">
          <div className="hero-logo">
            <SparkleIcon />
          </div>
          <h1 className="hero-title">
            Icon<span>Forge</span>
          </h1>
        </div>
        <p className="hero-subtitle">
          Générateur d'icônes SVG par intelligence artificielle
        </p>
      </header>

      {/* Input */}
      <section className="input-section">
        <form onSubmit={handleSubmit} className="prompt-form">
          <input
            type="text"
            className="prompt-input"
            placeholder="Décris l'icône que tu veux créer..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
          />
          <button
            type="submit"
            className={`submit-btn ${loading ? 'loading' : ''}`}
            disabled={loading || !query.trim()}
          >
            {loading ? 'Génération…' : 'Générer'}
          </button>
        </form>
      </section>

      {/* Error */}
      {error && (
        <div className="error-banner" role="alert">
          {error}
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="loading-section">
          <div className="loading-spinner" />
          <p className="loading-text">
            Génération en cours<span className="loading-dots" />
          </p>
        </div>
      )}

      {/* Results or Empty State */}
      {!loading && searched && icons.length > 0 && (
        <section className="results-section">
          <div className="results-header">
            <span className="results-count">
              <strong>{icons.length}</strong> icône{icons.length > 1 ? 's' : ''} générée{icons.length > 1 ? 's' : ''}
            </span>
          </div>
          <div className="icons-grid">
            {icons.map((icon) => (
              <IconCard key={icon.id} icon={icon} />
            ))}
          </div>
        </section>
      )}

      {!loading && !searched && (
        <EmptyState onSuggestion={handleSuggestion} />
      )}

      {!loading && searched && icons.length === 0 && !error && (
        <div className="empty-state">
          <p className="empty-description">Aucune icône générée. Essayez un autre concept.</p>
        </div>
      )}

      <footer className="app-footer">
        IconForge AI — Examen Clinique IMTICIA
      </footer>
    </div>
  );
}

export default App;
