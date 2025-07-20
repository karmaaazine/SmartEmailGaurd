"""
Catch a Phish! - Beach-themed Email Security & Phishing Detection App
A responsive web UI with playful ocean elements and serious anti-phishing features.
"""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import Dict, Optional

# Configuration
BACKEND_URL = "http://localhost:8000"
API_KEY = "salmas_email_guard"  # Updated to match backend

# Page configuration
st.set_page_config(
    page_title="Catch a Phish! 🎣",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beach theme - simplified for better text visibility
st.markdown("""
<style>
    /* Beach Theme Colors */
    :root {
        --ocean-blue: #1e3a8a;
        --sand-beige: #fef3c7;
        --coral-orange: #fb7185;
        --seafoam-green: #34d399;
        --sunset-yellow: #fbbf24;
        --wave-blue: #0ea5e9;
    }
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #0ea5e9 0%, #1e3a8a 100%);
        min-height: 100vh;
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #fef3c7 0%, #fbbf24 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 3px solid #fbbf24;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: bold;
        color: #1e3a8a !important;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #374151 !important;
        margin-bottom: 2rem;
    }
    
    /* Ocean wave divider */
    .wave-divider {
        height: 60px;
        background: linear-gradient(45deg, #0ea5e9, #1e3a8a);
        border-radius: 0 0 50% 50%;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Card styling */
    .beach-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fbbf24 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 3px solid #fbbf24;
    }
    
    /* Result boxes with beach theme */
    .result-box {
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        border: 3px solid;
        position: relative;
        overflow: hidden;
    }
    
    .result-box::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #fbbf24, #fb7185);
    }
    
    .legitimate {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        border-color: #34d399;
        color: #065f46 !important;
    }
    
    .suspicious {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        border-color: #fbbf24;
        color: #92400e !important;
    }
    
    .spam {
        background: linear-gradient(135deg, #fecaca, #fca5a5);
        border-color: #fb7185;
        color: #991b1b !important;
    }
    
    .phishing {
        background: linear-gradient(135deg, #fecaca, #f87171);
        border-color: #dc2626;
        color: #7f1d1d !important;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #0ea5e9;
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1e3a8a !important;
    }
    
    .metric-label {
        color: #374151 !important;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
        }
        
        .beach-card {
            padding: 1rem;
        }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3a8a 0%, #0ea5e9 100%);
    }
    
    /* Fish animation */
    @keyframes swim {
        0% { transform: translateX(-100px); }
        100% { transform: translateX(calc(100vw + 100px)); }
    }
    
    .swimming-fish {
        position: fixed;
        top: 20%;
        font-size: 2rem;
        animation: swim 15s linear infinite;
        z-index: -1;
    }
    
    /* Ensure text visibility */
    .stMarkdown, .stText, .stButton {
        color: inherit !important;
    }
    
    /* Override Streamlit's default text colors */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown p {
        color: inherit !important;
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
        st.error(f"🌊 Connection error: {e}")
        return None

def display_scan_result(result: Dict):
    """Display scan results with beach theme."""
    classification = result.get("classification", "unknown")
    confidence = result.get("confidence", 0.0)
    explanation = result.get("explanation", "")
    features = result.get("features", {})
    indicators = result.get("indicators", [])
    
    # Classification icons and colors
    classification_icons = {
        "legitimate": "🐠",
        "suspicious": "🦈", 
        "spam": "🐙",
        "phishing": "🦑"
    }
    
    icon = classification_icons.get(classification, "🐟")
    
    # Display result with beach theme using native Streamlit
    if classification == "legitimate":
        st.success(f"{icon} **Catch Report - SAFE**")
    elif classification == "suspicious":
        st.warning(f"{icon} **Catch Report - SUSPICIOUS**")
    elif classification == "spam":
        st.error(f"{icon} **Catch Report - SPAM**")
    elif classification == "phishing":
        st.error(f"{icon} **Catch Report - PHISHING**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Type", classification.upper())
        st.metric("Confidence", f"{confidence:.1%}")
    with col2:
        st.metric("Characters", f"{features.get('length', 0):,}")
        st.metric("Words", features.get('word_count', 0))
    
    st.info(f"**Analysis:** {explanation}")
    
    # Display additional metrics
    col3, col4 = st.columns(2)
    with col3:
        st.metric("Links Found", features.get('url_count', 0))
    with col4:
        st.metric("Red Flags", features.get('urgent_words', 0))
    
    # Display indicators
    if indicators:
        st.subheader("⚠️ Caught Red Flags")
        for indicator in indicators:
            st.write(f"🎯 {indicator.replace('_', ' ').title()}")

def main():
    """Main application function."""
    
    # Add floating fish animation
    st.markdown('<div class="swimming-fish">🐟</div>', unsafe_allow_html=True)
    
    # Hero section using native Streamlit
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🎣 Catch a Phish!</h1>
        <p class="hero-subtitle">Don't get hooked by phishing emails! 🏖️</p>
        <p style="font-size: 1.1rem; color: #6b7280;">
            Your beach-side email security guard protecting you from the deep web's dangerous waters
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Wave divider
    st.markdown('<div class="wave-divider">🌊</div>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(180deg, #1e3a8a 0%, #0ea5e9 100%); border-radius: 10px; color: white;">
        <h2>🏖️ Beach Patrol</h2>
        <p>Choose your security tool:</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.selectbox(
        "🌊 Navigation",
        ["🎣 Email Scanner", "📊 Catch History", "📈 Beach Stats", "ℹ️ About"]
    )
    
    if page == "🎣 Email Scanner":
        show_email_scanner()
    elif page == "📊 Catch History":
        show_scan_history()
    elif page == "📈 Beach Stats":
        show_statistics()
    elif page == "ℹ️ About":
        show_about()

def show_email_scanner():
    """Show the main email scanner interface with beach theme."""
    st.markdown("""
    <div class="beach-card">
        <h2 style="color: #6b7280;">🎣 Cast Your Net</h2>
        <p style="color: #374151;">Drop your suspicious email into our security net and let our AI lifeguards analyze it!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input method selection
    input_method = st.radio(
        "Choose your fishing method:",
        ["📝 Manual Cast", "📁 File Drop"]
    )
    
    email_content = ""
    
    if input_method == "📝 Manual Cast":
        st.markdown("""
        <div class="beach-card">
            <h3 style="color: #1e3a8a;">🌊 Drop Your Email Here</h3>
        </div>
        """, unsafe_allow_html=True)
        
        email_content = st.text_area(
            "Paste your email content:",
            height=300,
            placeholder="Drop your suspicious email here and let our lifeguards check it out! 🏖️"
        )
        
        # Sample emails for testing
        st.markdown("""
        <div class="beach-card">
            <h3 style="color: #1e3a8a;">🧪 Test Waters</h3>
            <p style="color: #374151;">Try these sample emails to test our security net:</p>
        </div>
        """, unsafe_allow_html=True)
        
        sample_option = st.selectbox(
            "Choose a test email:",
            ["None", "🐠 Safe Email", "🦈 Suspicious Email", "🦑 Phishing Email", "🐙 Spam Email"]
        )
        
        sample_emails = {
            "🐠 Safe Email": """Hi John,

I hope this email finds you well. I wanted to follow up on our meeting from last week regarding the project timeline.

The team has made good progress and we're on track to meet our deadline. Could you please review the attached documents and let me know if you have any questions?

Best regards,
Sarah""",
            
            "🦈 Suspicious Email": """Dear Customer,

Your account has been temporarily suspended due to suspicious activity. Please verify your identity immediately by clicking the link below.

Click here to verify: http://secure-bank-verify.com/login

This is urgent and requires immediate attention.

Best regards,
Security Team""",
            
            "🦑 Phishing Email": """URGENT: Your account has been COMPROMISED!

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
            
            "🐙 Spam Email": """🔥🔥🔥 LIMITED TIME OFFER! 🔥🔥🔥

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
        st.markdown("""
        <div class="beach-card">
            <h3 style="color: #1e3a8a;">📁 Drop Your File</h3>
            <p style="color: #374151;">Upload an email file and let our security net catch any threats!</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose an email file:",
            type=['txt', 'eml']
        )
        
        if uploaded_file is not None:
            email_content = uploaded_file.getvalue().decode("utf-8")
            st.text_area("File content:", email_content, height=200, disabled=True)
    
    # Scan button
    if st.button("🎣 Cast Security Net", type="primary", disabled=not email_content.strip()):
        if email_content.strip():
            with st.spinner("🌊 Our lifeguards are analyzing your email..."):
                # Call backend API
                result = call_backend_api(
                    "/scan",
                    {"content": email_content, "user_id": "beach_user"},
                    "POST"
                )
                
                if result:
                    st.success("🎉 Analysis complete! Here's what we caught:")
                    display_scan_result(result)
                else:
                    st.error("🌊 Failed to analyze email. Please check your connection to the security net.")

def show_scan_history():
    """Show scan history with beach theme."""
    st.markdown("""
    <div class="beach-card">
        <h2 style="color: #1e3a8a;">📊 Catch Log</h2>
        <p style="color: #374151;">Review your recent catches and security patrol history</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get scan history from backend
    history = call_backend_api("/history?limit=20")
    
    if history and history.get("scans"):
        scans = history["scans"]
        
        # Display summary using native Streamlit metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Catches", history["total_count"])
        with col2:
            st.metric("Recent Catches", len(scans))
        with col3:
            if scans:
                avg_confidence = sum(scan["confidence"] for scan in scans) / len(scans)
                st.metric("Avg Confidence", f"{avg_confidence:.1%}")
        
        # Display scan list
        st.subheader("🎣 Recent Catches")
        for scan in scans:
            with st.expander(f"{scan['classification'].upper()} - {scan['timestamp'][:19]}"):
                display_scan_result(scan)
    else:
        st.info("🌊 No catches in the log yet. Start fishing for some emails!")

def show_statistics():
    """Show statistics with beach theme."""
    st.markdown("""
    <div class="beach-card">
        <h2 style="color: #1e3a8a;">📈 Beach Patrol Stats</h2>
        <p style="color: #374151;">Your security lifeguard statistics and performance metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    stats = call_backend_api("/stats")
    
    if stats:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏖️ Overall Stats")
            st.metric("Total Scans", stats["total_scans"])
            
            if stats["recent_activity"]["last_24_hours"]:
                st.metric("Last 24 Hours", stats["recent_activity"]["last_24_hours"])
                st.metric("Avg Confidence", f"{stats['recent_activity']['average_confidence']:.1%}")
        
        with col2:
            st.subheader("🐟 Catch Types")
            if stats["classifications"]:
                for classification, count in stats["classifications"].items():
                    icon = {"legitimate": "🐠", "suspicious": "🦈", "spam": "🐙", "phishing": "🦑"}.get(classification, "🐟")
                    st.metric(f"{icon} {classification.title()}", count)
            else:
                st.info("🌊 No classification data available yet.")
    else:
        st.error("🌊 Unable to load beach patrol statistics.")

def show_about():
    """Show about page with beach theme."""
    st.markdown("""
    <div class="beach-card">
        <h2 style="color: #1e3a8a;">🏖️ About Catch a Phish!</h2>
        <p style="color: #374151;">Your beach-side email security guard protecting you from the deep web's dangerous waters</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 🌊 What is Catch a Phish!?
    
    Catch a Phish! is your friendly beach-side email security guard that helps detect spam, phishing, and other security threats in email content. Just like a lifeguard watches over swimmers, we watch over your emails!
    
    ### 🎣 Features
    
    - 🐠 **AI-Powered Analysis**: Uses advanced machine learning to analyze email content
    - 🦈 **Multi-Threat Detection**: Identifies spam, phishing, and suspicious emails
    - 📊 **Detailed Reports**: Provides confidence scores and explanations for each catch
    - 🌊 **Beautiful Interface**: Enjoy a relaxing beach theme while staying secure
    - 🎣 **Multiple Input Methods**: Support for manual input and file uploads
    - 📈 **Catch History**: Keep track of all your catches for analysis
    
    ### 🏖️ How it Works
    
    1. **Cast Your Net**: Paste email content or upload a file
    2. **AI Analysis**: Our lifeguards analyze the content using multiple factors
    3. **Catch Report**: Content is classified as safe, suspicious, spam, or phishing
    4. **Results**: Get detailed analysis with confidence scores and explanations
    
    ### 🛠️ Technology Stack
    
    - **Backend**: FastAPI with Python
    - **AI Model**: HuggingFace Transformers (DistilBERT)
    - **Frontend**: Streamlit with beach theme
    - **Authentication**: API Key-based security
    
    ### 🔒 Security
    
    - All API calls require authentication
    - Email content is processed securely
    - No data is stored permanently (in-memory only)
    
    ### 🏄‍♂️ Version
    
    Catch a Phish! v1.0.0 - Beach Edition
    
    ---
    
    **Built with ❤️ for email security and beach vibes! 🏖️🎣**
    """)

if __name__ == "__main__":
    main() 