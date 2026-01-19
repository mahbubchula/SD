# Setup Guide - Advanced Survey Data Generator

Complete installation and setup instructions for the Advanced Survey Data Generator.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software (100% FREE)

#### Option 1: Docker (Recommended - Easiest)
- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
  - Download: https://www.docker.com/products/docker-desktop
  - Includes Docker Compose

#### Option 2: Manual Installation
- **Python 3.10+**
  - Download: https://www.python.org/downloads/
- **Node.js 18+**
  - Download: https://nodejs.org/
- **PostgreSQL 14+**
  - Download: https://www.postgresql.org/download/

## Installation Methods

### Method 1: Docker (Recommended)

**Easiest and fastest method - everything is automated!**

#### Step 1: Install Docker
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Install and start Docker Desktop
3. Verify installation:
```bash
docker --version
docker-compose --version
```

#### Step 2: Clone/Navigate to Project
```bash
cd "E:\06_GitHub_Repo\01_Active_Projects\advanced-survey-data-generator"
```

#### Step 3: Start All Services
```bash
docker-compose up -d
```

This single command will:
- Start PostgreSQL database
- Start Backend API (FastAPI)
- Start Frontend (React)
- Configure all networking

#### Step 4: Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

#### Step 5: Stop Services
```bash
docker-compose down
```

---

### Method 2: Manual Installation

**For development or if you prefer manual setup**

#### Step 1: Install Prerequisites
1. Install Python 3.10+
2. Install Node.js 18+
3. Install PostgreSQL 14+

#### Step 2: Setup Database
```bash
# Start PostgreSQL service
# Windows: Start via Services
# Linux/Mac: sudo systemctl start postgresql

# Create database
createdb survey_data_generator

# Or using psql:
psql -U postgres
CREATE DATABASE survey_data_generator;
\q
```

#### Step 3: Setup Backend
```bash
# Navigate to project
cd "E:\06_GitHub_Repo\01_Active_Projects\advanced-survey-data-generator"

# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
copy .env.example .env

# Edit .env file with your database credentials
# DATABASE_URL=postgresql://postgres:password@localhost:5432/survey_data_generator
# SECRET_KEY=your-secret-key-change-this
```

#### Step 4: Setup Frontend
```bash
# Open new terminal
cd "E:\06_GitHub_Repo\01_Active_Projects\advanced-survey-data-generator"

# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

#### Step 5: Run Backend
```bash
# In backend directory with activated venv
cd backend
python app/main.py

# Backend will run on http://localhost:8000
```

#### Step 6: Run Frontend
```bash
# In frontend directory (new terminal)
cd frontend
npm run dev

# Frontend will run on http://localhost:3000
```

---

## Configuration

### Backend Configuration (.env)

Create `backend/.env` file:

```env
# Database
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/survey_data_generator

# JWT Secret (CHANGE THIS!)
SECRET_KEY=your-super-secret-key-at-least-32-characters-long

# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
```

**IMPORTANT**: Change `SECRET_KEY` in production!

### Frontend Configuration

Frontend automatically proxies API requests to `http://localhost:8000` (configured in `vite.config.js`)

---

## Running the Application

### Development Mode

#### Using Docker:
```bash
docker-compose up
```

#### Manual:
```bash
# Terminal 1 - Backend
cd backend
python app/main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Production Mode

#### Build Frontend:
```bash
cd frontend
npm run build
```

#### Serve with Production Server:
```bash
# Backend (with production settings)
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend (serve build folder with nginx or similar)
```

---

## Accessing the Application

1. **Open Browser**: http://localhost:3000
2. **Register**: Create new account
3. **Login**: Use your credentials
4. **Start Generating**: Create your first survey dataset

---

## Default URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | React web interface |
| Backend API | http://localhost:8000 | FastAPI backend |
| API Documentation | http://localhost:8000/api/docs | Interactive API docs |
| ReDoc | http://localhost:8000/api/redoc | Alternative API docs |
| Database | localhost:5432 | PostgreSQL |

---

## Troubleshooting

### Docker Issues

**Problem**: Docker containers won't start
```bash
# Check Docker is running
docker ps

# Check logs
docker-compose logs

# Restart containers
docker-compose restart

# Clean rebuild
docker-compose down
docker-compose up --build
```

**Problem**: Port already in use
```bash
# Check what's using port 3000 or 8000
# Windows:
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Kill process or change port in docker-compose.yml
```

### Backend Issues

**Problem**: Module not found
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**Problem**: Database connection error
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Test connection: `psql -U postgres -d survey_data_generator`

**Problem**: Import errors
```bash
# Ensure you're in the correct directory
cd backend/app
python main.py
```

### Frontend Issues

**Problem**: npm install fails
```bash
# Clear cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

**Problem**: API calls fail
- Check backend is running on port 8000
- Verify CORS settings in backend
- Check browser console for errors

### Database Issues

**Problem**: Cannot connect to database
```bash
# Windows - Start PostgreSQL service
services.msc
# Find "PostgreSQL" and start

# Linux/Mac
sudo systemctl start postgresql

# Verify it's running
psql -U postgres -c "SELECT version();"
```

**Problem**: Database doesn't exist
```bash
# Create it
createdb survey_data_generator

# Or via psql
psql -U postgres
CREATE DATABASE survey_data_generator;
\q
```

---

## Verification Checklist

After installation, verify everything works:

- [ ] Docker containers running (if using Docker)
- [ ] Backend API accessible at http://localhost:8000
- [ ] API docs accessible at http://localhost:8000/api/docs
- [ ] Frontend accessible at http://localhost:3000
- [ ] Can register new user
- [ ] Can login successfully
- [ ] Can access dashboard
- [ ] Database connection working

---

## Next Steps

Once setup is complete:

1. Read the [User Manual](USER_MANUAL.md)
2. Explore the Dashboard
3. Generate your first dataset
4. Export data in different formats

---

## Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Review error messages in:
   - Browser console (F12)
   - Backend logs
   - Docker logs
3. Ensure all prerequisites are installed
4. Try Docker method if manual installation fails

---

## Free Deployment Options

### Frontend
- **Vercel**: https://vercel.com (FREE)
- **Netlify**: https://netlify.com (FREE)
- **GitHub Pages**: https://pages.github.com (FREE)

### Backend
- **Railway**: https://railway.app (FREE tier)
- **Render**: https://render.com (FREE tier)
- **PythonAnywhere**: https://www.pythonanywhere.com (FREE tier)

### Database
- **Supabase**: https://supabase.com (FREE tier)
- **ElephantSQL**: https://www.elephantsql.com (FREE tier)
- **Neon**: https://neon.tech (FREE tier)

---

**Project is 100% FREE and Open Source!**
