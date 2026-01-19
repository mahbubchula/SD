"""
Advanced Survey Data Generator - Backend API
Main FastAPI application with authentication and data generation endpoints
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Advanced Survey Data Generator API",
    description="Generate statistically validated synthetic survey data for research and teaching",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Import routes (will be created)
from app.routes import auth, data_generation, validation, export

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(data_generation.router, prefix="/api/generate", tags=["Data Generation"])
app.include_router(validation.router, prefix="/api/validate", tags=["Validation"])
app.include_router(export.router, prefix="/api/export", tags=["Export"])


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Advanced Survey Data Generator API",
        "version": "1.0.0",
        "status": "active",
        "description": "Generate statistically validated synthetic survey data",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Advanced Survey Data Generator"
    }


@app.get("/api/statistics")
async def get_statistics():
    """Get supported statistical tests and validations"""
    return {
        "normality_tests": [
            "Kolmogorov-Smirnov",
            "Shapiro-Wilk",
            "Anderson-Darling",
            "D'Agostino-Pearson"
        ],
        "reliability_tests": [
            "Cronbach's Alpha",
            "Composite Reliability (CR)",
            "Average Variance Extracted (AVE)",
            "Rho_A"
        ],
        "validity_tests": [
            "Fornell-Larcker Criterion",
            "HTMT (Heterotrait-Monotrait Ratio)",
            "Cross Loadings"
        ],
        "model_fit_indices": [
            "R² (R-squared)",
            "Adjusted R²",
            "Q² (Predictive Relevance)",
            "f² (Effect Size)",
            "VIF (Variance Inflation Factor)",
            "GoF (Goodness of Fit)",
            "SRMR",
            "NFI"
        ],
        "path_analysis": [
            "Direct Effects",
            "Indirect Effects",
            "Mediation Analysis",
            "Moderation Analysis",
            "Total Effects"
        ],
        "supported_analyses": [
            "PLS-SEM (SmartPLS 4.0)",
            "CB-SEM",
            "fsQCA",
            "Multi-Group Analysis",
            "IPMA"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
