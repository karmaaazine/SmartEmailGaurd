import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
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
      case 'legitimate': return '#34d399';
      case 'suspicious': return '#fbbf24';
      case 'spam': return '#fb7185';
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
      <div className="beach-card text-center">
        <div className="loading-spinner"></div>
        <p>🌊 Loading your catch history...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="beach-card">
        <h3>⚠️ Error</h3>
        <p>{error}</p>
      </div>
    );
  }

  if (!history || !history.scans || history.scans.length === 0) {
    return (
      <div className="beach-card text-center">
        <h2>📊 Catch Log</h2>
        <p>🌊 No catches in the log yet. Start fishing for some emails!</p>
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
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="beach-card">
        <h2>📊 Catch Log</h2>
        <p>Review your recent catches and security patrol history</p>
      </div>

      {/* Summary Metrics */}
      <div className="beach-card">
        <h3>🏖️ Summary</h3>
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-value">{totalScans}</div>
            <div className="metric-label">Total Catches</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{recentScans}</div>
            <div className="metric-label">Recent Catches</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{(avgConfidence * 100).toFixed(1)}%</div>
            <div className="metric-label">Avg Confidence</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{Object.keys(classificationCounts).length}</div>
            <div className="metric-label">Types Caught</div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="beach-card">
        <h3>📈 Catch Analytics</h3>
        <div className="charts-container">
          {/* Pie Chart */}
          <div className="chart-section">
            <h4>🐟 Catch Types Distribution</h4>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Bar Chart */}
          <div className="chart-section">
            <h4>📊 Recent Confidence Scores</h4>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={confidenceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="confidence" fill="#0ea5e9" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Scan List */}
      <div className="beach-card">
        <h3>🎣 Recent Catches</h3>
        <div className="scans-list">
          {scans.map((scan, index) => (
            <motion.div
              key={index}
              className="scan-item"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
            >
              <div className="scan-header">
                <span className="scan-icon">
                  {getClassificationIcon(scan.classification)}
                </span>
                <span className="scan-type">
                  {scan.classification.toUpperCase()}
                </span>
                <span className="scan-confidence">
                  {(scan.confidence * 100).toFixed(1)}%
                </span>
                <span className="scan-date">
                  {new Date(scan.timestamp).toLocaleDateString()}
                </span>
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => setSelectedScan(selectedScan === index ? null : index)}
                >
                  {selectedScan === index ? 'Hide' : 'View'} Details
                </button>
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
  );
};

export default ScanHistory; 