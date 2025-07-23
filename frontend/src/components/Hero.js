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
        className="photo-wrapper"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 1, delay: 0.5 }}
      >
        <img
          src="/woman.png"
          alt="Woman holding smartphone illustration"
          className="photo-image"
          style={{
            maxWidth: '300px',      // or another value that looks good
            height: 'auto',
            marginTop: '40px',      // pushes the image down from the nav
            display: 'block'
          }}
        />
      </motion.div>
    </div>

    </section>
  );
};

export default Hero; 