"""
FastAPI Backend for Smart Email Guardian
Provides REST API endpoints for email analysis and history with HTTPS support.
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
# Remove SSL Configuration and HTTPSRedirectMiddleware
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Add the ai directory to the path
import sys
# sys.path.append(str(Path(__file__).parent.parent / "ai"))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.email_guard import analyze_email

# Configuration
API_KEY = os.getenv("EMAIL_GUARD_API_KEY", "salmas_email_guard")
MAX_EMAIL_LENGTH = 10000  # Maximum email content length

# In-memory storage for scan history (in production, use a database)
scan_history: List[Dict] = []

app = FastAPI(
    title="Smart Email Guardian API",
    description="AI-powered email spam and phishing detection API with HTTPS support",
    version="1.0.0"
)

# Add security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.localhost", "*.127.0.0.1"]
)

# Do not add HTTPS redirect middleware

# Pydantic models
class EmailScanRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=MAX_EMAIL_LENGTH, description="Email content to analyze")
    user_id: Optional[str] = Field(None, description="Optional user identifier")

class EmailScanResponse(BaseModel):
    id: str
    timestamp: str
    classification: str
    confidence: float
    explanation: str
    features: Dict
    indicators: List[str]
    user_id: Optional[str] = None

class ScanHistoryResponse(BaseModel):
    scans: List[EmailScanResponse]
    total_count: int

# Authentication dependency
async def verify_api_key(x_api_key: str = Header(..., alias="x-api-key")):
    """Verify the API key from request header."""
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return x_api_key

# Utility functions
def generate_scan_id() -> str:
    """Generate a unique scan ID."""
    return f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(scan_history)}"

def store_scan_result(scan_data: Dict) -> None:
    """Store scan result in history."""
    scan_history.append(scan_data)
    # Keep only last 100 scans in memory
    if len(scan_history) > 100:
        scan_history.pop(0)

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Smart Email Guardian API",
        "version": "1.0.0",
        "endpoints": {
            "POST /scan": "Analyze email content",
            "GET /history": "Get scan history",
            "GET /health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# Remove /ssl-info endpoint entirely

@app.post("/scan", response_model=EmailScanResponse)
async def scan_email(
    request: EmailScanRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Analyze email content for spam and phishing detection.
    
    Args:
        request: EmailScanRequest containing email content
        api_key: API key for authentication
        
    Returns:
        EmailScanResponse: Analysis results
    """
    try:
        # Analyze email using AI model
        result = analyze_email(request.content)
        
        # Create scan response
        scan_data = {
            "id": generate_scan_id(),
            "timestamp": datetime.now().isoformat(),
            "classification": result["classification"],
            "confidence": result["confidence"],
            "explanation": result["explanation"],
            "features": result.get("features", {}),
            "indicators": result.get("indicators", []),
            "user_id": request.user_id
        }
        
        # Store scan result
        store_scan_result(scan_data)
        
        return EmailScanResponse(**scan_data)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing email: {str(e)}"
        )

@app.get("/history", response_model=ScanHistoryResponse)
async def get_scan_history(
    limit: int = 10,
    user_id: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    """
    Get scan history with optional filtering.
    
    Args:
        limit: Maximum number of scans to return (default: 10)
        user_id: Filter by user ID (optional)
        api_key: API key for authentication
        
    Returns:
        ScanHistoryResponse: List of scan results
    """
    try:
        # Filter scans
        filtered_scans = scan_history
        
        if user_id:
            filtered_scans = [scan for scan in scan_history if scan.get("user_id") == user_id]
        
        # Apply limit
        limited_scans = filtered_scans[-limit:] if limit > 0 else filtered_scans
        
        return ScanHistoryResponse(
            scans=[EmailScanResponse(**scan) for scan in limited_scans],
            total_count=len(filtered_scans)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving scan history: {str(e)}"
        )

@app.get("/stats")
async def get_stats(api_key: str = Depends(verify_api_key)):
    """
    Get statistics about scan history.
    
    Args:
        api_key: API key for authentication
        
    Returns:
        Dict: Statistics about scans
    """
    try:
        if not scan_history:
            return {
                "total_scans": 0,
                "classifications": {},
                "recent_activity": []
            }
        
        # Calculate statistics
        classifications = {}
        for scan in scan_history:
            classification = scan["classification"]
            classifications[classification] = classifications.get(classification, 0) + 1
        
        # Recent activity (last 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        recent_scans = [
            scan for scan in scan_history
            if datetime.fromisoformat(scan["timestamp"]) > cutoff_time
        ]
        
        return {
            "total_scans": len(scan_history),
            "classifications": classifications,
            "recent_activity": {
                "last_24_hours": len(recent_scans),
                "average_confidence": sum(scan["confidence"] for scan in scan_history) / len(scan_history)
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating statistics: {str(e)}"
        )

if __name__ == "__main__":
    # Run the server (HTTP only, no SSL)
    print("🚀 Starting HTTP server on http://localhost:8000")
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 