# Advanced Survey Data Generator

🧡 **Professional Synthetic Survey Data Generation Tool for Academic Research & Teaching**

## 📋 Overview

This tool generates statistically validated synthetic survey data for teaching and research purposes. Perfect for practicing advanced statistical analyses including:

- **SmartPLS 4.0** (PLS-SEM)
- **Structural Equation Modeling (SEM)**
- **fsQCA (Fuzzy-Set Qualitative Comparative Analysis)**
- **Multi-Group Analysis**
- **Mediation & Moderation Analysis**

## ✨ Key Features

### 📊 Data Generation Capabilities
- ✅ **Custom Constructs & Items** - Full flexibility to define research model
- ✅ **Path Modeling** - Direct, indirect, mediation, moderation paths
- ✅ **Statistical Validity** - Passes all SmartPLS validation criteria
- ✅ **Demographic Variables** - Logically generated control variables
- ✅ **Multiple Formats** - Export to SPSS, Excel, CSV, SmartPLS

### 🎯 Statistical Controls
- **Normality Tests** - Kolmogorov-Smirnov, Shapiro-Wilk
- **Distribution Control** - Mean, SD, Skewness, Kurtosis per item
- **Reliability** - Cronbach's Alpha, Composite Reliability, AVE
- **Validity** - Discriminant validity (Fornell-Larcker, HTMT)
- **Model Fit** - R², Q², f², VIF, GoF, SRMR, NFI
- **Effect Sizes** - Control significance levels and effect magnitudes

### 🔧 Advanced Features
- Pre-validation checks before generation
- Common Method Bias control
- Missing data simulation (MCAR, MAR, MNAR)
- Sample size calculator
- Correlation matrix preview
- Full analysis report generation

## 🎨 Design

**Color Theme**: Orange & White - Professional, energetic, and educational
- Primary: #FF6B35 (Vibrant Orange)
- Accents: White & Light Orange
- Clean, modern, academic interface

## 🛠️ Technology Stack (100% FREE!)

### Backend
- **Python 3.10+**
- **FastAPI** - Modern, fast web framework
- **NumPy, SciPy** - Statistical computations
- **pandas** - Data manipulation
- **scikit-learn** - Advanced algorithms
- **PostgreSQL** - Database

### Frontend
- **React 18** - Modern UI library
- **Tailwind CSS** - Styling with orange theme
- **Axios** - API communication
- **Chart.js** - Data visualization

### Authentication
- **JWT** - Secure token-based auth
- **bcrypt** - Password hashing

### Deployment
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Docker (optional)

### Installation

#### 1. Clone Repository
```bash
cd "E:\06_GitHub_Repo\01_Active_Projects"
cd advanced-survey-data-generator
```

#### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Backend runs on: `http://localhost:8000`

#### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```
Frontend runs on: `http://localhost:3000`

#### 4. Database Setup
```bash
# Create PostgreSQL database
createdb survey_data_generator

# Run migrations
cd backend
python -m alembic upgrade head
```

### Docker Deployment (Recommended)
```bash
docker-compose up -d
```

## 📖 Usage Guide

### 1. Sign Up / Login
- Create account with email and password
- Secure JWT authentication

### 2. Create Research Model
- Define constructs (latent variables)
- Add items (observed variables) per construct
- Set relationships (paths) between constructs

### 3. Customize Parameters
- **Item Level**: Mean, SD, Skewness, Kurtosis
- **Construct Level**: Reliability (α, CR, AVE)
- **Path Level**: Significance, Effect size (β)
- **Model Level**: R², Q², GoF

### 4. Add Demographics
- Age, Gender, Education, Income, etc.
- Logically generated with conditional logic

### 5. Pre-Validation
- Check all statistical criteria
- View correlation matrix
- Review expected results

### 6. Generate & Export
- Generate statistically valid dataset
- Export in multiple formats
- Download analysis report

## 📊 Supported Analyses

### Measurement Model Assessment
- ✅ Internal Consistency (Cronbach's α, CR, ρA)
- ✅ Convergent Validity (AVE > 0.5)
- ✅ Discriminant Validity (Fornell-Larcker, HTMT)
- ✅ Indicator Reliability (Loadings > 0.7)

### Structural Model Assessment
- ✅ Collinearity (VIF < 5)
- ✅ Path Coefficients (β, t-values, p-values)
- ✅ R² (Variance Explained)
- ✅ f² Effect Sizes
- ✅ Q² Predictive Relevance
- ✅ RMSE, MAE

### Model Fit
- ✅ Goodness of Fit (GoF)
- ✅ SRMR
- ✅ NFI
- ✅ Chi-square (if applicable)

### Advanced Analyses
- ✅ Mediation Analysis
- ✅ Moderation Analysis
- ✅ Multi-Group Analysis (MGA)
- ✅ IPMA (Importance-Performance Map)
- ✅ fsQCA Compatibility

## 🔒 Security

- Password hashing with bcrypt
- JWT token authentication
- Protected API endpoints
- SQL injection prevention
- XSS protection

## 📁 Project Structure

```
advanced-survey-data-generator/
├── backend/
│   ├── app/
│   │   ├── algorithms/          # Statistical generation algorithms
│   │   ├── models/              # Database models
│   │   ├── routes/              # API endpoints
│   │   ├── utils/               # Utility functions
│   │   ├── validation/          # Statistical validation
│   │   └── main.py             # FastAPI app
│   ├── tests/                   # Unit tests
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API services
│   │   ├── styles/             # CSS/Tailwind
│   │   └── App.js
│   └── package.json            # Node dependencies
├── database/
│   └── schema.sql              # Database schema
├── deployment/
│   ├── docker/
│   │   ├── Dockerfile.backend
│   │   └── Dockerfile.frontend
│   └── docker-compose.yml
└── docs/                       # Documentation

```

## 🎓 Educational Purpose

**IMPORTANT**: This tool is designed SOLELY for:
- ✅ Teaching statistical methods
- ✅ Learning advanced analyses
- ✅ Practice with SmartPLS/SEM/fsQCA
- ✅ Understanding research methodology

**NOT for**:
- ❌ Fabricating real research data
- ❌ Publishing as actual survey results
- ❌ Academic dishonesty

## 📜 License

MIT License - Free for educational use

## 🤝 Contributing

This is an educational tool. Contributions welcome!

## 📧 Support

For issues and questions, please refer to the documentation in `/docs`

---

**Built with ❤️ for Research & Education**

🧡 Orange & White Theme | 100% Free & Open Source
