import React from 'react';
import { motion } from 'framer-motion';

const About = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="beach-card">
        <h2>🏖️ About Catch a Phish!</h2>
        <p>Your beach-side email security guard protecting you from the deep web's dangerous waters</p>
      </div>

      <div className="beach-card">
        <h3>🌊 What is Catch a Phish!?</h3>
        <p>
          Catch a Phish! is your friendly beach-side email security guard that helps detect spam, 
          phishing, and other security threats in email content. Just like a lifeguard watches over 
          swimmers, we watch over your emails!
        </p>
      </div>

      <div className="beach-card">
        <h3>🎣 Features</h3>
        <div className="features-list">
          <div className="feature-item">
            <span className="feature-icon">🐠</span>
            <div className="feature-content">
              <h4>AI-Powered Analysis</h4>
              <p>Uses advanced machine learning to analyze email content</p>
            </div>
          </div>
          <div className="feature-item">
            <span className="feature-icon">🦈</span>
            <div className="feature-content">
              <h4>Multi-Threat Detection</h4>
              <p>Identifies spam, phishing, and suspicious emails</p>
            </div>
          </div>
          <div className="feature-item">
            <span className="feature-icon">📊</span>
            <div className="feature-content">
              <h4>Detailed Reports</h4>
              <p>Provides confidence scores and explanations for each catch</p>
            </div>
          </div>
          <div className="feature-item">
            <span className="feature-icon">🌊</span>
            <div className="feature-content">
              <h4>Beautiful Interface</h4>
              <p>Enjoy a relaxing beach theme while staying secure</p>
            </div>
          </div>
          <div className="feature-item">
            <span className="feature-icon">🎣</span>
            <div className="feature-content">
              <h4>Multiple Input Methods</h4>
              <p>Support for manual input and file uploads</p>
            </div>
          </div>
          <div className="feature-item">
            <span className="feature-icon">📈</span>
            <div className="feature-content">
              <h4>Catch History</h4>
              <p>Keep track of all your catches for analysis</p>
            </div>
          </div>
        </div>
      </div>

      <div className="beach-card">
        <h3>🏖️ How it Works</h3>
        <div className="workflow-steps">
          <div className="workflow-step">
            <div className="step-number">1</div>
            <div className="step-content">
              <h4>Cast Your Net</h4>
              <p>Paste email content or upload a file</p>
            </div>
          </div>
          <div className="workflow-step">
            <div className="step-number">2</div>
            <div className="step-content">
              <h4>AI Analysis</h4>
              <p>Our lifeguards analyze the content using multiple factors</p>
            </div>
          </div>
          <div className="workflow-step">
            <div className="step-number">3</div>
            <div className="step-content">
              <h4>Catch Report</h4>
              <p>Content is classified as safe, suspicious, spam, or phishing</p>
            </div>
          </div>
          <div className="workflow-step">
            <div className="step-number">4</div>
            <div className="step-content">
              <h4>Results</h4>
              <p>Get detailed analysis with confidence scores and explanations</p>
            </div>
          </div>
        </div>
      </div>

      <div className="beach-card">
        <h3>🛠️ Technology Stack</h3>
        <div className="tech-grid">
          <div className="tech-item">
            <h4>Backend</h4>
            <p>FastAPI with Python</p>
          </div>
          <div className="tech-item">
            <h4>AI Model</h4>
            <p>HuggingFace Transformers (DistilBERT)</p>
          </div>
          <div className="tech-item">
            <h4>Frontend</h4>
            <p>React with beach theme</p>
          </div>
          <div className="tech-item">
            <h4>Authentication</h4>
            <p>API Key-based security</p>
          </div>
          <div className="tech-item">
            <h4>Charts</h4>
            <p>Recharts for data visualization</p>
          </div>
          <div className="tech-item">
            <h4>Animations</h4>
            <p>Framer Motion for smooth interactions</p>
          </div>
        </div>
      </div>

      <div className="beach-card">
        <h3>🔒 Security</h3>
        <div className="security-features">
          <div className="security-item">
            <span className="security-icon">🔐</span>
            <div className="security-content">
              <h4>API Authentication</h4>
              <p>All API calls require authentication with secure API keys</p>
            </div>
          </div>
          <div className="security-item">
            <span className="security-icon">🛡️</span>
            <div className="security-content">
              <h4>Input Validation</h4>
              <p>Email content is processed securely with proper validation</p>
            </div>
          </div>
          <div className="security-item">
            <span className="security-icon">🗑️</span>
            <div className="security-content">
              <h4>No Data Storage</h4>
              <p>No data is stored permanently (in-memory only)</p>
            </div>
          </div>
          <div className="security-item">
            <span className="security-icon">🔒</span>
            <div className="security-content">
              <h4>HTTPS Ready</h4>
              <p>Backend configured for secure connections</p>
            </div>
          </div>
        </div>
      </div>

      <div className="beach-card">
        <h3>🏄‍♂️ Version</h3>
        <p><strong>Catch a Phish! v1.0.0 - Beach Edition</strong></p>
        <p>Built with ❤️ for email security and beach vibes! 🏖️🎣</p>
      </div>

      <div className="beach-card">
        <h3>📞 Support</h3>
        <p>
          If you have any questions or need help with Catch a Phish!, feel free to reach out to our 
          beach patrol team. We're here to help keep your digital shores safe!
        </p>
        <div className="contact-info">
          <p>🌊 Email: support@catchaphish.com</p>
          <p>🏖️ Website: www.catchaphish.com</p>
          <p>🎣 GitHub: github.com/catchaphish</p>
        </div>
      </div>
    </motion.div>
  );
};

export default About; 