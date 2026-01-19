# 🚀 START HERE - Quick Setup Guide

## ✅ Installation Status

**Frontend**: ✅ **INSTALLED**
**Backend**: ⏳ **INSTALLING** (will finish in a few minutes)

---

## 📋 How to Run the Application

### Option 1: Using Batch Files (Easiest!)

**Step 1: Start Backend**
1. Double-click `start-backend.bat`
2. Wait for "Uvicorn running on http://0.0.0.0:8000"
3. Keep this window open

**Step 2: Start Frontend (New Window)**
1. Double-click `start-frontend.bat`
2. Wait for "Local: http://localhost:3000"
3. Keep this window open

**Step 3: Open Browser**
- Go to: **http://localhost:3000**
- Create an account
- Start generating data!

---

### Option 2: Using PowerShell/Terminal

**Terminal 1 - Backend:**
```powershell
cd "E:\06_GitHub_Repo\01_Active_Projects\advanced-survey-data-generator"
cd backend
.\venv\Scripts\activate
cd app
python main.py
```

**Terminal 2 - Frontend:**
```powershell
cd "E:\06_GitHub_Repo\01_Active_Projects\advanced-survey-data-generator"
cd frontend
npm run dev
```

---

## 🌐 Access URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application |
| **Backend API** | http://localhost:8000 | API server |
| **API Docs** | http://localhost:8000/api/docs | Interactive API documentation |

---

## ✨ First Steps

1. **Register**: Create a new account
2. **Login**: Sign in with your credentials
3. **Explore Dashboard**: See features and quick start guide
4. **Generate Data**:
   - Define constructs (e.g., "Customer Satisfaction")
   - Add items to each construct (e.g., "CS1", "CS2", "CS3")
   - Set parameters (mean, SD, skewness, kurtosis)
   - Define paths between constructs
   - Generate dataset
5. **Export**: Download in your preferred format

---

## 🎨 Features

- ✅ **Orange & White Theme** - Professional and energetic design
- ✅ **Statistical Validation** - All SmartPLS criteria
- ✅ **Multiple Export Formats** - SPSS, Excel, CSV, SmartPLS, JSON
- ✅ **Full Control** - Customize every parameter
- ✅ **Pre-Validation** - Check before generating

---

## 🆘 Troubleshooting

### Backend won't start
**Error**: "Module not found"
**Solution**: Wait for installation to complete (check if packages are still installing)

**Error**: "Port 8000 already in use"
**Solution**:
```powershell
# Find what's using port 8000
netstat -ano | findstr :8000
# Kill the process or change port in main.py
```

### Frontend won't start
**Error**: "Port 3000 already in use"
**Solution**: Stop other apps using port 3000 or change port in vite.config.js

### Can't access in browser
**Solution**:
- Make sure both backend AND frontend are running
- Check http://localhost:3000 (not http://127.0.0.1:3000)
- Clear browser cache

---

## 📚 Documentation

- **Quick Start**: QUICKSTART.md
- **Full Setup Guide**: docs/SETUP_GUIDE.md
- **User Manual**: docs/USER_MANUAL.md
- **Project README**: README.md

---

## 🎯 Example Workflow

1. **Create Constructs**:
   - Perceived Usefulness (PU) - 4 items
   - Perceived Ease of Use (PEOU) - 4 items
   - Intention to Use (ITU) - 3 items

2. **Set Item Parameters**:
   - Mean: 5.0-5.5 (positive responses)
   - SD: 1.0-1.2 (typical variation)
   - Skewness: -0.3 to -0.5 (slight negative)
   - Kurtosis: 0.0 (normal)

3. **Define Paths**:
   - PEOU → PU: β=0.45
   - PU → ITU: β=0.60
   - PEOU → ITU: β=0.25

4. **Generate**:
   - Sample Size: 300
   - Likert Scale: 7-point
   - Validate and generate

5. **Export**:
   - Choose SmartPLS format
   - Import into SmartPLS 4.0
   - Run analysis

---

## 🆓 100% Free

All technologies used are completely free:
- Python, FastAPI
- React, Vite, Tailwind CSS
- NumPy, SciPy, pandas
- No subscriptions, no costs!

---

## ⚠️ Educational Purpose Only

This tool generates synthetic data for:
- ✅ Teaching statistical methods
- ✅ Learning PLS-SEM/fsQCA
- ✅ Practicing analysis software

NOT for:
- ❌ Actual research publication
- ❌ Fabricating data
- ❌ Academic dishonesty

---

## 💡 Pro Tips

1. Start with 2-3 constructs for first try
2. Use 4 items per construct (standard)
3. Set realistic parameters (mean 4-6, SD 1-1.5)
4. Always pre-validate before generating
5. Export to multiple formats to test

---

## 🔧 Technical Stack

**Backend:**
- Python 3.14
- FastAPI (API framework)
- NumPy, SciPy (statistical computations)
- pandas (data manipulation)

**Frontend:**
- React 18
- Vite (build tool)
- Tailwind CSS (styling with orange theme)

---

## 📞 Need Help?

- Check troubleshooting section above
- Read the full documentation
- Review error messages carefully
- API documentation: http://localhost:8000/api/docs

---

**Ready to start?**

1. Wait for backend installation to complete
2. Run `start-backend.bat`
3. Run `start-frontend.bat`
4. Open http://localhost:3000
5. Create account and start generating data!

🧡 **Enjoy your Advanced Survey Data Generator!**
