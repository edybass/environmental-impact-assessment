# 🚀 Deployment Guide - EIA Pro Platform

## GitHub Deployment Strategy

### Frontend (GitHub Pages)
The frontend will be deployed to GitHub Pages for easy access and testing.

### Backend Options
1. **Vercel** - Easy Python deployment
2. **Render** - Free tier available
3. **Railway** - Simple deployment
4. **Heroku** - Professional option

## Step 1: Push to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "feat: Professional EIA Platform with PDF generation"

# Add your GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/environmental-impact-assessment.git

# Push to main branch
git push -u origin main
```

## Step 2: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on **Settings**
3. Scroll down to **Pages**
4. Under **Source**, select **Deploy from a branch**
5. Choose **main** branch
6. Select **/docs** folder
7. Click **Save**

Your frontend will be available at:
```
https://YOUR_USERNAME.github.io/environmental-impact-assessment/
```

## Step 3: Deploy Backend

### Option A: Deploy to Vercel (Recommended)

1. Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "backend_comprehensive.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "backend_comprehensive.py"
    }
  ]
}
```

2. Install Vercel CLI:
```bash
npm i -g vercel
```

3. Deploy:
```bash
vercel --prod
```

### Option B: Deploy to Render

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: eia-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python backend_comprehensive.py"
    envVars:
      - key: PORT
        value: 10000
```

2. Connect GitHub repo to Render
3. Deploy automatically

### Option C: Deploy to Railway

1. Install Railway CLI:
```bash
npm i -g @railway/cli
```

2. Deploy:
```bash
railway login
railway init
railway up
```

## Step 4: Update Frontend API Endpoint

Once backend is deployed, update the API URL in `docs/index.html`:

```javascript
// Change from:
const API_URL = 'http://localhost:5000/api';

// To your deployed backend:
const API_URL = 'https://your-backend-url.vercel.app/api';
```

## Step 5: Test Deployment

1. Visit your GitHub Pages URL
2. Fill out the assessment form
3. Click "Run Comprehensive Assessment"
4. Verify results appear
5. Test PDF generation

## Environment Variables

Create `.env` file for sensitive data (don't commit):
```
SECRET_KEY=your-secret-key
API_KEY=your-api-key
```

## CORS Configuration

The backend is already configured to accept requests from any origin:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

For production, update to specific domain:
```python
CORS(app, resources={r"/api/*": {"origins": "https://YOUR_USERNAME.github.io"}})
```

## Quick Deploy Script

Create `deploy.sh`:
```bash
#!/bin/bash
# Deploy script

echo "📦 Deploying EIA Platform..."

# Frontend
git add .
git commit -m "Update: $1"
git push origin main

echo "✅ Frontend deployed to GitHub Pages"

# Backend (if using Vercel)
vercel --prod

echo "🚀 Deployment complete!"
```

Usage:
```bash
./deploy.sh "Added new feature"
```

## Troubleshooting

### Frontend not loading?
- Check GitHub Pages is enabled
- Wait 5-10 minutes for initial deployment
- Check browser console for errors

### API calls failing?
- Verify backend is deployed and running
- Check API_URL is updated in index.html
- Test backend directly: `https://your-backend-url/health`

### PDF generation issues?
- Ensure ReportLab is in requirements.txt
- Check backend logs for errors
- Try HTML format as fallback

## Success Checklist

✅ Code pushed to GitHub
✅ GitHub Pages enabled
✅ Frontend accessible via GitHub Pages URL
✅ Backend deployed to cloud platform
✅ API endpoint updated in frontend
✅ Assessment runs successfully
✅ PDF generation works

---

Once deployed, share your GitHub Pages URL for easy testing without any local setup issues!