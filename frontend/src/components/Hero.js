import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const Hero = () => {
  return (
    <section className="hero-section">
      <div className="hero-content">
        <motion.h3
          className="hero-headline"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          Stay One Step Ahead of <span className="highlight">Scammers</span> 
        </motion.h3>
        
        <motion.p
          className="hero-description"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          Catch A Phish is your smart shield against phishing and scam emails. 
          Using advanced AI detection, it analyzes suspicious messages in real time 
          to help you stay safe, informed, and one step ahead of cyber threats — because your inbox deserves protection.
        </motion.p>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          <Link to="/scanner" className="hero-cta">
            Get started
          </Link>
        </motion.div>
      </div>

      <div className="hero-visual">
        <motion.div
          className="woman-illustration"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, delay: 0.5 }}
        >
          <div className="woman-outline">
            {/* Woman's hair */}
            <div className="woman-hair"></div>
            
            {/* Woman's head */}
            <div className="woman-head">
              {/* Eyes */}
              <div className="woman-eyes">
                <div className="eye"></div>
                <div className="eye"></div>
              </div>
              {/* Nose */}
              <div className="woman-nose"></div>
            </div>
            
            {/* Woman's body */}
            <div className="woman-body"></div>
            
            {/* Woman's arms */}
            <div className="woman-arms">
              <div className="arm-left"></div>
              <div className="arm-right"></div>
            </div>
            
            {/* Smartphone */}
            <div className="smartphone">
              <div className="smartphone-screen"></div>
              <div className="smartphone-camera"></div>
            </div>
            
            {/* Woman's legs */}
            <div className="woman-legs">
              <div className="leg-left"></div>
              <div className="leg-right"></div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Hero; 