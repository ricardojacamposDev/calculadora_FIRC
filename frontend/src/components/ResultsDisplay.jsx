import React from 'react';
import './ResultsDisplay.css';

function ResultsDisplay({ results, filename }) {
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value);
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>✅ Processamento Concluído</h2>
        <p className="filename">{filename}</p>
      </div>

      <div className="results-grid">
        <div className="result-card">
          <div className="result-label">Valor Pago</div>
          <div className="result-value valor-pago">
            {formatCurrency(results.total_valor_pago)}
          </div>
          <div className="result-count">
            {results.details?.valores_pago_count || 0} valores encontrados
          </div>
        </div>

        <div className="result-card">
          <div className="result-label">Cartório</div>
          <div className="result-value cartorio">
            {formatCurrency(results.total_cartorio)}
          </div>
          <div className="result-count">
            {results.details?.cartorio_count || 0} valores encontrados
          </div>
        </div>
      </div>

      <div className="results-summary">
        <div className="summary-item">
          <span className="summary-label">Total de Valores:</span>
          <span className="summary-value">{results.total_values_found}</span>
        </div>
        <div className="summary-item">
          <span className="summary-label">Diferença:</span>
          <span className="summary-value">
            {formatCurrency(
              results.total_valor_pago - results.total_cartorio
            )}
          </span>
        </div>
      </div>

      <div className="results-details">
        <h3>Detalhes</h3>
        <ul>
          <li>
            <strong>Arquivo:</strong> {filename}
          </li>
          <li>
            <strong>Valores de Valor Pago:</strong>{' '}
            {results.details?.valores_pago_count || 0}
          </li>
          <li>
            <strong>Valores de Cartório:</strong> {results.details?.cartorio_count || 0}
          </li>
          <li>
            <strong>Status:</strong> Processado com sucesso
          </li>
        </ul>
      </div>
    </div>
  );
}

export default ResultsDisplay;
