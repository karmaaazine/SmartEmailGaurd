# 🛡️ Smart Email Guardian

**AI-Powered Spam & Phishing Detection Toolkit**

Smart Email Guardian is a comprehensive email security solution that uses advanced AI to detect spam, phishing, and other security threats in email content. Built with Python, FastAPI, and Streamlit, it provides both CLI and web interfaces for easy email analysis.

## 🚀 Features

- **🤖 AI-Powered Analysis**: Uses HuggingFace Transformers (DistilBERT) for intelligent email classification
- **🛡️ Multi-Threat Detection**: Identifies spam, phishing, suspicious, and legitimate emails
- **📊 Detailed Reports**: Provides confidence scores, explanations, and feature analysis
- **🌐 Web Interface**: Modern React frontend for easy email analysis
- **🔧 CLI Tool**: Command-line interface for batch processing and automation
- **📧 Gmail Integration**: Direct integration with Gmail API for inbox scanning
- **📈 History Tracking**: Maintains scan history and provides statistics
- **🔐 Secure API**: Token-based authentication for backend API

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Gmail Inbox   │───▶│ gmail_reader.py │───▶│   FastAPI       │
└─────────────────┘    └─────────────────┘    │   Backend       │
                                              └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐           │
│   React         │◀───│   AI Module     │◀──────────┘
│   Frontend      │    │ email_guard.py  │
└─────────────────┘    └─────────────────┘
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Google Cloud Console account (for Gmail integration)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd email_spam_detection_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "EMAIL_GUARD_API_KEY=your-secret-api-key-here" > .env
   ```

4. **Download AI model** (first run will download automatically)
   ```bash
   python -c "from ai.email_guard import analyze_email; analyze_email('test')"
   ```

## 🚀 Usage

### 1. CLI Tool

**Basic usage:**
```bash
# Analyze email from stdin
echo "Your email content here" | python email_guard.py

# Analyze email from file
python email_guard.py -f suspicious_email.txt

# Output in different formats
python email_guard.py -f email.txt -o text
python email_guard.py -f email.txt -o table
```

**Exit codes:**
- `0`: Legitimate email
- `1`: Invalid input
- `2`: Suspicious content (spam/phishing)

### 2. Web Interface

**Start the full-stack app with Docker:**
```bash
docker build -t email-guardian .
docker run -p 8000:8000 email-guardian
```

**Start the backend separately:**
```bash
cd backend
python app.py
```

**Start the frontend separately:**
```bash
cd frontend
npm install
npm start
```

**Access the web interface:**
- App: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 3. Gmail Integration

**Set up Gmail API:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API
4. Create OAuth2 credentials
5. Download `credentials.json` to the `gmail_integration/` directory

**Run Gmail scanner:**
```bash
cd gmail_integration
python gmail_reader.py
```

### 4. API Usage

**Scan an email:**
```bash
curl -X POST "http://localhost:8000/scan" \
  -H "x-api-key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{"content": "Your email content here"}'
```

**Get scan history:**
```bash
curl -X GET "http://localhost:8000/history?limit=10" \
  -H "x-api-key: your-secret-api-key-here"
```

## 🧪 Testing

**Run unit tests:**
```bash
pytest tests/
```

**Run specific test:**
```bash
pytest tests/test_email_guard.py::TestEmailGuardAI::test_analyze_email_legitimate
```

## 📁 Project Structure

```
email_spam_detection_app/
├── ai/
│   └── email_guard.py          # AI analysis module
├── backend/
│   └── app.py                  # FastAPI backend
├── frontend/
│   ├── src/                    # React source code
│   └── ...                     # React frontend files
├── gmail_integration/
│   └── gmail_reader.py         # Gmail API integration
├── tests/
│   └── test_email_guard.py     # Unit tests
├── docs/
│   ├── README.md               # This file
│   ├── security_notes.md       # Security considerations
│   └── architecture.png        # Architecture diagram
├── email_guard.py              # CLI tool
├── requirements.txt            # Python dependencies
└── .env                        # Environment variables
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EMAIL_GUARD_API_KEY` | API key for backend authentication | `your-secret-api-key-here` |
| `GMAIL_CREDENTIALS_FILE` | Path to Gmail OAuth2 credentials | `credentials.json` |

### API Configuration

The backend API supports the following endpoints:

- `POST /scan` - Analyze email content
- `GET /history` - Get scan history
- `GET /stats` - Get statistics
- `GET /health` - Health check

All endpoints require the `x-api-key` header for authentication.

## 🚀 Deployment

### Local Development

1. **Backend:**
   ```bash
   cd backend
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend (React):**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Full-stack (Docker):**
   ```bash
   docker build -t email-guardian .
   docker run -p 8000:8000 email-guardian
   ```

### Production Deployment

**Using Docker (Full Stack):**
```bash
# Build image (from project root)
docker build -t email-guardian .

# Run container
docker run -p 8000:8000 email-guardian
```

**Using Render.com:**
1. Connect your repository to Render
2. Set environment variables
3. Deploy as a web service

## 🔒 Security Considerations

- **API Key Protection**: Use strong, unique API keys
- **HTTPS**: Always use HTTPS in production
- **Input Validation**: All inputs are validated and sanitized
- **Rate Limiting**: Consider implementing rate limiting for production
- **Data Privacy**: Email content is processed in memory only

See `docs/security_notes.md` for detailed security information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check the `docs/` directory
- **API Docs**: Available at `http://localhost:8000/docs` when backend is running

## 🔄 Version History

- **v1.0.0**: Initial release with basic functionality
  - AI-powered email analysis
  - CLI and web interfaces
  - Gmail integration
  - Basic security features

## 🎯 Roadmap

- [ ] Advanced threat detection models
- [ ] Real-time email monitoring
- [ ] Email labeling and filtering
- [ ] Integration with email clients
- [ ] Machine learning model training
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Mobile app

---

**Built with ❤️ for email security** 
