"""
Validation Routes
Endpoints for pre-validation and statistical checks
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Dict, Any
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.algorithms.statistical_validator import StatisticalValidator
from app.routes.auth import verify_token

router = APIRouter()


class ValidationRequest(BaseModel):
    data: List[Dict[str, Any]]
    constructs: Dict[str, Any]
    paths: List[Dict[str, Any]]


@router.post("/validate-data")
async def validate_data(
    request: ValidationRequest,
    payload: dict = Depends(verify_token)
):
    """
    Validate existing data against all statistical criteria
    """
    try:
        # Convert to DataFrame
        df = pd.DataFrame(request.data)

        # Validate
        validator = StatisticalValidator()
        results = validator.validate_all(df, request.constructs, request.paths)

        return {
            'success': True,
            'validation_results': results
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error validating data: {str(e)}"
        )


@router.get("/criteria")
async def get_validation_criteria(payload: dict = Depends(verify_token)):
    """
    Get all validation criteria and thresholds
    """
    criteria = {
        'normality': {
            'tests': ['Kolmogorov-Smirnov', 'Shapiro-Wilk'],
            'thresholds': {
                'p_value': 0.05,
                'skewness': [-2, 2],
                'kurtosis': [-7, 7]
            }
        },
        'reliability': {
            'cronbach_alpha': {
                'threshold': 0.7,
                'excellent': 0.9,
                'good': 0.8,
                'acceptable': 0.7
            },
            'composite_reliability': {
                'threshold': 0.7,
                'excellent': 0.9
            },
            'ave': {
                'threshold': 0.5,
                'good': 0.7
            }
        },
        'validity': {
            'fornell_larcker': {
                'description': 'Squared correlation < AVE',
                'threshold': 'AVE of construct'
            },
            'htmt': {
                'threshold': 0.85,
                'conservative': 0.85,
                'liberal': 0.90
            }
        },
        'structural_model': {
            'r_squared': {
                'substantial': 0.75,
                'moderate': 0.50,
                'weak': 0.25
            },
            'f_squared': {
                'large': 0.35,
                'medium': 0.15,
                'small': 0.02
            },
            'vif': {
                'threshold': 5,
                'ideal': 3
            }
        },
        'model_fit': {
            'gof': {
                'large': 0.36,
                'medium': 0.25,
                'small': 0.10
            },
            'srmr': {
                'threshold': 0.08
            },
            'nfi': {
                'threshold': 0.90
            }
        }
    }

    return {
        'criteria': criteria,
        'references': [
            'Hair et al. (2019) - PLS-SEM guidelines',
            'Henseler et al. (2015) - HTMT',
            'Fornell & Larcker (1981) - Discriminant validity'
        ]
    }
