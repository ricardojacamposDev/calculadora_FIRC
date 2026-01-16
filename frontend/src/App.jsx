import React, { useState } from 'react';
import './App.css';
import PDFUploader from './components/PDFUploader';
import ResultsDisplay from './components/ResultsDisplay';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filename, setFilename] = useState(null);

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError(null);
    setResults(null);
    setFilename(file.name);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/process-pdf', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        setResults(data.data);
      } else {
        setError('Erro ao processar PDF');
      }
    } catch (err) {
      setError(err.message || 'Erro ao conectar com o servidor');
      console.error('Erro:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
    setFilename(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>💰 Calculadora FIRC</h1>
        <p>Processador de Documentos Financeiros</p>
      </header>

      <main className="app-main">
        <div className="container">
          {!results ? (
            <PDFUploader onFileUpload={handleFileUpload} loading={loading} />
          ) : (
            <>
              <ResultsDisplay results={results} filename={filename} />
              <button className="btn btn-reset" onClick={handleReset}>
                Processar Outro PDF
              </button>
            </>
          )}

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              <p>{error}</p>
            </div>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>Calculadora FIRC v1.0.0 | Processamento de Guias Geradas</p>
      </footer>
    </div>
  );
}

export default App;
