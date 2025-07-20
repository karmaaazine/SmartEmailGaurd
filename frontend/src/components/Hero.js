import React from 'react';
import { motion } from 'framer-motion';

const Hero = () => {
  return (
    <motion.div
      className="hero-section"
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
    >
      <motion.h1
        className="hero-title"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        🎣 Catch a Phish!
      </motion.h1>
      
      <motion.p
        className="hero-subtitle"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.4 }}
      >
        Don't get hooked by phishing emails! 🏖️
      </motion.p>
      
      <motion.p
        className="hero-description"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.6 }}
      >
        Your beach-side email security guard protecting you from the deep web's dangerous waters
      </motion.p>
      
      <motion.div
        className="hero-features"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.8 }}
      >
        <div className="feature-grid">
          <div className="feature-item">
            <span className="feature-icon">🐠</span>
            <span className="feature-text">AI-Powered Analysis</span>
          </div>
          <div className="feature-item">
            <span className="feature-icon">🦈</span>
            <span className="feature-text">Multi-Threat Detection</span>
          </div>
          <div className="feature-item">
            <span className="feature-icon">🌊</span>
            <span className="feature-text">Beautiful Interface</span>
          </div>
          <div className="feature-item">
            <span className="feature-icon">🎣</span>
            <span className="feature-text">Easy to Use</span>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default Hero; 