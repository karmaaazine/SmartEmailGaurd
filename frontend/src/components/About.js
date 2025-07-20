import React from 'react';
import { motion } from 'framer-motion';

const About = () => {
  return (
    <div className="page-container">
      <div className="page-hero">
        <h1>About Catch A Phish</h1>
        <p>Your intelligent email security companion powered by advanced AI technology.</p>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="content-card">
          <h2>Our Mission</h2>
          <p>
            Catch A Phish is dedicated to protecting individuals and organizations from the growing threat of 
            phishing attacks and email scams. We believe that everyone deserves to feel safe and secure when 
            using email, which is why we've developed an intelligent system that works tirelessly to identify 
            and flag suspicious messages before they can cause harm.
          </p>
        </div>

        <div className="content-card">
          <h2>How It Works</h2>
          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-value">1</div>
              <div className="metric-label">Upload Email</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">2</div>
              <div className="metric-label">AI Analysis</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">3</div>
              <div className="metric-label">Get Results</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">4</div>
              <div className="metric-label">Stay Protected</div>
            </div>
          </div>
        </div>

        <div className="content-card">
          <h2>Key Features</h2>
          <div className="metrics-grid">
            <div className="metric-card">
              <h3>AI-Powered Detection</h3>
              <p>Advanced machine learning algorithms analyze email content, links, and patterns to identify threats.</p>
            </div>
            <div className="metric-card">
              <h3>Real-Time Analysis</h3>
              <p>Get instant results with detailed explanations of why an email was flagged as suspicious.</p>
            </div>
            <div className="metric-card">
              <h3>Multiple Input Methods</h3>
              <p>Paste email content directly or upload email files for analysis.</p>
            </div>
            <div className="metric-card">
              <h3>Comprehensive Reports</h3>
              <p>Detailed breakdowns including confidence scores and threat indicators.</p>
            </div>
          </div>
        </div>

        <div className="content-card">
          <h2>Technology Stack</h2>
          <div className="metrics-grid">
            <div className="metric-card">
              <h3>Backend</h3>
              <p>FastAPI with Python, HuggingFace Transformers for AI analysis</p>
            </div>
            <div className="metric-card">
              <h3>Frontend</h3>
              <p>React with modern UI components and responsive design</p>
            </div>
            <div className="metric-card">
              <h3>AI Model</h3>
              <p>DistilBERT fine-tuned for sentiment and threat analysis</p>
            </div>
            <div className="metric-card">
              <h3>Security</h3>
              <p>Token-based authentication and input validation</p>
            </div>
          </div>
        </div>

        <div className="content-card">
          <h2>Security & Privacy</h2>
          <p>
            Your privacy and security are our top priorities. We do not store any email content permanently, 
            and all analysis is performed in real-time. Our system uses secure API authentication and 
            follows industry best practices for data protection.
          </p>
        </div>

        <div className="content-card">
          <h2>Version Information</h2>
          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-value">v1.0</div>
              <div className="metric-label">Current Version</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">2024</div>
              <div className="metric-label">Release Year</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">MIT</div>
              <div className="metric-label">License</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">Active</div>
              <div className="metric-label">Development Status</div>
            </div>
          </div>
        </div>

        <div className="content-card">
          <h2>Support & Contact</h2>
          <p>
            Need help or have questions? Our team is here to support you. For technical issues, 
            feature requests, or general inquiries, please reach out through our support channels.
          </p>
          <div className="text-center mt-3">
            <button className="btn btn-primary">Contact Support</button>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default About; 