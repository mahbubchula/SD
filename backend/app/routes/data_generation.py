"""
Data Generation Routes
Main endpoints for generating synthetic survey data
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.algorithms.data_generator import SurveyDataGenerator
from app.algorithms.statistical_validator import StatisticalValidator
from app.routes.auth import verify_token

router = APIRouter()


# Pydantic Models
class Item(BaseModel):
    name: str
    mean: float = Field(default=4.0, ge=1.0, le=7.0)
    std: float = Field(default=1.0, ge=0.1, le=3.0)
    skewness: float = Field(default=0.0, ge=-2.0, le=2.0)
    kurtosis: float = Field(default=0.0, ge=-2.0, le=7.0)


class Construct(BaseModel):
    name: str
    items: List[Item]
    target_cronbach_alpha: Optional[float] = Field(default=0.8, ge=0.7, le=0.95)
    target_cr: Optional[float] = Field(default=0.8, ge=0.7, le=0.95)
    target_ave: Optional[float] = Field(default=0.6, ge=0.5, le=0.9)


class Path(BaseModel):
    from_construct: str = Field(..., alias='from')
    to_construct: str = Field(..., alias='to')
    beta: float = Field(default=0.3, ge=-1.0, le=1.0)
    significant: bool = True
    effect_size: Optional[str] = Field(default="medium")  # small, medium, large


class DemographicVariable(BaseModel):
    name: str
    type: str  # categorical, numerical, ordinal
    categories: Optional[List[str]] = None
    probabilities: Optional[List[float]] = None
    min: Optional[float] = None
    max: Optional[float] = None
    mean: Optional[float] = None
    std: Optional[float] = None
    levels: Optional[List[str]] = None


class DataGenerationRequest(BaseModel):
    sample_size: int = Field(..., ge=100, le=10000)
    constructs: List[Construct]
    paths: List[Path]
    demographic_variables: Optional[List[DemographicVariable]] = []
    likert_scale: int = Field(default=7, ge=3, le=10)
    add_noise: bool = True
    noise_level: float = Field(default=0.05, ge=0.0, le=0.3)
    random_seed: Optional[int] = None
    validate_before_generate: bool = True


class PreValidationRequest(BaseModel):
    """Request to validate parameters before generating data"""
    constructs: List[Construct]
    paths: List[Path]
    sample_size: int = Field(..., ge=100, le=10000)


# Routes
@router.post("/generate")
async def generate_survey_data(
    request: DataGenerationRequest,
    payload: dict = Depends(verify_token)
):
    """
    Generate synthetic survey data with specified parameters
    """
    try:
        # Convert Pydantic models to dictionaries
        constructs_dict = {}
        for construct in request.constructs:
            constructs_dict[construct.name] = {
                'items': [item.dict() for item in construct.items],
                'target_cronbach_alpha': construct.target_cronbach_alpha,
                'target_cr': construct.target_cr,
                'target_ave': construct.target_ave
            }

        paths_list = [
            {
                'from': path.from_construct,
                'to': path.to_construct,
                'beta': path.beta,
                'significant': path.significant
            }
            for path in request.paths
        ]

        demographic_vars = None
        if request.demographic_variables:
            demographic_vars = [var.dict() for var in request.demographic_variables]

        # Generate data
        generator = SurveyDataGenerator(random_seed=request.random_seed)

        df = generator.generate_survey_data(
            n_samples=request.sample_size,
            constructs=constructs_dict,
            paths=paths_list,
            demographic_vars=demographic_vars,
            likert_scale=request.likert_scale,
            add_noise=request.add_noise,
            noise_level=request.noise_level
        )

        # Validate generated data
        validator = StatisticalValidator()
        validation_results = validator.validate_all(df, constructs_dict, paths_list)

        # Convert DataFrame to dictionary
        data_dict = df.to_dict(orient='records')

        # 🔍 DEBUG: Log what we're sending back
        print("=" * 50)
        print("BACKEND: Data Generation Complete")
        print(f"User: {payload.get('sub', 'Unknown')}")
        print(f"Number of samples: {len(df)}")
        print(f"DataFrame columns: {list(df.columns)}")
        print(f"Number of columns: {len(df.columns)}")
        print(f"Constructs: {list(constructs_dict.keys())}")
        print(f"Items in constructs_dict:")
        for c_name, c_spec in constructs_dict.items():
            items = [item['name'] for item in c_spec['items']]
            print(f"  {c_name}: {items}")
        print(f"First row sample: {list(data_dict[0].keys())[:15]}")
        print("=" * 50)

        return {
            'success': True,
            'data': data_dict,
            'validation': validation_results,
            'metadata': {
                'sample_size': len(df),
                'n_constructs': len(constructs_dict),
                'n_items': sum(len(c['items']) for c in constructs_dict.values()),
                'n_paths': len(paths_list),
                'n_demographics': len(demographic_vars) if demographic_vars else 0
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating data: {str(e)}"
        )


@router.post("/preview")
async def preview_generation(
    request: PreValidationRequest,
    payload: dict = Depends(verify_token)
):
    """
    Preview what the generated data will look like (without full generation)
    Shows expected correlations, sample statistics, etc.
    """
    try:
        # Convert to dictionaries
        constructs_dict = {}
        for construct in request.constructs:
            constructs_dict[construct.name] = {
                'items': [item.dict() for item in construct.items]
            }

        paths_list = [
            {
                'from': path.from_construct,
                'to': path.to_construct,
                'beta': path.beta,
                'significant': path.significant
            }
            for path in request.paths
        ]

        # Generate small sample for preview (100 samples)
        generator = SurveyDataGenerator()
        correlation_matrix, construct_order = generator._build_correlation_matrix(
            constructs_dict,
            paths_list
        )

        # Calculate expected statistics
        expected_stats = {}
        for construct_name, construct_spec in constructs_dict.items():
            items_stats = []
            for item in construct_spec['items']:
                items_stats.append({
                    'name': item['name'],
                    'mean': item.get('mean', 4.0),
                    'std': item.get('std', 1.0),
                    'skewness': item.get('skewness', 0.0),
                    'kurtosis': item.get('kurtosis', 0.0)
                })

            expected_stats[construct_name] = items_stats

        return {
            'success': True,
            'expected_correlation_matrix': correlation_matrix.tolist(),
            'construct_order': construct_order,
            'expected_statistics': expected_stats,
            'paths_summary': paths_list
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating preview: {str(e)}"
        )


@router.post("/calculate-sample-size")
async def calculate_sample_size(
    n_constructs: int = Query(..., ge=2, le=20),
    n_items_per_construct: int = Query(..., ge=3, le=10),
    power: float = Query(default=0.8, ge=0.7, le=0.95),
    effect_size: str = Query(default="medium"),
    payload: dict = Depends(verify_token)
):
    """
    Calculate recommended sample size for PLS-SEM
    """
    # Rule of thumb for PLS-SEM: 10 times the maximum number of arrows pointing to a construct
    # or 10 times the number of items in the largest construct

    if effect_size == "small":
        multiplier = 15
    elif effect_size == "medium":
        multiplier = 10
    else:  # large
        multiplier = 7

    # Calculate based on items
    sample_size_items = n_items_per_construct * multiplier

    # Calculate based on power (simplified)
    if effect_size == "small":
        sample_size_power = 300
    elif effect_size == "medium":
        sample_size_power = 150
    else:
        sample_size_power = 100

    recommended_size = max(sample_size_items, sample_size_power)

    return {
        'recommended_sample_size': recommended_size,
        'minimum_sample_size': max(100, n_items_per_construct * 5),
        'optimal_sample_size': recommended_size * 1.5,
        'rationale': f"Based on {n_items_per_construct} items per construct and {effect_size} effect size"
    }


@router.get("/templates")
async def get_model_templates(payload: dict = Depends(verify_token)):
    """
    Get pre-defined research model templates
    """
    templates = {
        'TAM': {
            'name': 'Technology Acceptance Model',
            'constructs': ['Perceived Usefulness', 'Perceived Ease of Use', 'Attitude', 'Behavioral Intention'],
            'description': 'Classic TAM model for technology adoption'
        },
        'UTAUT': {
            'name': 'Unified Theory of Acceptance and Use of Technology',
            'constructs': ['Performance Expectancy', 'Effort Expectancy', 'Social Influence', 'Facilitating Conditions', 'Behavioral Intention'],
            'description': 'Extended model for technology acceptance'
        },
        'TPB': {
            'name': 'Theory of Planned Behavior',
            'constructs': ['Attitude', 'Subjective Norm', 'Perceived Behavioral Control', 'Intention', 'Behavior'],
            'description': 'Theory of planned behavior'
        },
        'CSR_Performance': {
            'name': 'CSR and Performance Model',
            'constructs': ['CSR Activities', 'Corporate Reputation', 'Customer Loyalty', 'Financial Performance'],
            'description': 'Corporate Social Responsibility impact model'
        }
    }

    return {
        'templates': templates
    }
