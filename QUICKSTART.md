# Quick Start Guide

Get the AI Voice Detector API running in 5 minutes.

## Prerequisites

- Python 3.9 or higher
- pip
- Audio file (WAV or MP3) for testing

## Steps

### 1. Setup (2 minutes)

```bash
# Navigate to project directory
cd ai-voice-detector

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Server (30 seconds)

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
🎙️  AI Voice Detector API starting up...
Rate limiting: 30 requests per 60 seconds
```

### 3. Test API (1 minute)

**In a new terminal:**

**Option A: Health Check**
```bash
curl http://localhost:8000/health
```

**Option B: With Your Audio File**
```bash
curl -X POST http://localhost:8000/detect-voice \
  -H "X-API-Key: your-default-api-key-change-in-production" \
  -F "file=@your_audio.wav"
```

**Option C: Python Test**
```bash
python test_api.py
```

### 4. View Documentation (Optional)

Open in browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example Response

```json
{
  "classification": "human",
  "confidence": 0.87,
  "explanation": "Audio exhibits characteristics consistent with natural human speech...",
  "timestamp": "2026-02-03T10:30:45.123456",
  "processing_time_ms": 234.56
}
```

## Troubleshooting

### Issue: "Module not found: librosa"
```bash
pip install librosa
```

### Issue: "Port 8000 already in use"
```bash
# Use different port
python -m uvicorn main:app --port 8001
```

### Issue: "Audio file not recognized"
- Ensure file is WAV or MP3
- Check file is not corrupted
- Try with a smaller file

## Next Steps

- 📖 Read [README.md](README.md) for full documentation
- 🚀 Check [DEPLOYMENT.md](DEPLOYMENT.md) to deploy online
- 📋 See [API_SPECIFICATION.md](API_SPECIFICATION.md) for detailed API docs

---

**Done! Your API is ready.** 🎉
