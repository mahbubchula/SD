"""
Complete System Test - Verify All Features
Tests backend functionality including indirect effects, total effects, and moderation
"""

import sys
import os
import io

# Set UTF-8 encoding for console output (Windows compatibility)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.algorithms.data_generator import SurveyDataGenerator
from app.algorithms.statistical_validator import StatisticalValidator
import json

def test_complete_system():
    """Test complete system with mediation model"""

    print("\n" + "="*60)
    print("COMPLETE SYSTEM TEST - MEDIATION MODEL")
    print("="*60 + "\n")

    # Define constructs with mediation chain
    constructs = {
        'Trust': {
            'items': [
                {'name': 'Trust_1', 'mean': 5.0, 'std': 1.2, 'skewness': 0.0, 'kurtosis': 0.0},
                {'name': 'Trust_2', 'mean': 5.0, 'std': 1.2, 'skewness': 0.0, 'kurtosis': 0.0},
                {'name': 'Trust_3', 'mean': 5.0, 'std': 1.2, 'skewness': 0.0, 'kurtosis': 0.0}
            ]
        },
        'Quality': {
            'items': [
                {'name': 'Quality_1', 'mean': 5.0, 'std': 1.2, 'skewness': 0.0, 'kurtosis': 0.0},
                {'name': 'Quality_2', 'mean': 5.0, 'std': 1.2, 'skewness': 0.0, 'kurtosis': 0.0},
                {'name': 'Quality_3', 'mean': 5.0, 'std': 1.2, 'skewness': 0.0, 'kurtosis': 0.0}
            ]
        },
        'Satisfaction': {
            'items': [
                {'name': 'Sat_1', 'mean': 5.0, 'std': 1.2, 'skewness': 0.0, 'kurtosis': 0.0},
                {'name': 'Sat_2', 'mean': 5.0, 'std': 1.2, 'skewness': 0.0, 'kurtosis': 0.0},
                {'name': 'Sat_3', 'mean': 5.0, 'std': 1.2, 'skewness': 0.0, 'kurtosis': 0.0}
            ]
        }
    }

    # Define mediation paths: Trust -> Quality -> Satisfaction
    paths = [
        {'from': 'Trust', 'to': 'Quality', 'beta': 0.5, 'significant': True},
        {'from': 'Quality', 'to': 'Satisfaction', 'beta': 0.6, 'significant': True},
        {'from': 'Trust', 'to': 'Satisfaction', 'beta': 0.2, 'significant': True}
    ]

    print("Model Configuration:")
    print(f"  Constructs: {list(constructs.keys())}")
    print(f"  Paths: {len(paths)}")
    print("  Mediation chain: Trust -> Quality -> Satisfaction\n")

    # Generate data
    print("Step 1: Generating data...")
    generator = SurveyDataGenerator(random_seed=42)

    try:
        df = generator.generate_survey_data(
            n_samples=300,
            constructs=constructs,
            paths=paths,
            likert_scale=7
        )
        print(f"[OK] Generated {len(df)} samples with {len(df.columns)} variables\n")
    except Exception as e:
        print(f"[FAIL] FAILED to generate data: {e}\n")
        return False

    # Validate data
    print("Step 2: Running complete validation...")
    validator = StatisticalValidator()

    try:
        results = validator.validate_all(df, constructs, paths)
        print("[OK] Validation completed\n")
    except Exception as e:
        print(f"[FAIL] FAILED validation: {e}\n")
        return False

    # Check critical features
    print("="*60)
    print("FEATURE VERIFICATION")
    print("="*60 + "\n")

    success = True

    # 1. Check Normality
    print("1. Normality Tests:")
    if 'normality' in results and len(results['normality']) > 0:
        print(f"   [OK] Tested {len(results['normality'])} items")
        # Show sample
        first_item = list(results['normality'].keys())[0]
        print(f"   Sample ({first_item}):")
        print(f"     - K-S p-value: {results['normality'][first_item]['kolmogorov_smirnov']['p_value']:.3f}")
        print(f"     - Skewness: {results['normality'][first_item]['skewness']:.3f}")
    else:
        print("   [FAIL] Normality tests missing")
        success = False
    print()

    # 2. Check Reliability
    print("2. Reliability Assessment:")
    if 'reliability' in results and len(results['reliability']) == 3:
        print(f"   [OK] Tested {len(results['reliability'])} constructs")
        for construct, metrics in results['reliability'].items():
            alpha = metrics.get('cronbach_alpha', 0)
            cr = metrics.get('composite_reliability', 0)
            ave = metrics.get('ave', 0)
            status = "+" if alpha >= 0.7 and cr >= 0.7 and ave >= 0.5 else "-"
            print(f"   {status} {construct}: alpha={alpha:.3f}, CR={cr:.3f}, AVE={ave:.3f}")
    else:
        print("   [FAIL] Reliability assessment missing or incomplete")
        success = False
    print()

    # 3. Check Validity
    print("3. Discriminant Validity:")
    if 'validity' in results:
        htmt = results['validity'].get('htmt', {})
        cross_loadings = results['validity'].get('cross_loadings', {})

        if htmt:
            print(f"   [OK] HTMT calculated for {len(htmt)} construct pairs")
            valid_count = sum(1 for v in htmt.values() if v.get('valid', False))
            print(f"     - {valid_count}/{len(htmt)} pairs passed (HTMT < 0.85)")
        else:
            print("   [FAIL] HTMT missing")
            success = False

        if cross_loadings:
            print(f"   [OK] Cross-loadings calculated for {len(cross_loadings)} items")
            valid_count = sum(1 for v in cross_loadings.values() if v.get('valid', False))
            print(f"     - {valid_count}/{len(cross_loadings)} items load highest on own construct")
        else:
            print("   [FAIL] Cross-loadings missing")
            success = False
    else:
        print("   [FAIL] Validity tests missing")
        success = False
    print()

    # 4. Check Direct Effects
    print("4. Direct Effects (Path Coefficients):")
    if 'structural_model' in results and 'paths' in results['structural_model']:
        paths_results = results['structural_model']['paths']
        print(f"   [OK] Calculated {len(paths_results)} path coefficients")
        for path in paths_results:
            beta = path.get('beta', 0)
            t_stat = path.get('t_statistic', 0)
            sig = "+" if path.get('significant', False) else "-"
            print(f"   {sig} {path['from']} -> {path['to']}: beta={beta:.3f}, t={t_stat:.2f}")
    else:
        print("   [FAIL] Direct effects missing")
        success = False
    print()

    # 5. Check Indirect Effects (CRITICAL)
    print("5. Indirect Effects (Mediation) - ** NEW FEATURE:")
    if 'structural_model' in results and 'indirect_effects' in results['structural_model']:
        indirect_effects = results['structural_model']['indirect_effects']

        if len(indirect_effects) > 0:
            print(f"   [OK] Found {len(indirect_effects)} mediation path(s)")
            for effect in indirect_effects:
                path_str = effect.get('path', '')
                indirect_value = effect.get('indirect_effect', 0)
                z_score = effect.get('z_score', 0)
                sig = "+" if effect.get('significant', False) else "-"
                print(f"   {sig} {path_str}")
                print(f"      Indirect Effect: {indirect_value:.3f}, z={z_score:.2f}")

            # Verify expected mediation
            expected_path = "Trust -> Quality -> Satisfaction"
            found_expected = any(expected_path in e.get('path', '') for e in indirect_effects)
            if found_expected:
                print(f"\n   [OK] VERIFIED: Expected mediation path '{expected_path}' found!")
            else:
                print(f"\n   [WARN]  WARNING: Expected mediation path '{expected_path}' not found")
                print(f"      Found paths: {[e.get('path') for e in indirect_effects]}")
        else:
            print("   [FAIL] CRITICAL: No indirect effects found!")
            print("      This is the main issue - mediation analysis not working")
            success = False
    else:
        print("   [FAIL] CRITICAL: Indirect effects section missing entirely!")
        success = False
    print()

    # 6. Check Total Effects (CRITICAL)
    print("6. Total Effects (Direct + Indirect) - ** NEW FEATURE:")
    if 'structural_model' in results and 'total_effects' in results['structural_model']:
        total_effects = results['structural_model']['total_effects']

        if len(total_effects) > 0:
            print(f"   [OK] Calculated {len(total_effects)} total effect(s)")
            for effect in total_effects:
                from_var = effect.get('from', '')
                to_var = effect.get('to', '')
                direct = effect.get('direct_effect', 0)
                indirect = effect.get('indirect_effect', 0)
                total = effect.get('total_effect', 0)
                vaf = effect.get('variance_accounted_for', 0)
                med_type = effect.get('mediation_type', '')

                print(f"   {from_var} -> {to_var} (via {effect.get('mediator', '')})")
                print(f"     Direct:   {direct:.3f}")
                print(f"     Indirect: {indirect:.3f}")
                print(f"     Total:    {total:.3f}")
                print(f"     VAF:      {vaf:.1f}%")
                print(f"     Type:     {med_type}")
        else:
            print("   [FAIL] CRITICAL: No total effects found!")
            success = False
    else:
        print("   [FAIL] CRITICAL: Total effects section missing!")
        success = False
    print()

    # 7. Check Moderation
    print("7. Moderation Analysis - ** NEW FEATURE:")
    if 'structural_model' in results and 'moderation_analysis' in results['structural_model']:
        moderation = results['structural_model']['moderation_analysis']

        if len(moderation) > 0:
            print(f"   [OK] Found {len(moderation)} potential moderation effect(s)")
            for mod in moderation[:3]:  # Show top 3
                print(f"   {mod['independent']} x {mod['moderator']} -> {mod['dependent']}")
                print(f"     ΔR²: {mod['r2_change']:.4f}, f²: {mod['f_squared']:.3f} ({mod['effect_size']})")
        else:
            print("   [INFO]  No significant moderation effects detected (this is OK)")
    else:
        print("   [FAIL] Moderation analysis section missing")
        success = False
    print()

    # 8. Check R-squared
    print("8. Model Fit:")
    if 'structural_model' in results and 'r_squared' in results['structural_model']:
        r_squared = results['structural_model']['r_squared']
        print(f"   [OK] R² calculated for {len(r_squared)} endogenous construct(s)")
        for construct, metrics in r_squared.items():
            r2 = metrics.get('r_squared', 0)
            interp = metrics.get('interpretation', '')
            print(f"     {construct}: R²={r2:.3f} ({interp})")
    else:
        print("   [FAIL] R² values missing")
        success = False

    if 'model_fit' in results and 'gof' in results['model_fit']:
        gof = results['model_fit']['gof']
        print(f"   [OK] GoF: {gof['value']:.3f} ({gof['interpretation']})")
    print()

    # 9. Check VIF
    print("9. Multicollinearity (VIF):")
    if 'multicollinearity' in results:
        vif = results['multicollinearity']
        print(f"   [OK] VIF calculated for {len(vif)} construct(s)")
        all_ok = all(v['acceptable'] for v in vif.values())
        status = "+" if all_ok else "[WARN]"
        print(f"   {status} All VIF values < 5: {all_ok}")
    else:
        print("   [FAIL] VIF missing")
        success = False
    print()

    # 10. JSON Serialization
    print("10. JSON Serialization:")
    try:
        json_str = json.dumps(results, indent=2)
        print(f"   [OK] Results can be serialized to JSON ({len(json_str)} chars)")
        # Check for problematic values
        if 'inf' in json_str.lower() or 'nan' in json_str.lower():
            print("   [WARN]  WARNING: Found inf/nan in JSON (should be sanitized)")
            success = False
    except Exception as e:
        print(f"   [FAIL] JSON serialization failed: {e}")
        success = False
    print()

    # Final result
    print("="*60)
    if success:
        print("[OK] ALL TESTS PASSED - SYSTEM IS FULLY FUNCTIONAL!")
        print("\nCritical Features Verified:")
        print("  + Indirect Effects (Mediation) working")
        print("  + Total Effects (Direct + Indirect) working")
        print("  + Moderation Analysis working")
        print("  + Cross-Loadings working")
        print("  + JSON serialization working")
    else:
        print("[FAIL] SOME TESTS FAILED - REVIEW ERRORS ABOVE")
    print("="*60 + "\n")

    return success


if __name__ == "__main__":
    success = test_complete_system()
    sys.exit(0 if success else 1)
