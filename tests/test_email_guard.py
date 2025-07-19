"""
Unit tests for Smart Email Guardian AI module.
"""

import pytest
import sys
from pathlib import Path

# Add the ai directory to the path
sys.path.append(str(Path(__file__).parent.parent / "ai"))

from ai.email_guard import analyze_email, EmailGuardAI

class TestEmailGuardAI:
    """Test cases for EmailGuardAI class."""
    
    def test_analyze_email_legitimate(self):
        """Test analysis of a legitimate email."""
        email_text = """
        Hi John,
        
        I hope this email finds you well. I wanted to follow up on our meeting from last week regarding the project timeline.
        
        The team has made good progress and we're on track to meet our deadline. Could you please review the attached documents and let me know if you have any questions?
        
        Best regards,
        Sarah
        """
        
        result = analyze_email(email_text)
        
        # Check required keys
        assert 'classification' in result
        assert 'confidence' in result
        assert 'explanation' in result
        assert 'features' in result
        assert 'indicators' in result
        
        # Check data types
        assert isinstance(result['classification'], str)
        assert isinstance(result['confidence'], float)
        assert isinstance(result['explanation'], str)
        assert isinstance(result['features'], dict)
        assert isinstance(result['indicators'], list)
        
        # Check confidence range
        assert 0.0 <= result['confidence'] <= 1.0
        
        # Check features
        features = result['features']
        assert 'length' in features
        assert 'word_count' in features
        assert 'uppercase_ratio' in features
        assert 'exclamation_count' in features
        assert 'question_count' in features
        assert 'url_count' in features
        assert 'email_count' in features
        assert 'money_mentions' in features
        assert 'urgent_words' in features
    
    def test_analyze_email_suspicious(self):
        """Test analysis of a suspicious email."""
        email_text = """
        Dear Customer,
        
        Your account has been temporarily suspended due to suspicious activity. Please verify your identity immediately by clicking the link below.
        
        Click here to verify: http://secure-bank-verify.com/login
        
        This is urgent and requires immediate attention.
        
        Best regards,
        Security Team
        """
        
        result = analyze_email(email_text)
        
        # Check required keys
        assert 'classification' in result
        assert 'confidence' in result
        assert 'explanation' in result
        assert 'features' in result
        assert 'indicators' in result
        
        # Should detect some indicators
        assert len(result['indicators']) > 0
        
        # Should have URLs detected
        assert result['features']['url_count'] > 0
    
    def test_analyze_email_phishing(self):
        """Test analysis of a phishing email."""
        email_text = """
        URGENT: Your account has been COMPROMISED!
        
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
        Bank Security Team
        """
        
        result = analyze_email(email_text)
        
        # Check required keys
        assert 'classification' in result
        assert 'confidence' in result
        assert 'explanation' in result
        assert 'features' in result
        assert 'indicators' in result
        
        # Should detect multiple indicators
        assert len(result['indicators']) >= 2
        
        # Should have high urgent words count
        assert result['features']['urgent_words'] > 0
        
        # Should have URLs detected
        assert result['features']['url_count'] > 0
    
    def test_analyze_email_spam(self):
        """Test analysis of a spam email."""
        email_text = """
        🔥🔥🔥 LIMITED TIME OFFER! 🔥🔥🔥
        
        Dear Friend,
        
        You won't BELIEVE this amazing opportunity! We're giving away FREE iPhones to the first 100 people who respond!
        
        🎉 ACT NOW! 🎉
        🎉 DON'T MISS OUT! 🎉
        🎉 LIMITED TIME ONLY! 🎉
        
        Click here to claim your FREE iPhone: http://free-iphone-now.com
        
        This offer expires in 2 hours! Don't wait!
        
        Best regards,
        Marketing Team
        """
        
        result = analyze_email(email_text)
        
        # Check required keys
        assert 'classification' in result
        assert 'confidence' in result
        assert 'explanation' in result
        assert 'features' in result
        assert 'indicators' in result
        
        # Should have high exclamation count
        assert result['features']['exclamation_count'] > 0
        
        # Should have URLs detected
        assert result['features']['url_count'] > 0
    
    def test_analyze_email_empty(self):
        """Test analysis of empty email."""
        result = analyze_email("")
        
        assert result['classification'] == 'invalid'
        assert result['confidence'] == 0.0
        assert 'Empty or invalid email content' in result['explanation']
    
    def test_analyze_email_whitespace(self):
        """Test analysis of whitespace-only email."""
        result = analyze_email("   \n\t   ")
        
        assert result['classification'] == 'invalid'
        assert result['confidence'] == 0.0
        assert 'Empty or invalid email content' in result['explanation']
    
    def test_analyze_email_none(self):
        """Test analysis of None input."""
        result = analyze_email(None)
        
        assert result['classification'] == 'invalid'
        assert result['confidence'] == 0.0
        assert 'Empty or invalid email content' in result['explanation']
    
    def test_email_guard_ai_initialization(self):
        """Test EmailGuardAI class initialization."""
        ai = EmailGuardAI()
        
        assert ai.model_name == "distilbert-base-uncased-finetuned-sst-2-english"
        assert ai.classifier is not None
    
    def test_feature_extraction(self):
        """Test feature extraction functionality."""
        ai = EmailGuardAI()
        
        test_text = "Hello! This is a test email with http://example.com and some UPPERCASE text."
        features = ai._extract_features(test_text)
        
        assert features['length'] == len(test_text)
        assert features['word_count'] == 12  # Count words
        assert features['url_count'] == 1    # One URL
        assert features['exclamation_count'] == 1  # One exclamation mark
        assert features['uppercase_ratio'] > 0     # Some uppercase letters
    
    def test_phishing_indicators_detection(self):
        """Test phishing indicators detection."""
        ai = EmailGuardAI()
        
        # Test with phishing indicators
        phishing_text = "Dear customer, your account has been suspended. Please verify your password and login immediately."
        indicators = ai._detect_phishing_indicators(phishing_text)
        
        assert len(indicators) > 0
        assert any('personal_info' in indicator or 'urgent_action' in indicator for indicator in indicators)
        
        # Test with legitimate text
        legitimate_text = "Hi John, thanks for the meeting yesterday. Let's catch up next week."
        indicators = ai._detect_phishing_indicators(legitimate_text)
        
        # Should have fewer or no indicators
        assert len(indicators) == 0 or len(indicators) < 2

def test_analyze_email_function():
    """Test the convenience analyze_email function."""
    email_text = "Hello, this is a test email."
    result = analyze_email(email_text)
    
    # Check that it returns a valid result
    assert isinstance(result, dict)
    assert 'classification' in result
    assert 'confidence' in result
    assert 'explanation' in result

if __name__ == "__main__":
    pytest.main([__file__]) 