"""
Streamlit Frontend for Smart Email Guardian
Provides a user-friendly web interface for email analysis.
"""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import Dict, Optional

# Configuration
BACKEND_URL = "http://localhost:8000"
API_KEY = "salmas_email_guard"  # In production, use environment variables

# Page configuration
st.set_page_config(
    page_title="Smart Email Guardian",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .result-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .legitimate {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .suspicious {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    .spam {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .phishing {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def call_backend_api(endpoint: str, data: Optional[Dict] = None, method: str = "GET") -> Optional[Dict]:
    """Make API call to backend."""
    try:
        headers = {"x-api-key": API_KEY}
        
        if method == "GET":
            response = requests.get(f"{BACKEND_URL}{endpoint}", headers=headers)
        elif method == "POST":
            response = requests.post(f"{BACKEND_URL}{endpoint}", json=data, headers=headers)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
        return None

def display_scan_result(result: Dict):
    """Display scan results in a formatted way."""
    classification = result.get("classification", "unknown")
    confidence = result.get("confidence", 0.0)
    explanation = result.get("explanation", "")
    features = result.get("features", {})
    indicators = result.get("indicators", [])
    
    # Classification color mapping
    color_map = {
        "legitimate": "legitimate",
        "suspicious": "suspicious", 
        "spam": "spam",
        "phishing": "phishing"
    }
    
    css_class = color_map.get(classification, "suspicious")
    
    # Display result
    st.markdown(f"""
    <div class="result-box {css_class}">
        <h3>🔍 Analysis Result</h3>
        <p><strong>Classification:</strong> {classification.upper()}</p>
        <p><strong>Confidence:</strong> {confidence:.1%}</p>
        <p><strong>Explanation:</strong> {explanation}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display features
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Text Length", f"{features.get('length', 0):,} chars")
    
    with col2:
        st.metric("Word Count", features.get('word_count', 0))
    
    with col3:
        st.metric("URLs Found", features.get('url_count', 0))
    
    with col4:
        st.metric("Urgent Words", features.get('urgent_words', 0))
    
    # Display indicators if any
    if indicators:
        st.subheader("⚠️ Detected Indicators")
        for indicator in indicators:
            st.write(f"• {indicator}")

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🛡️ Smart Email Guardian</h1>', unsafe_allow_html=True)
    st.markdown("### AI-Powered Spam & Phishing Detection")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["📧 Email Scanner", "📊 Scan History", "📈 Statistics", "ℹ️ About"]
    )
    
    if page == "📧 Email Scanner":
        show_email_scanner()
    elif page == "📊 Scan History":
        show_scan_history()
    elif page == "📈 Statistics":
        show_statistics()
    elif page == "ℹ️ About":
        show_about()

def show_email_scanner():
    """Show the main email scanner interface."""
    st.header("📧 Email Scanner")
    
    # Input method selection
    input_method = st.radio(
        "Choose input method:",
        ["📝 Manual Input", "📁 File Upload"]
    )
    
    email_content = ""
    
    if input_method == "📝 Manual Input":
        st.subheader("Enter Email Content")
        email_content = st.text_area(
            "Paste your email content here:",
            height=300,
            placeholder="Paste the email content you want to analyze..."
        )
        
        # Sample emails for testing
        st.subheader("🧪 Sample Emails for Testing")
        sample_option = st.selectbox(
            "Choose a sample email:",
            ["None", "Legitimate Email", "Suspicious Email", "Phishing Email", "Spam Email"]
        )
        
        sample_emails = {
            "Legitimate Email": """Hi John,

I hope this email finds you well. I wanted to follow up on our meeting from last week regarding the project timeline.

The team has made good progress and we're on track to meet our deadline. Could you please review the attached documents and let me know if you have any questions?

Best regards,
Sarah""",
            
            "Suspicious Email": """Dear Customer,

Your account has been temporarily suspended due to suspicious activity. Please verify your identity immediately by clicking the link below.

Click here to verify: http://secure-bank-verify.com/login

This is urgent and requires immediate attention.

Best regards,
Security Team""",
            
            "Phishing Email": """URGENT: Your account has been COMPROMISED!

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
Bank Security Team""",
            
            "Spam Email": """🔥🔥🔥 LIMITED TIME OFFER! 🔥🔥🔥

Dear Friend,

You won't BELIEVE this amazing opportunity! We're giving away FREE iPhones to the first 100 people who respond!

🎉 ACT NOW! 🎉
🎉 DON'T MISS OUT! 🎉
🎉 LIMITED TIME ONLY! 🎉

Click here to claim your FREE iPhone: http://free-iphone-now.com

This offer expires in 2 hours! Don't wait!

Best regards,
Marketing Team"""
        }
        
        if sample_option != "None":
            email_content = sample_emails[sample_option]
            st.text_area("Sample email loaded:", email_content, height=200, disabled=True)
    
    else:  # File Upload
        st.subheader("Upload Email File")
        uploaded_file = st.file_uploader(
            "Choose a text file containing email content:",
            type=['txt', 'eml']
        )
        
        if uploaded_file is not None:
            email_content = uploaded_file.getvalue().decode("utf-8")
            st.text_area("File content:", email_content, height=200, disabled=True)
    
    # Scan button
    if st.button("🔍 Analyze Email", type="primary", disabled=not email_content.strip()):
        if email_content.strip():
            with st.spinner("Analyzing email content..."):
                # Call backend API
                result = call_backend_api(
                    "/scan",
                    {"content": email_content, "user_id": "streamlit_user"},
                    "POST"
                )
                
                if result:
                    st.success("Analysis completed!")
                    display_scan_result(result)
                else:
                    st.error("Failed to analyze email. Please check your connection to the backend.")

def show_scan_history():
    """Show scan history."""
    st.header("📊 Scan History")
    
    # Get scan history from backend
    history = call_backend_api("/history?limit=20")
    
    if history and history.get("scans"):
        scans = history["scans"]
        
        # Display summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Scans", history["total_count"])
        with col2:
            st.metric("Recent Scans", len(scans))
        with col3:
            if scans:
                avg_confidence = sum(scan["confidence"] for scan in scans) / len(scans)
                st.metric("Avg Confidence", f"{avg_confidence:.1%}")
        
        # Display scan list
        st.subheader("Recent Scans")
        for scan in scans:
            with st.expander(f"{scan['classification'].upper()} - {scan['timestamp'][:19]}"):
                display_scan_result(scan)
    else:
        st.info("No scan history available.")

def show_statistics():
    """Show statistics."""
    st.header("📈 Statistics")
    
    stats = call_backend_api("/stats")
    
    if stats:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Overall Statistics")
            st.metric("Total Scans", stats["total_scans"])
            if stats["recent_activity"]["last_24_hours"]:
                st.metric("Last 24 Hours", stats["recent_activity"]["last_24_hours"])
                st.metric("Avg Confidence", f"{stats['recent_activity']['average_confidence']:.1%}")
        
        with col2:
            st.subheader("Classifications")
            if stats["classifications"]:
                for classification, count in stats["classifications"].items():
                    st.metric(classification.title(), count)
            else:
                st.info("No classification data available.")
    else:
        st.error("Unable to load statistics.")

def show_about():
    """Show about page."""
    st.header("ℹ️ About Smart Email Guardian")
    
    st.markdown("""
    ### What is Smart Email Guardian?
    
    Smart Email Guardian is an AI-powered email analysis tool that helps detect spam, phishing, and other security threats in email content.
    
    ### Features
    
    - 🔍 **AI-Powered Analysis**: Uses advanced machine learning models to analyze email content
    - 🛡️ **Multi-Threat Detection**: Identifies spam, phishing, and suspicious emails
    - 📊 **Detailed Reports**: Provides confidence scores and explanations for each classification
    - 📈 **History Tracking**: Keeps track of all scans for analysis
    - 🔧 **Multiple Input Methods**: Support for manual input and file uploads
    
    ### How it Works
    
    1. **Input**: Paste email content or upload a file
    2. **Analysis**: Our AI model analyzes the content using multiple factors
    3. **Classification**: Content is classified as legitimate, suspicious, spam, or phishing
    4. **Results**: Get detailed analysis with confidence scores and explanations
    
    ### Technology Stack
    
    - **Backend**: FastAPI with Python
    - **AI Model**: HuggingFace Transformers (DistilBERT)
    - **Frontend**: Streamlit
    - **Authentication**: API Key-based security
    
    ### Security
    
    - All API calls require authentication
    - Email content is processed securely
    - No data is stored permanently (in-memory only)
    
    ### Version
    
    Smart Email Guardian v1.0.0
    """)

if __name__ == "__main__":
    main() 