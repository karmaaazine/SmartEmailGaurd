"""
AI-powered email analysis module using HuggingFace Transformers.
Analyzes email content to detect spam, phishing, or legitimate emails.
"""

import re
from typing import Dict, List, Tuple
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

class EmailGuardAI:
    """AI-powered email analysis using pre-trained transformer models."""
    
    def __init__(self):
        """Initialize the AI model and tokenizer."""
        self.model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self.classifier = None
        self.tokenizer = None
        self._load_model()
        
    def _load_model(self):
        """Load the pre-trained model and tokenizer."""
        try:
            print("Loading AI model...")
            self.classifier = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                device=-1  # CPU only
            )
            print("AI model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def _extract_features(self, text: str) -> Dict[str, float]:
        """Extract features from email text for analysis."""
        features = {
            'length': len(text),
            'word_count': len(text.split()),
            'uppercase_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0,
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'url_count': len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)),
            'email_count': len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)),
            'money_mentions': len(re.findall(r'\$[\d,]+|\d+\s*(?:dollars?|euros?|pounds?)', text, re.IGNORECASE)),
            'urgent_words': len(re.findall(r'\b(?:urgent|immediate|action|required|account|suspended|verify|confirm|password|login|security)\b', text, re.IGNORECASE))
        }
        return features
    
    def _classify_content(self, text: str) -> Tuple[str, float]:
        """Classify email content using the transformer model."""
        try:
            result = self.classifier(text[:512])  # Limit to 512 tokens
            # Map sentiment to our categories
            if result[0]['label'] == 'POSITIVE':
                return 'legitimate', result[0]['score']
            else:
                return 'suspicious', result[0]['score']
        except Exception as e:
            print(f"Error in classification: {e}")
            return 'unknown', 0.0
    
    def _detect_phishing_indicators(self, text: str) -> List[str]:
        """Detect specific phishing indicators in the text."""
        indicators = []
        
        # Common phishing patterns
        patterns = {
            'urgent_action': r'\b(?:urgent|immediate|action required|account suspended|verify now)\b',
            'personal_info': r'\b(?:password|login|account|verify|confirm|personal information)\b',
            'financial': r'\b(?:bank|credit card|account|payment|transfer|money)\b',
            'suspicious_links': r'\b(?:click here|login here|verify here|secure link)\b',
            'grammar_errors': r'\b(?:dear sir|madam|kindly|please find|attached herewith)\b',
            'generic_greeting': r'^(?:dear user|dear customer|dear sir|dear madam)',
        }
        
        for indicator, pattern in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                indicators.append(indicator)
        
        return indicators
    
    def analyze_email(self, text: str) -> Dict:
        """
        Analyze email content and return classification results.
        
        Args:
            text (str): Email content to analyze
            
        Returns:
            Dict: Analysis results with classification, confidence, and explanation
        """
        if not text or not text.strip():
            return {
                'classification': 'invalid',
                'confidence': 0.0,
                'explanation': 'Empty or invalid email content provided.',
                'features': {},
                'indicators': []
            }
        
        # Clean and normalize text
        text = text.strip()
        
        # Extract features
        features = self._extract_features(text)
        
        # Get AI classification
        classification, confidence = self._classify_content(text)
        
        # Detect phishing indicators
        indicators = self._detect_phishing_indicators(text)
        
        # Determine final classification based on multiple factors
        final_classification = self._determine_final_classification(
            classification, confidence, features, indicators
        )
        
        # Generate explanation
        explanation = self._generate_explanation(
            final_classification, features, indicators, confidence
        )
        
        return {
            'classification': final_classification,
            'confidence': confidence,
            'explanation': explanation,
            'features': features,
            'indicators': indicators,
            'raw_text_length': len(text)
        }
    
    def _determine_final_classification(self, ai_class: str, confidence: float, 
                                      features: Dict, indicators: List[str]) -> str:
        """Determine final classification based on multiple factors."""
        
        # High confidence AI classification
        if confidence > 0.8:
            if ai_class == 'legitimate':
                return 'legitimate'
            else:
                return 'suspicious'
        
        # Check for strong phishing indicators
        if len(indicators) >= 3:
            return 'phishing'
        
        # Check for suspicious features
        suspicious_score = 0
        if features['urgent_words'] > 2:
            suspicious_score += 2
        if features['money_mentions'] > 0:
            suspicious_score += 1
        if features['url_count'] > 2:
            suspicious_score += 1
        if features['uppercase_ratio'] > 0.3:
            suspicious_score += 1
        
        if suspicious_score >= 3:
            return 'spam'
        elif suspicious_score >= 1:
            return 'suspicious'
        else:
            return 'legitimate'
    
    def _generate_explanation(self, classification: str, features: Dict, 
                            indicators: List[str], confidence: float) -> str:
        """Generate human-readable explanation for the classification."""
        
        explanations = {
            'legitimate': f"This email appears to be legitimate (confidence: {confidence:.2f}).",
            'suspicious': f"This email shows suspicious characteristics (confidence: {confidence:.2f}).",
            'spam': "This email appears to be spam based on multiple indicators.",
            'phishing': "This email shows strong phishing indicators and should be avoided.",
            'invalid': "Invalid or empty email content provided."
        }
        
        base_explanation = explanations.get(classification, "Unable to classify email.")
        
        if indicators:
            indicator_text = ", ".join(indicators)
            base_explanation += f" Detected indicators: {indicator_text}."
        
        if features['urgent_words'] > 0:
            base_explanation += f" Contains {features['urgent_words']} urgent/suspicious words."
        
        return base_explanation

# Global instance for easy access
email_guard_ai = EmailGuardAI()

def analyze_email(text: str) -> Dict:
    """
    Convenience function to analyze email content.
    
    Args:
        text (str): Email content to analyze
        
    Returns:
        Dict: Analysis results
    """
    return email_guard_ai.analyze_email(text) 