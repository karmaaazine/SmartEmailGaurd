#!/usr/bin/env python3
"""
Setup test script for Smart Email Guardian
Verifies that all components can be imported and basic functionality works.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all modules can be imported successfully."""
    print("🔍 Testing imports...")
    
    try:
        # Test AI module
        sys.path.append(str(Path(__file__).parent / "ai"))
        from ai.email_guard import analyze_email, EmailGuardAI
        print("✅ AI module imported successfully")
        
        # Test basic AI functionality
        result = analyze_email("Hello, this is a test email.")
        assert isinstance(result, dict)
        assert 'classification' in result
        assert 'confidence' in result
        print("✅ AI analysis function works")
        
    except Exception as e:
        print(f"❌ AI module import failed: {e}")
        return False
    
    try:
        # Test CLI tool
        from email_guard import read_input, format_output
        print("✅ CLI module imported successfully")
    except Exception as e:
        print(f"❌ CLI module import failed: {e}")
        return False
    
    try:
        # Test backend dependencies
        import fastapi
        import uvicorn
        import pydantic
        print("✅ Backend dependencies imported successfully")
    except Exception as e:
        print(f"❌ Backend dependencies import failed: {e}")
        return False
    
    try:
        # Test frontend dependencies
        import streamlit
        import requests
        print("✅ Frontend dependencies imported successfully")
    except Exception as e:
        print(f"❌ Frontend dependencies import failed: {e}")
        return False
    
    try:
        # Test Gmail integration dependencies
        import google.auth
        import googleapiclient
        print("✅ Gmail integration dependencies imported successfully")
    except Exception as e:
        print(f"❌ Gmail integration dependencies import failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test that all required files exist."""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "requirements.txt",
        "email_guard.py",
        "ai/email_guard.py",
        "backend/app.py",
        "frontend/app.py",
        "gmail_integration/gmail_reader.py",
        "tests/test_email_guard.py",
        "docs/README.md",
        "docs/security_notes.md",
        "docs/reflection.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality of the AI module."""
    print("\n🧪 Testing basic functionality...")
    
    try:
        from backend.ai.email_guard import analyze_email
        
        # Test legitimate email
        legitimate_email = """
        Hi John,
        
        I hope this email finds you well. I wanted to follow up on our meeting from last week.
        
        Best regards,
        Sarah
        """
        
        result = analyze_email(legitimate_email)
        print(f"✅ Legitimate email test: {result['classification']} ({result['confidence']:.1%})")
        
        # Test suspicious email
        suspicious_email = """
        Dear Customer,
        
        Your account has been suspended. Please verify your identity immediately.
        
        Click here: http://suspicious-link.com
        
        Best regards,
        Security Team
        """
        
        result = analyze_email(suspicious_email)
        print(f"✅ Suspicious email test: {result['classification']} ({result['confidence']:.1%})")
        
        # Test empty email
        result = analyze_email("")
        print(f"✅ Empty email test: {result['classification']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🛡️ Smart Email Guardian - Setup Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please check your installation.")
        return False
    
    # Test file structure
    if not test_file_structure():
        print("\n❌ File structure tests failed. Please check your project setup.")
        return False
    
    # Test basic functionality
    if not test_basic_functionality():
        print("\n❌ Basic functionality tests failed. Please check your AI module.")
        return False
    
    print("\n🎉 All tests passed! Your Smart Email Guardian setup is ready.")
    print("\n📋 Next steps:")
    print("1. Start the backend: cd backend && python app.py")
    print("2. Start the frontend: cd frontend && streamlit run app.py")
    print("3. Test the CLI: python email_guard.py -h")
    print("4. Run unit tests: pytest tests/")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 