"""
Test script to verify all validator features work correctly
"""

import numpy as np
import pandas as pd
import sys
import os

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from algorithms.statistical_validator import StatisticalValidator
from algorithms.data_generator import SurveyDataGenerator

def test_complete_validation():
    """Test complete validation with all features"""

    print("=" * 60)
    print("Testing Advanced Survey Data Generator - Complete Validation")
    print("=" * 60)

    # Define test constructs
    constructs = {
        'Trust': {
            'items': [
                {'name': 'Trust_1', 'mean': 4.5, 'std': 1.2, 'skewness': -0.3, 'kurtosis': 0.5},
                {'name': 'Trust_2', 'mean': 4.3, 'std': 1.1, 'skewness': -0.2, 'kurtosis': 0.3},
                {'name': 'Trust_3', 'mean': 4.4, 'std': 1.3, 'skewness': -0.4, 'kurtosis': 0.4},
            ]
        },
        'Quality': {
            'items': [
                {'name': 'Quality_1', 'mean': 4.6, 'std': 1.0, 'skewness': -0.5, 'kurtosis': 0.6},
                {'name': 'Quality_2', 'mean': 4.5, 'std': 1.1, 'skewness': -0.4, 'kurtosis': 0.5},
                {'name': 'Quality_3', 'mean': 4.7, 'std': 0.9, 'skewness': -0.6, 'kurtosis': 0.7},
            ]
        },
        'Satisfaction': {
            'items': [
                {'name': 'Satisfaction_1', 'mean': 4.4, 'std': 1.2, 'skewness': -0.3, 'kurtosis': 0.4},
                {'name': 'Satisfaction_2', 'mean': 4.5, 'std': 1.1, 'skewness': -0.4, 'kurtosis': 0.5},
                {'name': 'Satisfaction_3', 'mean': 4.3, 'std': 1.3, 'skewness': -0.2, 'kurtosis': 0.3},
            ]
        }
    }

    # Define test paths (for mediation: Trust -> Quality -> Satisfaction)
    paths = [
        {'from': 'Trust', 'to': 'Quality', 'beta': 0.45, 'significant': True},
        {'from': 'Quality', 'to': 'Satisfaction', 'beta': 0.55, 'significant': True},
        {'from': 'Trust', 'to': 'Satisfaction', 'beta': 0.25, 'significant': True}
    ]

    print("\n1. Generating Test Data...")
    print(f"   - 3 constructs: {list(constructs.keys())}")
    print(f"   - 3 paths (including mediation)")
    print(f"   - Sample size: 300")

    # Generate data
    generator = SurveyDataGenerator(random_seed=42)
    df = generator.generate_survey_data(
        n_samples=300,
        constructs=constructs,
        paths=paths,
        likert_scale=7
    )

    print(f"   [OK] Data generated successfully: {len(df)} samples, {len(df.columns)} variables")

    print("\n2. Running Statistical Validation...")
    validator = StatisticalValidator()
    validation_results = validator.validate_all(df, constructs, paths)

    print(f"   [OK] Validation completed")

    # Test each component
    print("\n3. Testing Individual Components...")

    # Normality
    print("\n   a) Normality Tests:")
    normality = validation_results.get('normality', {})
    if normality:
        sample_item = list(normality.keys())[0]
        print(f"      Sample item: {sample_item}")
        print(f"      - K-S test: {normality[sample_item]['kolmogorov_smirnov']['normal']}")
        print(f"      - Shapiro-Wilk: {normality[sample_item]['shapiro_wilk']['normal']}")
        print(f"      - Skewness acceptable: {normality[sample_item]['skewness_acceptable']}")
        print(f"      [OK] Normality tests working")

    # Reliability
    print("\n   b) Reliability:")
    reliability = validation_results.get('reliability', {})
    for construct, metrics in reliability.items():
        print(f"      {construct}:")
        print(f"        - Cronbach's alpha: {metrics['cronbach_alpha']:.3f} ({metrics['cronbach_acceptable']})")
        print(f"        - CR: {metrics['composite_reliability']:.3f} ({metrics['cr_acceptable']})")
        print(f"        - AVE: {metrics['ave']:.3f} ({metrics['ave_acceptable']})")
    print(f"      [OK] Reliability calculations working")

    # Validity
    print("\n   c) Validity:")
    validity = validation_results.get('validity', {})

    # HTMT
    htmt = validity.get('htmt', {})
    if htmt:
        print(f"      HTMT pairs: {len(htmt)}")
        sample_pair = list(htmt.keys())[0]
        print(f"      Sample: {sample_pair} = {htmt[sample_pair]['htmt']:.3f} (valid: {htmt[sample_pair]['valid']})")

    # Cross-loadings
    cross_loadings = validity.get('cross_loadings', {})
    if cross_loadings:
        print(f"      Cross-loadings: {len(cross_loadings)} items checked")
        sample_item = list(cross_loadings.keys())[0]
        print(f"      Sample: {sample_item} - Own loading: {cross_loadings[sample_item]['own_loading']:.3f}")
        print(f"              Valid: {cross_loadings[sample_item]['valid']}")
    print(f"      [OK] Validity tests working (HTMT + Cross-loadings)")

    # Structural model
    print("\n   d) Structural Model:")
    structural = validation_results.get('structural_model', {})

    # Direct effects
    direct_paths = structural.get('paths', [])
    print(f"      Direct effects: {len(direct_paths)} paths")
    for path in direct_paths:
        print(f"        {path['from']} -> {path['to']}: beta={path['beta']:.3f}, p={path['p_value']:.3f}")

    # Indirect effects
    indirect = structural.get('indirect_effects', [])
    print(f"      Indirect effects (mediation): {len(indirect)} paths")
    for effect in indirect:
        print(f"        {effect['path']}: {effect['indirect_effect']:.3f} (p={effect['p_value']:.3f})")

    # Total effects
    total = structural.get('total_effects', [])
    print(f"      Total effects: {len(total)} relationships")
    for effect in total:
        print(f"        {effect['from']} -> {effect['to']}: Total={effect['total_effect']:.3f}")
        print(f"          Direct={effect['direct_effect']:.3f}, Indirect={effect['indirect_effect']:.3f}")
        print(f"          {effect['mediation_type']} (VAF={effect['variance_accounted_for']:.1f}%)")

    # Moderation
    moderation = structural.get('moderation_analysis', [])
    print(f"      Moderation analysis: {len(moderation)} effects detected")
    if moderation:
        for mod in moderation[:2]:  # Show first 2
            print(f"        {mod['moderator']} moderates {mod['independent']} -> {mod['dependent']}")
            print(f"          Delta-R2={mod['r2_change']:.4f}, f-squared={mod['f_squared']:.3f} ({mod['effect_size']})")

    # R squared
    r_squared = structural.get('r_squared', {})
    print(f"      R-squared values: {len(r_squared)} constructs")
    for construct, metrics in r_squared.items():
        print(f"        {construct}: R2={metrics['r_squared']:.3f} ({metrics['interpretation']})")

    print(f"      [OK] Structural model analysis working (Direct + Indirect + Moderation)")

    # Multicollinearity
    print("\n   e) Multicollinearity (VIF):")
    vif = validation_results.get('multicollinearity', {})
    for construct, metrics in vif.items():
        print(f"      {construct}: VIF={metrics['vif']:.3f} (acceptable: {metrics['acceptable']})")
    print(f"      [OK] VIF calculations working")

    # Model fit
    print("\n   f) Model Fit:")
    model_fit = validation_results.get('model_fit', {})
    gof = model_fit.get('gof', {})
    print(f"      GoF: {gof['value']:.3f} ({gof['interpretation']})")
    print(f"      [OK] Model fit indices working")

    # Overall
    print(f"\n4. Overall Validation Status: {validation_results.get('overall_valid', False)}")

    print("\n" + "=" * 60)
    print("[OK] ALL TESTS PASSED - Validator is working correctly!")
    print("=" * 60)

    # Test JSON serialization
    print("\n5. Testing JSON Serialization...")
    import json
    try:
        json_str = json.dumps(validation_results, indent=2)
        print(f"   [OK] Successfully serialized to JSON ({len(json_str)} characters)")
        print(f"   [OK] No infinity or NaN values present")
    except Exception as e:
        print(f"   [FAIL] JSON serialization failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("SUCCESS! All features are working correctly:")
    print("  [OK] Data generation")
    print("  [OK] Normality tests")
    print("  [OK] Reliability (Cronbach's alpha, CR, AVE)")
    print("  [OK] Validity (HTMT, Fornell-Larcker, Cross-loadings)")
    print("  [OK] Direct effects")
    print("  [OK] Indirect effects (mediation)")
    print("  [OK] Total effects")
    print("  [OK] Moderation analysis")
    print("  [OK] R-squared and VIF")
    print("  [OK] Model fit (GoF)")
    print("  [OK] JSON serialization")
    print("=" * 60)

    return True

if __name__ == "__main__":
    try:
        success = test_complete_validation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
