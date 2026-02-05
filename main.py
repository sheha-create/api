"""
AI-Generated Voice Detection API
Main FastAPI application with authentication, rate limiting, and voice detection endpoint.
"""

import os
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Dict, Optional
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Header, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from collections import defaultdict
import time

from audio_processing import AudioProcessor

# ============================================================================
# Models
# ============================================================================
class VoiceDetectionResponse(BaseModel):
    """Response model for voice detection endpoint."""
    classification: str  # "AI-generated" or "human"
    confidence: float    # 0.0 to 1.0
    explanation: str
    timestamp: str
    processing_time_ms: float


# ============================================================================
# Configuration
# ============================================================================
# Load environment variables from .env (if present)
load_dotenv()

API_KEY = os.getenv("API_KEY", "your-default-api-key-change-in-production")
MAX_FILE_SIZE_MB = 25
ALLOWED_AUDIO_FORMATS = {"wav", "mp3"}
RATE_LIMIT_REQUESTS = 30
RATE_LIMIT_WINDOW_SECONDS = 60

# ============================================================================
# Rate Limiting
# ============================================================================
class RateLimiter:
    """Simple in-memory rate limiter using sliding window."""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if client is within rate limit."""
        now = time.time()
        cutoff = now - self.window_seconds
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > cutoff
        ]
        
        # Check if limit exceeded
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True


rate_limiter = RateLimiter(
    max_requests=RATE_LIMIT_REQUESTS,
    window_seconds=RATE_LIMIT_WINDOW_SECONDS
)

# ============================================================================
# FastAPI Application
# ============================================================================
app = FastAPI(
    title="AI Voice Detector API",
    description="Detects AI-generated vs human voices in audio files",
    version="1.0.0"
)

audio_processor = AudioProcessor()


# ============================================================================
# Middleware & Dependencies
# ============================================================================
async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """Verify API key from request header."""
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    return x_api_key


async def check_rate_limit(x_api_key: str = Header(None)) -> None:
    """Check if client is within rate limits."""
    client_id = x_api_key or "anonymous"
    
    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Max {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW_SECONDS} seconds"
        )


# ============================================================================
# Health Check Endpoint
# ============================================================================
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


# ============================================================================
# Main Detection Endpoint
# ============================================================================
@app.post("/detect-voice", tags=["detection"], response_model=VoiceDetectionResponse)
async def detect_voice(
    file: UploadFile = File(...),
    x_api_key: str = Header(None)
):
    """
    Detect if uploaded audio is AI-generated or human.
    
    Parameters:
    - file: Audio file (WAV or MP3) via multipart form data
    - X-API-Key: API key in request header
    
    Returns:
    - classification: "AI-generated" or "human"
    - confidence: 0.0 to 1.0
    - explanation: Brief technical reason
    - timestamp: Request timestamp
    - processing_time_ms: Processing duration
    
    Languages supported: Tamil, English, Hindi, Malayalam, Telugu
    
    Example:
        curl -X POST http://localhost:8000/detect-voice \\
          -H "X-API-Key: your-api-key" \\
          -F "file=@sample.wav"
    """
    
    # Verify authentication
    await verify_api_key(x_api_key)
    
    # Check rate limit
    await check_rate_limit(x_api_key)
    
    start_time = time.time()
    
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File name is required"
            )
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lower().lstrip('.')
        if file_ext not in ALLOWED_AUDIO_FORMATS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid audio format. Allowed: {', '.join(ALLOWED_AUDIO_FORMATS)}"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Check file size
        file_size_mb = len(file_content) / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Max size: {MAX_FILE_SIZE_MB}MB"
            )
        
        if len(file_content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is empty"
            )
        
        # Process audio and detect
        classification, confidence, explanation = await asyncio.to_thread(
            audio_processor.detect_voice,
            file_content,
            file_ext
        )
        
        processing_time = (time.time() - start_time) * 1000
        
        return VoiceDetectionResponse(
            classification=classification,
            confidence=round(confidence, 2),
            explanation=explanation,
            timestamp=datetime.utcnow().isoformat(),
            processing_time_ms=round(processing_time, 2)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Processing error: {str(e)}"
        )


# ============================================================================
# Error Handlers
# ============================================================================
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Catch-all exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ============================================================================
# Startup/Shutdown Events
# ============================================================================
@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    print("🎙️  AI Voice Detector API starting up...")
    print(f"Rate limiting: {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW_SECONDS} seconds")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    print("🛑 AI Voice Detector API shutting down...")


# ============================================================================
# Entry Point
# ============================================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
