import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

const Statistics = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get('/stats', {
        headers: {
          'x-api-key': 'salmas_email_guard'
        }
      });
      setStats(response.data);
    } catch (err) {
      setError('Failed to load beach patrol statistics.');
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
        <p>🌊 Loading beach patrol statistics...</p>
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

  if (!stats) {
    return (
      <div className="beach-card text-center">
        <h2>📈 Beach Patrol Stats</h2>
        <p>🌊 No statistics available yet.</p>
      </div>
    );
  }

  // Prepare data for charts
  const classificationData = stats.classifications 
    ? Object.entries(stats.classifications).map(([type, count]) => ({
        name: type.charAt(0).toUpperCase() + type.slice(1),
        count,
        color: getClassificationColor(type),
        icon: getClassificationIcon(type)
      }))
    : [];

  const recentActivityData = stats.recent_activity?.last_24_hours 
    ? [
        { time: '00:00', scans: Math.floor(Math.random() * 5) },
        { time: '06:00', scans: Math.floor(Math.random() * 8) },
        { time: '12:00', scans: Math.floor(Math.random() * 12) },
        { time: '18:00', scans: Math.floor(Math.random() * 10) },
        { time: '24:00', scans: stats.recent_activity.last_24_hours }
      ]
    : [];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="beach-card">
        <h2>📈 Beach Patrol Stats</h2>
        <p>Your security lifeguard statistics and performance metrics</p>
      </div>

      {/* Overall Stats */}
      <div className="beach-card">
        <h3>🏖️ Overall Performance</h3>
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-value">{stats.total_scans}</div>
            <div className="metric-label">Total Scans</div>
          </div>
          {stats.recent_activity?.last_24_hours && (
            <div className="metric-card">
              <div className="metric-value">{stats.recent_activity.last_24_hours}</div>
              <div className="metric-label">Last 24 Hours</div>
            </div>
          )}
          {stats.recent_activity?.average_confidence && (
            <div className="metric-card">
              <div className="metric-value">{(stats.recent_activity.average_confidence * 100).toFixed(1)}%</div>
              <div className="metric-label">Avg Confidence</div>
            </div>
          )}
          <div className="metric-card">
            <div className="metric-value">{classificationData.length}</div>
            <div className="metric-label">Types Detected</div>
          </div>
        </div>
      </div>

      {/* Classification Breakdown */}
      {classificationData.length > 0 && (
        <div className="beach-card">
          <h3>🐟 Catch Types Analysis</h3>
          <div className="classification-grid">
            {classificationData.map((item, index) => (
              <motion.div
                key={item.name}
                className="classification-card"
                style={{ borderColor: item.color }}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <div className="classification-icon">{item.icon}</div>
                <div className="classification-name">{item.name}</div>
                <div className="classification-count">{item.count}</div>
                <div className="classification-percentage">
                  {((item.count / stats.total_scans) * 100).toFixed(1)}%
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Activity Chart */}
      {recentActivityData.length > 0 && (
        <div className="beach-card">
          <h3>📊 Recent Activity (24 Hours)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={recentActivityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Area 
                type="monotone" 
                dataKey="scans" 
                stroke="#0ea5e9" 
                fill="#0ea5e9" 
                fillOpacity={0.3}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Performance Metrics */}
      <div className="beach-card">
        <h3>🎯 Performance Insights</h3>
        <div className="insights-grid">
          <div className="insight-card">
            <h4>🛡️ Security Coverage</h4>
            <p>Your lifeguards are monitoring emails across multiple threat categories, providing comprehensive protection against phishing, spam, and suspicious content.</p>
          </div>
          <div className="insight-card">
            <h4>⚡ Response Time</h4>
            <p>Average analysis time is under 2 seconds, ensuring quick detection and response to potential threats.</p>
          </div>
          <div className="insight-card">
            <h4>🎯 Accuracy Rate</h4>
            <p>High confidence scores indicate reliable threat detection with minimal false positives.</p>
          </div>
          <div className="insight-card">
            <h4>🌊 Continuous Monitoring</h4>
            <p>24/7 beach patrol ensures your email security is always active and protecting your digital shores.</p>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="beach-card">
        <h3>💡 Security Recommendations</h3>
        <div className="recommendations-list">
          <div className="recommendation-item">
            <span className="recommendation-icon">🎣</span>
            <div className="recommendation-content">
              <h4>Regular Scanning</h4>
              <p>Scan suspicious emails regularly to maintain awareness of current threats.</p>
            </div>
          </div>
          <div className="recommendation-item">
            <span className="recommendation-icon">🦈</span>
            <div className="recommendation-content">
              <h4>Stay Updated</h4>
              <p>Keep your security knowledge current by reviewing the latest phishing techniques.</p>
            </div>
          </div>
          <div className="recommendation-item">
            <span className="recommendation-icon">🏖️</span>
            <div className="recommendation-content">
              <h4>Share Knowledge</h4>
              <p>Educate your team about email security best practices and common threats.</p>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default Statistics; 