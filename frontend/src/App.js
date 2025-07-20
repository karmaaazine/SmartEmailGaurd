import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Hero from './components/Hero';
import EmailScanner from './components/EmailScanner';
import ScanHistory from './components/ScanHistory';
import Statistics from './components/Statistics';
import About from './components/About';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Navigation />
        
        <Routes>
          <Route path="/" element={<Hero />} />
          <Route path="/scanner" element={<EmailScanner />} />
          <Route path="/history" element={<ScanHistory />} />
          <Route path="/stats" element={<Statistics />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 