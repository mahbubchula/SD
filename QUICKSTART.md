# Quick Start Guide

Get the Advanced Survey Data Generator running in 5 minutes!

## 🚀 Fastest Method: Docker

### Step 1: Install Docker
- Download: https://www.docker.com/products/docker-desktop
- Install and start Docker Desktop

### Step 2: Start the Application
```bash
cd "E:\06_GitHub_Repo\01_Active_Projects\advanced-survey-data-generator"
docker-compose up -d
```

### Step 3: Access the Application
Open your browser: **http://localhost:3000**

**That's it!** 🎉

---

## 🛠️ Manual Method (Without Docker)

### Prerequisites
Install:
- Python 3.10+ (https://www.python.org/downloads/)
- Node.js 18+ (https://nodejs.org/)
- PostgreSQL 14+ (https://www.postgresql.org/download/)

### Backend Setup
```bash
cd "E:\06_GitHub_Repo\01_Active_Projects\advanced-survey-data-generator\backend"

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env with your database credentials

# Run backend
python app/main.py
```

Backend runs on: **http://localhost:8000**

### Frontend Setup (New Terminal)
```bash
cd "E:\06_GitHub_Repo\01_Active_Projects\advanced-survey-data-generator\frontend"

# Install dependencies
npm install

# Run frontend
npm run dev
```

Frontend runs on: **http://localhost:3000**

---

## 📋 First Steps

1. **Open** http://localhost:3000
2. **Register** a new account
3. **Login** with your credentials
4. **Explore** the Dashboard
5. **Generate** your first dataset

---

## 🎨 Features Overview

### Orange & White Theme
Professional, energetic, and educational design

### Key Features
- ✅ Generate synthetic survey data
- ✅ Full statistical validation
- ✅ Export to SPSS, Excel, CSV, SmartPLS, JSON
- ✅ Pre-validation before generation
- ✅ Control all parameters

---

## 📚 Documentation

**Full Guides:**
- [Setup Guide](docs/SETUP_GUIDE.md) - Complete installation instructions
- [User Manual](docs/USER_MANUAL.md) - How to use the tool
- [README](README.md) - Project overview

**API Documentation:**
- http://localhost:8000/api/docs - Interactive API docs

---

## 🆘 Troubleshooting

### Docker Issues
```bash
# Check Docker is running
docker ps

# View logs
docker-compose logs

# Restart
docker-compose restart
```

### Cannot Access Frontend
- Check http://localhost:3000
- Ensure frontend container/process is running
- Check for port conflicts

### Cannot Access Backend
- Check http://localhost:8000
- Ensure backend container/process is running
- Verify database connection

### Port Already in Use
```bash
# Windows - Find what's using port
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Change ports in docker-compose.yml or config files
```

---

## ✅ Verification

After starting, verify:
- [ ] Frontend loads at http://localhost:3000
- [ ] Can create account
- [ ] Can login
- [ ] Dashboard displays
- [ ] Backend API at http://localhost:8000/api/docs

---

## 🎯 Next Steps

1. **Generate Data**
   - Define constructs and items
   - Set parameters (mean, SD, skewness, kurtosis)
   - Add paths between constructs
   - Generate dataset

2. **Validate**
   - Pre-check validation criteria
   - Review reliability and validity
   - Adjust parameters if needed

3. **Export**
   - Choose format (SPSS, Excel, CSV, SmartPLS)
   - Download data
   - Import into analysis software

4. **Analyze**
   - Use SmartPLS 4.0, SPSS, or R
   - Run PLS-SEM analysis
   - Practice statistical methods

---

## 🌟 Example Use Case

**Scenario**: Teaching PLS-SEM to students

**Steps**:
1. Generate data for Technology Acceptance Model (TAM)
2. Export as SmartPLS format
3. Import into SmartPLS 4.0
4. Demonstrate measurement model assessment
5. Show structural model evaluation
6. Practice interpretation

**Benefits**:
- Students get realistic data
- No need for actual surveys
- Control all parameters
- Perfect for learning

---

## 📊 Supported Analyses

- **PLS-SEM** (SmartPLS 4.0)
- **CB-SEM** (AMOS)
- **fsQCA**
- **Regression** (SPSS, R)
- **Multi-Group Analysis**
- **Mediation & Moderation**

---

## 🎓 Educational Purpose

**This tool is for teaching and learning only!**

✅ **Use for**:
- Teaching statistical methods
- Learning PLS-SEM
- Practicing analysis software
- Understanding research methodology

❌ **Do NOT use for**:
- Actual research publication
- Fabricating data
- Academic dishonesty

---

## 💡 Pro Tips

1. **Start small**: Begin with 2-3 constructs
2. **Use templates**: Try pre-built models (TAM, UTAUT)
3. **Validate first**: Always pre-check before generating
4. **Export multiple formats**: Try different software
5. **Read the manual**: Full User Manual has detailed guides

---

## 🆓 100% Free

**All technologies used are FREE:**
- Python, FastAPI - FREE
- React, Vite, Tailwind - FREE
- PostgreSQL - FREE
- Docker - FREE
- Node.js - FREE

**No hidden costs, no subscriptions, no limits!**

---

## 🔗 Quick Links

| Resource | URL |
|----------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/api/docs |
| Setup Guide | docs/SETUP_GUIDE.md |
| User Manual | docs/USER_MANUAL.md |

---

**Ready to generate synthetic survey data?**

**Start here**: http://localhost:3000

Enjoy your statistical journey! 🎉
