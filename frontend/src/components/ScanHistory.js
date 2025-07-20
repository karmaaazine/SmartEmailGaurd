import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import ResultDisplay from './ResultDisplay';

const ScanHistory = () => {
  const [history, setHistory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedScan, setSelectedScan] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get('/history?limit=50', {
        headers: {
          'x-api-key': 'salmas_email_guard'
        }
      });
      setHistory(response.data);
    } catch (err) {
      setError('Failed to load scan history. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  const getClassificationColor = (classification) => {
    switch (classification) {
      case 'legitimate': return '#22c55e';
      case 'suspicious': return '#fbbf24';
      case 'spam': return '#ec4899';
      case 'phishing': return '#dc2626';
      default: return '#6b7280';
    }
  };

  const getClassificationIcon = (classification) => {
    switch (classification) {
      case 'legitimate': return '🐠';
      case 'suspicious': return '🦈';
      case 'spam': return '🐙';
      case 'phishing': return '🦑';
      default: return '🐟';
    }
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="page-hero">
          <h1>Scan History</h1>
          <p>View your email analysis history and track security patterns.</p>
        </div>
        <div className="text-center">
          <div className="loading-spinner"></div>
          <p>Loading scan history...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container">
        <div className="page-hero">
          <h1>Scan History</h1>
          <p>View your email analysis history and track security patterns.</p>
        </div>
        <div className="content-card">
          <div className="result-box result-suspicious">
            <h3>⚠️ Error</h3>
            <p>{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!history || !history.scans || history.scans.length === 0) {
    return (
      <div className="page-container">
        <div className="page-hero">
          <h1>Scan History</h1>
          <p>View your email analysis history and track security patterns.</p>
        </div>
        <div className="content-card text-center">
          <h2>No Scans Yet</h2>
          <p>Start scanning emails to see your history here.</p>
        </div>
      </div>
    );
  }

  const scans = history.scans;
  const totalScans = history.total_count;
  const recentScans = scans.length;
  const avgConfidence = scans.length > 0 
    ? scans.reduce((sum, scan) => sum + scan.confidence, 0) / scans.length 
    : 0;

  // Prepare data for charts
  const classificationCounts = scans.reduce((acc, scan) => {
    acc[scan.classification] = (acc[scan.classification] || 0) + 1;
    return acc;
  }, {});

  const chartData = Object.entries(classificationCounts).map(([type, count]) => ({
    name: type.charAt(0).toUpperCase() + type.slice(1),
    value: count,
    color: getClassificationColor(type)
  }));

  const confidenceData = scans.slice(0, 10).map((scan, index) => ({
    name: `Scan ${index + 1}`,
    confidence: (scan.confidence * 100).toFixed(1),
    type: scan.classification
  }));

  return (
    <div className="page-container">
      <div className="page-hero">
        <h1>Scan History</h1>
        <p>View your email analysis history and track security patterns.</p>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Summary Metrics */}
        <div className="content-card">
          <h2>Summary</h2>
          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-value">{totalScans}</div>
              <div className="metric-label">Total Scans</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">{recentScans}</div>
              <div className="metric-label">Recent Scans</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">{(avgConfidence * 100).toFixed(1)}%</div>
              <div className="metric-label">Avg Confidence</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">{Object.keys(classificationCounts).length}</div>
              <div className="metric-label">Types Detected</div>
            </div>
          </div>
        </div>

        {/* Charts */}
        <div className="content-card">
          <h2>Analysis Charts</h2>
          <div className="metrics-grid">
            <div className="metric-card">
              <h3>Classification Distribution</h3>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={chartData}
                    cx="50%"
                    cy="50%"
                    outerRadius={60}
                    dataKey="value"
                    label={({ name, value }) => `${name}: ${value}`}
                  >
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="metric-card">
              <h3>Confidence Scores</h3>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={confidenceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="confidence" fill="#166534" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Recent Scans */}
        <div className="content-card">
          <h2>Recent Scans</h2>
          <div className="scan-list">
            {scans.map((scan, index) => (
              <motion.div
                key={index}
                className="scan-item"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                onClick={() => setSelectedScan(selectedScan === index ? null : index)}
              >
                <div className="scan-header">
                  <div className="scan-classification">
                    <span className="classification-badge" style={{ backgroundColor: getClassificationColor(scan.classification) }}>
                      {scan.classification.toUpperCase()}
                    </span>
                  </div>
                  <div className="scan-timestamp">
                    {new Date(scan.timestamp).toLocaleString()}
                  </div>
                </div>
                <div className="scan-content">
                  <p>{scan.content.substring(0, 100)}...</p>
                </div>
                <div className="scan-confidence">
                  Confidence: {(scan.confidence * 100).toFixed(1)}%
                </div>
                
                {selectedScan === index && (
                  <motion.div
                    className="scan-details"
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                  >
                    <ResultDisplay result={scan} />
                  </motion.div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default ScanHistory; 