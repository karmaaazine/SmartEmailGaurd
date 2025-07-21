import React, { useState } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import ResultDisplay from './ResultDisplay';

const EmailScanner = () => {
  const [emailContent, setEmailContent] = useState('');
  const [inputMethod, setInputMethod] = useState('manual');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Determine API base URL - try HTTPS first, fallback to HTTP
  const getApiBaseUrl = () => {
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;
    
    // If we're on HTTPS, try HTTPS API first
    if (protocol === 'https:') {
      return `https://${hostname}:8443`;
    }
    
    // Fallback to HTTP
    return `http://${hostname}:8000`;
  };

  const sampleEmails = {
    'safe': {
      label: 'Safe Email',
      content: `Hi John,

I hope this email finds you well. I wanted to follow up on our meeting from last week regarding the project timeline.

The team has made good progress and we're on track to meet our deadline. Could you please review the attached documents and let me know if you have any questions?

Best regards,
Sarah`
    },
    'suspicious': {
      label: 'Suspicious Email',
      content: `Dear Customer,

Your account has been temporarily suspended due to suspicious activity. Please verify your identity immediately by clicking the link below.

Click here to verify: http://secure-bank-verify.com/login

This is urgent and requires immediate attention.

Best regards,
Security Team`
    },
    'phishing': {
      label: 'Phishing Email',
      content: `URGENT: Your account has been COMPROMISED!

Dear valued customer,

We have detected unauthorized access to your account. Your account has been SUSPENDED immediately for security reasons.

To restore access, please CLICK HERE NOW and verify your personal information including:
- Full name
- Date of birth  
- Social security number
- Credit card details
- Password

This is URGENT! Your account will be permanently deleted if you don't act within 24 hours.

Click here: http://secure-verify-now.com/restore

Best regards,
Bank Security Team`
    },
    'spam': {
      label: 'Spam Email',
      content: `🔥🔥🔥 LIMITED TIME OFFER! 🔥🔥🔥

Dear Friend,

You won't BELIEVE this amazing opportunity! We're giving away FREE iPhones to the first 100 people who respond!

🎉 ACT NOW! 🎉
🎉 DON'T MISS OUT! 🎉
🎉 LIMITED TIME ONLY! 🎉

Click here to claim your FREE iPhone: http://free-iphone-now.com

This offer expires in 2 hours! Don't wait!

Best regards,
Marketing Team`
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setEmailContent(e.target.result);
      };
      reader.readAsText(file);
    }
  };

  const handleSampleEmail = (type) => {
    setEmailContent(sampleEmails[type].content);
  };

  const scanEmail = async () => {
    if (!emailContent.trim()) {
      setError('Please enter some email content to scan.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const apiBaseUrl = getApiBaseUrl();
      const response = await axios.post(`${apiBaseUrl}/scan`, {
        content: emailContent,
        user_id: 'beach_user'
      }, {
        headers: {
          'x-api-key': 'salmas_email_guard'
        },
        // Handle self-signed certificates in development
        httpsAgent: window.location.protocol === 'https:' ? {
          rejectUnauthorized: false
        } : undefined
      });

      setResult(response.data);
    } catch (err) {
      if (err.code === 'CERT_HAS_EXPIRED' || err.code === 'UNABLE_TO_VERIFY_LEAF_SIGNATURE') {
        setError('SSL certificate issue. This is normal for development with self-signed certificates. Please accept the certificate warning in your browser.');
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else if (err.code === 'ECONNREFUSED') {
        setError('Could not connect to the server. Please ensure the backend is running.');
      } else {
        setError(err.message || 'Failed to analyze email. Please check your connection.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="page-hero">
        <h1>Email Security Scanner</h1>
        <p>Analyze your emails for phishing, spam, and security threats using our AI-powered detection system.</p>
      </div>

      <motion.div
        className="form-container"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Input Method Selection */}
        <div className="form-group">
          <label className="form-label">Choose Input Method</label>
          <div className="input-method-selector">
            <label className="method-option">
              <input
                type="radio"
                name="inputMethod"
                value="manual"
                checked={inputMethod === 'manual'}
                onChange={(e) => setInputMethod(e.target.value)}
              />
              <span className="method-label">Manual Input</span>
            </label>
            <label className="method-option">
              <input
                type="radio"
                name="inputMethod"
                value="file"
                checked={inputMethod === 'file'}
                onChange={(e) => setInputMethod(e.target.value)}
              />
              <span className="method-label">File Upload</span>
            </label>
          </div>
        </div>

        {/* Email Input */}
        {inputMethod === 'manual' ? (
          <div className="form-group">
            <label className="form-label">Email Content</label>
            <textarea
              className="form-textarea"
              value={emailContent}
              onChange={(e) => setEmailContent(e.target.value)}
              placeholder="Paste your email content here to analyze for security threats..."
            />
          </div>
        ) : (
          <div className="form-group">
            <label className="form-label">Upload Email File</label>
            <input
              type="file"
              accept=".txt,.eml"
              onChange={handleFileUpload}
              className="form-input"
            />
            {emailContent && (
              <div className="mt-2">
                <label className="form-label">File Content Preview</label>
                <textarea
                  className="form-textarea"
                  value={emailContent}
                  onChange={(e) => setEmailContent(e.target.value)}
                  readOnly
                />
              </div>
            )}
          </div>
        )}

        {/* Sample Emails */}
        <div className="form-group">
          <label className="form-label">Test with Sample Emails</label>
          <div className="sample-buttons">
            {Object.entries(sampleEmails).map(([type, email]) => (
              <button
                key={type}
                className="btn btn-secondary sample-btn"
                onClick={() => handleSampleEmail(type)}
              >
                {email.label}
              </button>
            ))}
          </div>
        </div>

        {/* Scan Button */}
        <div className="text-center">
          <button
            className="btn btn-primary"
            onClick={scanEmail}
            disabled={isLoading || !emailContent.trim()}
          >
            {isLoading ? (
              <>
                <span className="loading-spinner"></span>
                Analyzing email...
              </>
            ) : (
              'Scan Email'
            )}
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <motion.div
            className="error-message"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="result-box result-suspicious">
              <h3>⚠️ Error</h3>
              <p>{error}</p>
            </div>
          </motion.div>
        )}

        {/* Result Display */}
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <ResultDisplay result={result} />
          </motion.div>
        )}
      </motion.div>
    </div>
  );
};

export default EmailScanner; 