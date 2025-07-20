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

  const sampleEmails = {
    'safe': {
      icon: '🐠',
      label: 'Safe Email',
      content: `Hi John,

I hope this email finds you well. I wanted to follow up on our meeting from last week regarding the project timeline.

The team has made good progress and we're on track to meet our deadline. Could you please review the attached documents and let me know if you have any questions?

Best regards,
Sarah`
    },
    'suspicious': {
      icon: '🦈',
      label: 'Suspicious Email',
      content: `Dear Customer,

Your account has been temporarily suspended due to suspicious activity. Please verify your identity immediately by clicking the link below.

Click here to verify: http://secure-bank-verify.com/login

This is urgent and requires immediate attention.

Best regards,
Security Team`
    },
    'phishing': {
      icon: '🦑',
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
      icon: '🐙',
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
      const response = await axios.post('/scan', {
        content: emailContent,
        user_id: 'beach_user'
      }, {
        headers: {
          'x-api-key': 'salmas_email_guard'
        }
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze email. Please check your connection.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="beach-card">
        <h2>🎣 Cast Your Net</h2>
        <p>Drop your suspicious email into our security net and let our AI lifeguards analyze it!</p>
      </div>

      {/* Input Method Selection */}
      <div className="beach-card">
        <h3>🌊 Choose Your Fishing Method</h3>
        <div className="input-method-selector">
          <label className="method-option">
            <input
              type="radio"
              name="inputMethod"
              value="manual"
              checked={inputMethod === 'manual'}
              onChange={(e) => setInputMethod(e.target.value)}
            />
            <span className="method-label">📝 Manual Cast</span>
          </label>
          <label className="method-option">
            <input
              type="radio"
              name="inputMethod"
              value="file"
              checked={inputMethod === 'file'}
              onChange={(e) => setInputMethod(e.target.value)}
            />
            <span className="method-label">📁 File Drop</span>
          </label>
        </div>
      </div>

      {/* Email Input */}
      <div className="beach-card">
        <h3>🌊 Drop Your Email Here</h3>
        
        {inputMethod === 'manual' ? (
          <div className="form-group">
            <label className="form-label">Email Content:</label>
            <textarea
              className="form-textarea"
              value={emailContent}
              onChange={(e) => setEmailContent(e.target.value)}
              placeholder="Drop your suspicious email here and let our lifeguards check it out! 🏖️"
            />
          </div>
        ) : (
          <div className="form-group">
            <label className="form-label">Upload Email File:</label>
            <input
              type="file"
              accept=".txt,.eml"
              onChange={handleFileUpload}
              className="form-input"
            />
            {emailContent && (
              <div className="mt-2">
                <label className="form-label">File Content Preview:</label>
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
        <div className="sample-emails">
          <h4>🧪 Test Waters</h4>
          <p>Try these sample emails to test our security net:</p>
          <div className="sample-buttons">
            {Object.entries(sampleEmails).map(([type, email]) => (
              <button
                key={type}
                className="btn btn-secondary sample-btn"
                onClick={() => handleSampleEmail(type)}
              >
                {email.icon} {email.label}
              </button>
            ))}
          </div>
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
              🌊 Our lifeguards are analyzing your email...
            </>
          ) : (
            '🎣 Cast Security Net'
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
          <div className="beach-card">
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
  );
};

export default EmailScanner; 