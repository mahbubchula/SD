"""
Test to verify item-level data generation
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.algorithms.data_generator import SurveyDataGenerator
import pandas as pd

# Test constructs with multiple items each
constructs = {
    'PerceivedUsefulness': {
        'items': [
            {'name': 'PU1', 'mean': 5.2, 'std': 1.1, 'skewness': -0.3, 'kurtosis': 0.1},
            {'name': 'PU2', 'mean': 5.0, 'std': 1.2, 'skewness': -0.2, 'kurtosis': 0.0},
            {'name': 'PU3', 'mean': 5.1, 'std': 1.0, 'skewness': -0.4, 'kurtosis': 0.2},
            {'name': 'PU4', 'mean': 5.3, 'std': 1.1, 'skewness': -0.3, 'kurtosis': 0.1}
        ],
        'target_cronbach_alpha': 0.85,
        'target_cr': 0.85,
        'target_ave': 0.65
    },
    'PerceivedEaseOfUse': {
        'items': [
            {'name': 'PEOU1', 'mean': 4.8, 'std': 1.3, 'skewness': -0.1, 'kurtosis': 0.0},
            {'name': 'PEOU2', 'mean': 4.9, 'std': 1.2, 'skewness': -0.2, 'kurtosis': 0.1},
            {'name': 'PEOU3', 'mean': 5.0, 'std': 1.1, 'skewness': -0.3, 'kurtosis': 0.2}
        ],
        'target_cronbach_alpha': 0.80,
        'target_cr': 0.80,
        'target_ave': 0.60
    },
    'IntentionToUse': {
        'items': [
            {'name': 'ITU1', 'mean': 4.7, 'std': 1.4, 'skewness': -0.1, 'kurtosis': 0.0},
            {'name': 'ITU2', 'mean': 4.8, 'std': 1.3, 'skewness': -0.2, 'kurtosis': 0.1},
            {'name': 'ITU3', 'mean': 4.9, 'std': 1.2, 'skewness': -0.3, 'kurtosis': 0.2}
        ],
        'target_cronbach_alpha': 0.80,
        'target_cr': 0.80,
        'target_ave': 0.60
    }
}

paths = [
    {'from': 'PerceivedUsefulness', 'to': 'IntentionToUse', 'beta': 0.45, 'significant': True},
    {'from': 'PerceivedUsefulness', 'to': 'PerceivedEaseOfUse', 'beta': 0.38, 'significant': True},
    {'from': 'PerceivedEaseOfUse', 'to': 'IntentionToUse', 'beta': 0.32, 'significant': True}
]

print("=" * 80)
print("TESTING ITEM-LEVEL DATA GENERATION")
print("=" * 80)
print()

# Count expected items
total_items = sum(len(c['items']) for c in constructs.values())
print(f"Expected total items: {total_items}")
print()
print("Expected columns:")
for construct_name, construct_spec in constructs.items():
    item_names = [item['name'] for item in construct_spec['items']]
    print(f"  {construct_name}: {', '.join(item_names)}")
print()

# Generate data
print("Generating data...")
generator = SurveyDataGenerator(random_seed=42)

df = generator.generate_survey_data(
    n_samples=100,
    constructs=constructs,
    paths=paths,
    likert_scale=7,
    add_noise=True,
    noise_level=0.05
)

print()
print("=" * 80)
print("GENERATION RESULTS")
print("=" * 80)
print()
print(f"✓ Generated {len(df)} samples")
print(f"✓ Number of columns: {len(df.columns)}")
print()
print("Columns in generated data:")
for col in df.columns:
    print(f"  - {col}")
print()

# Verify all expected items are present
print("=" * 80)
print("VERIFICATION")
print("=" * 80)
print()

all_expected_items = []
for construct_spec in constructs.values():
    all_expected_items.extend([item['name'] for item in construct_spec['items']])

missing_items = set(all_expected_items) - set(df.columns)
extra_items = set(df.columns) - set(all_expected_items)

if not missing_items and not extra_items:
    print("✓ SUCCESS: All expected items are present!")
    print()
    print(f"Total items: {len(all_expected_items)}")
    print(f"  - PerceivedUsefulness: 4 items (PU1, PU2, PU3, PU4)")
    print(f"  - PerceivedEaseOfUse: 3 items (PEOU1, PEOU2, PEOU3)")
    print(f"  - IntentionToUse: 3 items (ITU1, ITU2, ITU3)")
else:
    if missing_items:
        print(f"✗ Missing items: {missing_items}")
    if extra_items:
        print(f"! Extra items: {extra_items}")

print()
print("Sample data (first 5 rows):")
print(df.head())
print()

# Check data types and ranges
print("Data summary:")
print(df.describe())
print()

print("=" * 80)
print("CONCLUSION")
print("=" * 80)
if not missing_items:
    print("✓ Backend is correctly generating ALL ITEMS for ALL CONSTRUCTS!")
    print("✓ Each construct's items are separate columns")
    print("✓ Data is ready for export")
else:
    print("✗ Issue detected: Some items are missing")

print()
