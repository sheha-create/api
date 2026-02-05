# AI Voice Detector API

A production-ready REST API for detecting AI-generated vs human voice in audio files. Supports Tamil, English, Hindi, Malayalam, and Telugu languages.

---

## 🎯 Features

- **Single REST Endpoint**: `/detect-voice` for voice classification
- **Multiple Audio Formats**: WAV and MP3 support
- **Language Agnostic**: Works with any language via signal processing
- **ML-Based Detection**: Uses spectral analysis and artifact detection (no hardcoded rules)
- **API Key Authentication**: Secure via `X-API-Key` header
- **Rate Limiting**: Built-in protection against abuse
- **Async Support**: High-performance async request handling
- **Production Ready**: Deployable on Render, Heroku, or any Python-capable cloud service

---

## 📋 API Specification

### Endpoint: POST `/detect-voice`

Classify an audio file as AI-generated or human.

#### Request

**Headers:**
```
X-API-Key: your-api-key
Content-Type: multipart/form-data
```

**Body (form-data):**
- `file`: Audio file (WAV or MP3), max 25MB

**Example using cURL:**
```bash
curl -X POST http://localhost:8000/detect-voice \
  -H "X-API-Key: your-api-key" \
  -F "file=@sample.wav"
```

**Example using Python:**
```python
import requests

with open('sample.wav', 'rb') as f:
    files = {'file': f}
    headers = {'X-API-Key': 'your-api-key'}
    response = requests.post(
        'http://localhost:8000/detect-voice',
        headers=headers,
        files=files
    )
    print(response.json())
```

#### Response (Success - 200 OK)

```json
{
  "classification": "AI-generated",
  "confidence": 0.82,
  "explanation": "Audio exhibits characteristics consistent with AI generation. Key indicator: spectral artifacts (confidence: 82%). Analysis based on spectral features, temporal patterns, and digital artifact detection.",
  "timestamp": "2026-02-03T10:30:45.123456",
  "processing_time_ms": 245.67
}
```

**Fields:**
- `classification`: `"AI-generated"` or `"human"`
- `confidence`: Decimal 0.0-1.0 (higher = more confident in classification)
- `explanation`: Technical reasoning for the classification
- `timestamp`: ISO 8601 timestamp of request
- `processing_time_ms`: Processing duration in milliseconds

#### Response (Error - 400/401/429/500)

```json
{
  "error": "Invalid audio format. Allowed: wav, mp3",
  "timestamp": "2026-02-03T10:30:45.123456"
}
```

**Common Status Codes:**
- `200`: Success
- `400`: Invalid file format or empty file
- `401`: Missing API key
- `403`: Invalid API key
- `413`: File too large (>25MB)
- `429`: Rate limit exceeded (30 requests/60 seconds per API key)
- `500`: Processing error

---

## 🏥 Health Check

### Endpoint: GET `/health`

Check API status.

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-03T10:30:45.123456",
  "version": "1.0.0"
}
```

---

## 🛠️ Local Development

### Prerequisites

- Python 3.9+
- pip

### Setup

1. **Clone/Navigate to project:**
```bash
cd ai-voice-detector
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set API key (optional, defaults to provided key):**
```bash
export API_KEY=your-secure-api-key
# On Windows: set API_KEY=your-secure-api-key
```

5. **Run server:**
```bash
python main.py
```

Server starts on `http://localhost:8000`

### Testing

**Test health endpoint:**
```bash
curl http://localhost:8000/health
```

**Test detection:**
```bash
curl -X POST http://localhost:8000/detect-voice \
  -H "X-API-Key: your-default-api-key-change-in-production" \
  -F "file=@test_audio.wav"
```

**Interactive API Docs:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🚀 Deployment

### Deploy on Render

1. **Create Render account** at https://render.com

2. **Connect GitHub repository** (or use git deploy)

3. **Create New Web Service:**
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Set environment variables in Render dashboard:**
   ```
   API_KEY=your-production-api-key
   ```

5. **Deploy** and get public URL

### Deploy on Heroku

1. **Install Heroku CLI**

2. **Create app:**
```bash
heroku create your-app-name
```

3. **Deploy:**
```bash
git push heroku main
```

4. **Set config:**
```bash
heroku config:set API_KEY=your-production-api-key
```

### Deploy on DigitalOcean App Platform

1. Connect GitHub repo to DigitalOcean
2. Set buildpack to Python
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables

---

## 🔐 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_KEY` | `your-default-api-key-change-in-production` | API authentication key |
| `PORT` | `8000` | Server port |

---

## 📊 Detection Algorithm

The API uses ML-based voice detection combining:

1. **Spectral Feature Extraction**
   - MFCCs (Mel-Frequency Cepstral Coefficients)
   - Spectral centroid and rolloff
   - Zero crossing rate
   - Chroma features

2. **Digital Artifact Detection**
   - Harmonic structure analysis
   - Compression artifact identification
   - Noise floor characteristics
   - Periodicity patterns

3. **Temporal Consistency Analysis**
   - Energy variation patterns
   - Onset interval consistency
   - Speech rhythm detection

4. **Spectral Characteristics Analysis**
   - Spectral flatness (Wiener entropy)
   - Harmonic-to-total ratio
   - Centroid variance

The algorithm is **language-agnostic** and works with any spoken language (Tamil, English, Hindi, Malayalam, Telugu, etc.)

---

## 📁 Project Structure

```
ai-voice-detector/
├── main.py                 # FastAPI application with endpoints
├── audio_processing.py     # ML-based audio detection logic
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── Procfile               # Heroku deployment config
├── runtime.txt            # Python version specification
└── README.md              # This file
```

---

## ⚙️ Configuration Details

### Rate Limiting
- **Limit**: 30 requests per 60 seconds per API key
- **Sliding window**: Old requests expire after 60 seconds
- **Error**: Returns 429 Too Many Requests when exceeded

### File Constraints
- **Max size**: 25 MB
- **Formats**: WAV, MP3
- **Min duration**: 1 second
- **Processing**: Audio is mono-downsampled to 16 kHz

### API Key
- **Header**: `X-API-Key`
- **Required**: Yes
- **Default**: `your-default-api-key-change-in-production` (change in production!)

---

## 🐛 Troubleshooting

**ImportError: librosa**
```bash
pip install librosa
```

**ImportError: scikit-learn**
```bash
pip install scikit-learn
```

**Connection refused on localhost:8000**
- Ensure server is running: `python main.py`
- Check port isn't in use: `lsof -i :8000` (macOS/Linux)

**Audio file not loading**
- Ensure file format is WAV or MP3
- Check file is not corrupted
- Verify file size < 25MB

**Rate limit errors**
- Wait 60 seconds or use different API key
- Check X-API-Key header is correct

---

## 📝 API Examples

### Python Client Example

```python
import requests
import json

API_KEY = "your-api-key"
API_URL = "http://localhost:8000"

def detect_voice(audio_path):
    """Detect AI-generated vs human voice."""
    with open(audio_path, 'rb') as f:
        files = {'file': f}
        headers = {'X-API-Key': API_KEY}
        
        response = requests.post(
            f'{API_URL}/detect-voice',
            headers=headers,
            files=files,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Classification: {result['classification']}")
            print(f"Confidence: {result['confidence']:.1%}")
            print(f"Explanation: {result['explanation']}")
            print(f"Processing time: {result['processing_time_ms']:.2f}ms")
        else:
            print(f"Error: {response.status_code}")
            print(response.json())

# Test
detect_voice('sample.wav')
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');

const API_KEY = 'your-api-key';
const API_URL = 'http://localhost:8000';

async function detectVoice(audioPath) {
    const form = new FormData();
    form.append('file', fs.createReadStream(audioPath));
    
    try {
        const response = await axios.post(
            `${API_URL}/detect-voice`,
            form,
            {
                headers: {
                    ...form.getHeaders(),
                    'X-API-Key': API_KEY
                },
                timeout: 60000
            }
        );
        
        const result = response.data;
        console.log(`Classification: ${result.classification}`);
        console.log(`Confidence: ${(result.confidence * 100).toFixed(1)}%`);
        console.log(`Explanation: ${result.explanation}`);
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
    }
}

// Test
detectVoice('sample.wav');
```

---

## 📜 License

This project is provided as-is for hackathon evaluation and educational purposes.

---

## 🤝 Support

For issues or questions, refer to the project documentation or API docs at `/docs`.

---

**Version**: 1.0.0  
**Last Updated**: February 2026
