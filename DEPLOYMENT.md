# Deployment Guide: AI Voice Detector API

This guide covers deploying the AI Voice Detector API to various cloud platforms.

## Quick Start (Local Development)

```bash
# 1. Navigate to project
cd ai-voice-detector

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set API key
export API_KEY=your-api-key  # Windows: set API_KEY=your-api-key

# 5. Run server
python main.py

# Server runs on http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## Deploy on Render (Recommended for Free Tier)

**Render** offers a free tier that's perfect for hackathon projects.

### Steps

1. **Create account** at https://render.com
2. **Go to Dashboard** → New → Web Service
3. **Connect GitHub**
   - If using GitHub, authorize Render
   - Select the repository with this project
   - If using git deploy, use `git push render main`

4. **Configure Web Service**
   ```
   Name: ai-voice-detector
   Environment: Python 3
   Region: Choose closest to you
   Branch: main
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

5. **Set Environment Variables**
   - Go to Environment
   - Add new variables:
     ```
     API_KEY=your-production-api-key
     ```

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Get your public URL (e.g., `https://ai-voice-detector.onrender.com`)

### Testing on Render

```bash
curl -X POST https://ai-voice-detector.onrender.com/detect-voice \
  -H "X-API-Key: your-production-api-key" \
  -F "file=@sample.wav"
```

---

## Deploy on Heroku (Older Free Tier Ended)

If using an existing Heroku account:

### Steps

1. **Install Heroku CLI** from https://devcenter.heroku.com/articles/heroku-cli

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

4. **Set config variables**
   ```bash
   heroku config:set API_KEY=your-production-api-key
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **View logs**
   ```bash
   heroku logs --tail
   ```

7. **Get public URL**
   ```bash
   heroku apps:info
   # App will be at https://your-app-name.herokuapp.com
   ```

---

## Deploy on DigitalOcean App Platform

### Steps

1. **Create DigitalOcean account** at https://www.digitalocean.com/

2. **Go to App Platform** → Create App

3. **Connect GitHub**
   - Select repository
   - Choose branch: main

4. **Configure App**
   - **Resource Type**: Web Service
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **HTTP Port**: 8000

5. **Set Environment Variables**
   - `API_KEY=your-production-api-key`

6. **Choose Plan** (Basic plan recommended for hackathon)

7. **Deploy**

8. **Access your app** at the provided URL

---

## Deploy on Google Cloud Run

### Steps

1. **Install Google Cloud SDK**: https://cloud.google.com/sdk/docs/install

2. **Login**
   ```bash
   gcloud auth login
   gcloud config set project your-project-id
   ```

3. **Create Dockerfile** (if not using buildpacks)
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

4. **Deploy**
   ```bash
   gcloud run deploy ai-voice-detector \
     --source . \
     --platform managed \
     --region us-central1 \
     --set-env-vars API_KEY=your-production-api-key \
     --allow-unauthenticated
   ```

---

## Deploy on Railway

### Steps

1. **Create account** at https://railway.app

2. **Connect GitHub** or upload project

3. **Railway auto-detects Python**

4. **Add environment variables**
   - Go to Variables
   - Add `API_KEY=your-production-api-key`

5. **Deploy** automatically triggers on push

6. **Get public URL** from Railway dashboard

---

## Deploy on Replit (Fastest for Testing)

### Steps

1. **Go to** https://replit.com

2. **Create new Repl**
   - Template: Python
   - Upload or paste your code

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set secrets**
   - Click "Secrets" (lock icon)
   - Add `API_KEY=your-production-api-key`

5. **Run**
   - Click "Run" button
   - Share via Replit's public link

---

## Performance Optimization Tips

### For Render/DigitalOcean

- **Use Standard tier** for better CPU (free tier may timeout on large files)
- **Increase timeout** for audio processing if needed
- **Monitor logs** for errors and bottlenecks

### For Production

1. **Add GPU support** if processing large files
2. **Use Redis** for caching model weights
3. **Implement request queue** for spike handling
4. **Add CDN** for audio delivery
5. **Monitor metrics** with Sentry or DataDog

---

## Troubleshooting Deployment

### Issue: "librosa installation fails"
**Solution**: May need build tools. Add to buildpacks:
```
heroku buildpacks:add heroku/apt  # Heroku
# For Render: Add --build-arg in Dockerfile
```

### Issue: "Timeout on large files"
**Solution**: 
- Increase timeout in deployment config
- Reduce max file size in `main.py`
- Add chunked processing

### Issue: "Out of memory"
**Solution**:
- Upgrade to larger instance
- Process audio in chunks
- Stream responses instead of loading full file

### Issue: "Rate limit errors in testing"
**Solution**:
- Use different API keys for parallel testing
- Wait between requests
- Reset rate limiter if needed (requires restart)

---

## Security Checklist for Production

- ✅ Change `API_KEY` to strong random string
- ✅ Enable HTTPS (all platforms do this by default)
- ✅ Set `PORT` environment variable properly
- ✅ Monitor API logs for suspicious activity
- ✅ Implement WAF (Web Application Firewall) if available
- ✅ Set up alerts for errors and rate limit spikes
- ✅ Keep dependencies updated

---

## Monitoring & Logging

### View Logs

**Render**:
```
Dashboard → Service → Logs
```

**Heroku**:
```bash
heroku logs --tail
```

**DigitalOcean**:
```
App Platform → Logs tab
```

### Key Metrics to Monitor

- Request latency (should be <500ms for small files)
- Error rate (should be <1%)
- API key usage patterns
- Rate limit violations
- Memory/CPU usage

---

## Cost Estimation

| Platform | Free Tier | Limitation | Cost Upgrade |
|----------|-----------|-----------|-----------|
| Render | Yes | Spins down after 15min inactivity | $7/month (Standard) |
| Heroku | No | Previously $7/month (now paid plans only) | $7/month+ |
| DigitalOcean | $5/month credit | 1 container, 512MB RAM | $5/month+ |
| Google Cloud Run | Yes | 2M requests/month | Pay per use |
| Railway | $5/month credit | Generous free tier | Pay per use |
| Replit | Yes | No external API access | Upgrade needed |

**Recommendation for Hackathon**: Use **Render** (free tier) or **Google Cloud Run** (free tier with 2M requests/month)

---

## Final Checklist

Before submitting for evaluation:

- [ ] API deployed and publicly accessible
- [ ] Health endpoint returns 200 OK
- [ ] Detection endpoint works with test audio
- [ ] API key authentication working
- [ ] Rate limiting operational
- [ ] Error handling returns proper JSON
- [ ] README with API specs included
- [ ] requirements.txt includes all dependencies
- [ ] Environment variables documented
- [ ] Example curl commands work

---

**Good luck with your hackathon submission! 🚀**
