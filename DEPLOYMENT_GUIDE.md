# 🚀 FREE Deployment Guide - Survey Data Generator

## ✅ Total Cost: $0.00 (Forever FREE)

---

## 📋 Prerequisites

1. **GitHub Account** (free) - https://github.com
2. **Render Account** (free) - https://render.com
3. **Vercel Account** (free) - https://vercel.com

---

## 🎯 STEP 1: Push Code to GitHub

```bash
# Open terminal in your project folder
cd E:\06_GitHub_Repo\01_Active_Projects\advanced-survey-data-generator

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - Survey Data Generator"

# Create a new repository on GitHub.com, then:
git remote add origin https://github.com/YOUR_USERNAME/survey-data-generator.git
git branch -M main
git push -u origin main
```

**Or use GitHub Desktop** (easier):
1. Download GitHub Desktop: https://desktop.github.com
2. File → Add Local Repository → Select your project folder
3. Publish repository

---

## 🔧 STEP 2: Deploy Backend (Render.com - FREE)

### A. Sign Up:
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub

### B. Deploy:
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Settings:
   - **Name:** survey-data-generator-api
   - **Environment:** Python 3
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

4. **Environment Variables** (click "Advanced"):
   - `SECRET_KEY` → Generate random string
   - `ENVIRONMENT` → `production`

5. Click "Create Web Service"

6. **Wait 5-10 minutes** for deployment

7. **Copy your backend URL:** `https://survey-data-generator-api.onrender.com`

### C. Update CORS (Important!):
After deployment, you need to update backend CORS to allow your frontend domain.

---

## 🎨 STEP 3: Deploy Frontend (Vercel.com - FREE)

### A. Update Frontend API URL:

Edit `frontend/.env.production`:
```
VITE_API_URL=https://YOUR-BACKEND-URL.onrender.com
```
(Replace with your actual Render backend URL)

Commit and push:
```bash
git add .
git commit -m "Update API URL for production"
git push
```

### B. Sign Up & Deploy:
1. Go to https://vercel.com
2. Click "Sign Up" → Sign in with GitHub
3. Click "Add New..." → "Project"
4. Import your GitHub repository
5. Settings:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
6. Click "Deploy"

7. **Wait 2-3 minutes**

8. **Your app is live!** `https://your-app.vercel.app`

---

## 🔒 STEP 4: Update Backend CORS

Edit `backend/app/main.py` and add your Vercel URL to allowed origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app.vercel.app"  # Add your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push - Render will auto-redeploy!

---

## ✨ DONE! Your App is Live!

**Backend:** https://your-api.onrender.com
**Frontend:** https://your-app.vercel.app

---

## 📊 Free Tier Limits:

### Render.com (Backend):
- ✅ 750 hours/month (enough for 24/7)
- ✅ Sleeps after 15 min inactivity (wakes up in 30 sec)
- ✅ 512 MB RAM
- ✅ Unlimited users

### Vercel.com (Frontend):
- ✅ Unlimited bandwidth
- ✅ 100 GB/month free
- ✅ Automatic SSL
- ✅ Global CDN

---

## 🎁 BONUS: Custom Domain (Optional - FREE)

### Free Domain Options:
1. **Freenom** - Free .tk, .ml, .ga domains
2. **Use Vercel subdomain** - yourapp.vercel.app (already free)
3. **Use Render subdomain** - yourapp.onrender.com (already free)

---

## 🔄 Auto-Deploy Updates:

Any time you push to GitHub:
- Render auto-deploys backend (3-5 min)
- Vercel auto-deploys frontend (1-2 min)

```bash
git add .
git commit -m "Updated feature"
git push
# Wait for auto-deployment!
```

---

## 🐛 Troubleshooting:

### Backend Won't Start:
1. Check Render logs (Dashboard → Service → Logs)
2. Verify all packages in requirements.txt
3. Check Python version (3.11)

### Frontend Can't Connect:
1. Verify API URL in `.env.production`
2. Check CORS settings in backend
3. Look at browser console for errors

### Database Issues:
- SQLite file persists on Render's disk
- Backup: Download via Render dashboard
- Free tier: Disk clears if inactive 90+ days

---

## 💡 Tips:

1. **Keep Backend Awake:** Use UptimeRobot.com (free) to ping every 5 min
2. **Monitor:** Render dashboard shows logs, usage, errors
3. **Backup Database:** Download `survey_app.db` from Render shell monthly
4. **SSL:** Both Render and Vercel provide free HTTPS automatically

---

## 🎯 Next Steps (Optional):

1. **Add PostgreSQL** (free 256MB on Render) for better database
2. **Add Redis** (free 25MB on Render) for session caching
3. **Custom domain** from Namecheap ($3/year) or use free subdomains

---

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- Community: render.com/community

---

**Your app is now live and accessible from anywhere in the world! 🌍**

Total deployment time: ~15 minutes
Total cost: $0.00 ✨
