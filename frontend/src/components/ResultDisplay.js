import React from 'react';
import { motion } from 'framer-motion';

const ResultDisplay = ({ result }) => {
  const { classification, confidence, explanation, features, indicators } = result;

  const classificationIcons = {
    legitimate: '🐠',
    suspicious: '🦈',
    spam: '🐙',
    phishing: '🦑'
  };

  const getResultClass = () => {
    switch (classification) {
      case 'legitimate':
        return 'result-legitimate';
      case 'suspicious':
        return 'result-suspicious';
      case 'spam':
        return 'result-spam';
      case 'phishing':
        return 'result-phishing';
      default:
        return 'result-suspicious';
    }
  };

  const getResultTitle = () => {
    switch (classification) {
      case 'legitimate':
        return 'SAFE - This email looks legitimate!';
      case 'suspicious':
        return 'SUSPICIOUS - Exercise caution with this email';
      case 'spam':
        return 'SPAM - This appears to be unwanted spam';
      case 'phishing':
        return 'PHISHING - This is likely a phishing attempt!';
      default:
        return 'UNKNOWN - Unable to classify this email';
    }
  };

  return (
    <motion.div
      className="result-container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className={`result-box ${getResultClass()}`}>
        <h3>
          {classificationIcons[classification] || '🐟'} Catch Report
        </h3>
        <p><strong>Type:</strong> {getResultTitle()}</p>
        <p><strong>Confidence:</strong> {(confidence * 100).toFixed(1)}%</p>
        <p><strong>Analysis:</strong> {explanation}</p>
      </div>

      {/* Fishing Metrics */}
      <div className="beach-card">
        <h3>🎣 Fishing Metrics</h3>
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-value">{features?.length?.toLocaleString() || 0}</div>
            <div className="metric-label">Characters</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{features?.word_count || 0}</div>
            <div className="metric-label">Words</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{features?.url_count || 0}</div>
            <div className="metric-label">Links</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{features?.urgent_words || 0}</div>
            <div className="metric-label">Red Flags</div>
          </div>
        </div>
      </div>

      {/* Indicators */}
      {indicators && indicators.length > 0 && (
        <div className="beach-card">
          <h3>⚠️ Caught Red Flags</h3>
          <ul className="indicators-list">
            {indicators.map((indicator, index) => (
              <motion.li
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="indicator-item"
              >
                🎯 {indicator.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </motion.li>
            ))}
          </ul>
        </div>
      )}

      {/* Additional Features */}
      {features && Object.keys(features).length > 4 && (
        <div className="beach-card">
          <h3>🔍 Detailed Analysis</h3>
          <div className="features-grid">
            {Object.entries(features).map(([key, value]) => {
              if (['length', 'word_count', 'url_count', 'urgent_words'].includes(key)) {
                return null;
              }
              return (
                <div key={key} className="feature-detail">
                  <strong>{key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</strong>
                  <span>{typeof value === 'boolean' ? (value ? 'Yes' : 'No') : value}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default ResultDisplay; 