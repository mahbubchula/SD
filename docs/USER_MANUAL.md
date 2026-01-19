# User Manual - Advanced Survey Data Generator

Complete guide to using the Advanced Survey Data Generator for creating statistically validated synthetic survey data.

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Generating Survey Data](#generating-survey-data)
4. [Statistical Validation](#statistical-validation)
5. [Exporting Data](#exporting-data)
6. [Advanced Features](#advanced-features)
7. [Best Practices](#best-practices)
8. [FAQ](#faq)

---

## Introduction

### What is This Tool?

The Advanced Survey Data Generator creates **synthetic survey data** that is statistically validated for use in:
- Teaching statistical methods
- Learning PLS-SEM, SEM, and fsQCA
- Practicing with SmartPLS 4.0
- Understanding research methodology

### Key Features

- ✅ Generate data with custom constructs and items
- ✅ Control all statistical parameters (mean, SD, skewness, kurtosis)
- ✅ Define paths (direct, indirect, mediation, moderation)
- ✅ Pre-validate before generation
- ✅ Export to multiple formats (SPSS, Excel, CSV, SmartPLS, JSON)
- ✅ Passes all SmartPLS validation criteria

### Important Notice

**Educational Purpose Only**: This tool generates synthetic data for teaching and learning. It is NOT for:
- ❌ Fabricating research data
- ❌ Academic dishonesty
- ❌ Publishing as real survey results

---

## Getting Started

### 1. Registration and Login

#### Register New Account
1. Navigate to http://localhost:3000
2. Click "Create an account"
3. Fill in:
   - Full Name
   - Email Address
   - Password (minimum 8 characters)
4. Click "Create Account"

#### Login
1. Enter your email and password
2. Click "Sign In"
3. You'll be redirected to the Dashboard

### 2. Dashboard Overview

The dashboard shows:
- Quick statistics
- Main features (Generate, Validate, Export)
- Supported statistical tests
- Quick start guide
- Compatible software

---

## Generating Survey Data

### Step 1: Define Your Research Model

#### Create Constructs

A **construct** is a latent variable (e.g., "Customer Satisfaction", "Trust", "Intention to Use")

1. Go to "Generate Data" page
2. Click "Add Construct"
3. Enter construct name
4. Set target reliability:
   - **Cronbach's Alpha**: 0.7 - 0.95 (default: 0.8)
   - **Composite Reliability (CR)**: 0.7 - 0.95 (default: 0.8)
   - **Average Variance Extracted (AVE)**: 0.5 - 0.9 (default: 0.6)

#### Add Items to Constructs

**Items** are observed variables (survey questions)

For each construct:
1. Click "Add Item"
2. Configure parameters:

**Item Name**: e.g., "CS1", "CS2", "CS3"

**Distribution Parameters**:
- **Mean**: Center of distribution (1.0 - 7.0 for 7-point Likert scale)
  - Use 4.0 for neutral
  - Use 5.0-6.0 for positive responses
  - Use 2.0-3.0 for negative responses

- **Standard Deviation**: Spread of data (0.1 - 3.0)
  - 1.0 - typical for Likert scale
  - Lower (0.5-0.8) - more agreement
  - Higher (1.5-2.0) - more disagreement

- **Skewness**: Asymmetry (-2.0 to 2.0)
  - 0.0 = symmetric (normal)
  - Negative = tail on left (most agree)
  - Positive = tail on right (most disagree)

- **Kurtosis**: Peakedness (-2.0 to 7.0)
  - 0.0 = normal distribution
  - Positive = more peaked
  - Negative = more flat

**Example Construct**:
```
Construct: Customer Satisfaction
Items:
  CS1: Mean=5.2, SD=1.1, Skew=-0.3, Kurt=0.0
  CS2: Mean=5.4, SD=1.0, Skew=-0.5, Kurt=0.2
  CS3: Mean=5.0, SD=1.2, Skew=-0.2, Kurt=-0.1
  CS4: Mean=5.3, SD=1.1, Skew=-0.4, Kurt=0.1
```

### Step 2: Define Structural Paths

**Paths** represent relationships between constructs.

#### Types of Paths:

1. **Direct Effect**: A → B
2. **Indirect Effect (Mediation)**: A → B → C
3. **Moderation**: A × M → B

#### Adding Paths:

1. Click "Add Path"
2. Select:
   - **From**: Source construct
   - **To**: Target construct
   - **Beta (β)**: Path coefficient (-1.0 to 1.0)
   - **Significant**: Yes/No
   - **Effect Size**: Small/Medium/Large

**Path Coefficient Guidelines**:
- **Small effect**: β = 0.1 to 0.3
- **Medium effect**: β = 0.3 to 0.5
- **Large effect**: β = 0.5 to 0.7

**Example Model**:
```
Perceived Ease of Use (PEOU) → Perceived Usefulness (PU): β=0.45
Perceived Usefulness (PU) → Intention to Use (ITU): β=0.60
Perceived Ease of Use (PEOU) → Intention to Use (ITU): β=0.25
```

### Step 3: Add Demographic Variables (Optional)

#### Types:

**Categorical** (e.g., Gender)
- Categories: ["Male", "Female", "Other"]
- Probabilities: [0.48, 0.48, 0.04]

**Numerical** (e.g., Age)
- Min: 18
- Max: 65
- Mean: 32
- SD: 10

**Ordinal** (e.g., Education Level)
- Levels: ["High School", "Bachelor", "Master", "PhD"]
- Probabilities: [0.2, 0.5, 0.25, 0.05]

### Step 4: Set Generation Parameters

**Sample Size**: 100 - 10,000
- Minimum: 100 (for basic analysis)
- Recommended: 10 × largest number of paths or items
- Optimal: 200-500 for most analyses

**Likert Scale**: 3 - 10 points
- Most common: 5 or 7 points
- 7-point scale is most popular in research

**Add Noise**: Yes/No
- Adds realistic human response variability
- Noise Level: 0.0 - 0.3 (default: 0.05)

**Random Seed**: (Optional)
- For reproducibility
- Same seed = same data every time

### Step 5: Pre-Validation

Before generating:
1. Click "Preview & Validate"
2. Review:
   - Expected correlation matrix
   - Expected reliability metrics
   - Expected model fit
3. Adjust parameters if needed

### Step 6: Generate Data

1. Click "Generate Data"
2. Wait for generation (usually 1-5 seconds)
3. View validation results:
   - ✅ Green = Passed
   - ❌ Red = Failed
4. If validation fails, adjust parameters and regenerate

---

## Statistical Validation

### Normality Tests

**Tests Applied**:
- **Kolmogorov-Smirnov**: p > 0.05 indicates normality
- **Shapiro-Wilk**: p > 0.05 indicates normality
- **Skewness**: |skewness| < 2 is acceptable
- **Kurtosis**: |kurtosis| < 7 is acceptable

**Interpretation**:
- Most PLS-SEM analyses don't require perfect normality
- Severe non-normality can affect results

### Reliability Assessment

**Cronbach's Alpha (α)**:
- α ≥ 0.90: Excellent
- α ≥ 0.80: Good
- α ≥ 0.70: Acceptable
- α < 0.70: Poor (revise construct)

**Composite Reliability (CR)**:
- CR ≥ 0.90: Excellent
- CR ≥ 0.80: Good
- CR ≥ 0.70: Acceptable

**Average Variance Extracted (AVE)**:
- AVE ≥ 0.70: Good
- AVE ≥ 0.50: Acceptable
- AVE < 0.50: Poor (convergent validity issue)

### Validity Assessment

**Discriminant Validity**:

1. **Fornell-Larcker Criterion**:
   - Square root of AVE > correlations with other constructs
   - Ensures constructs are distinct

2. **HTMT (Heterotrait-Monotrait Ratio)**:
   - HTMT < 0.85: Discriminant validity confirmed (conservative)
   - HTMT < 0.90: Acceptable (liberal)

### Structural Model Assessment

**R² (Coefficient of Determination)**:
- R² ≥ 0.75: Substantial
- R² ≥ 0.50: Moderate
- R² ≥ 0.25: Weak
- R² < 0.25: Very weak

**f² (Effect Size)**:
- f² ≥ 0.35: Large effect
- f² ≥ 0.15: Medium effect
- f² ≥ 0.02: Small effect
- f² < 0.02: No effect

**VIF (Variance Inflation Factor)**:
- VIF < 3: Ideal (no multicollinearity)
- VIF < 5: Acceptable
- VIF ≥ 5: Problematic (multicollinearity issue)

**Path Coefficients**:
- Check significance: p < 0.05
- Check magnitude: β values
- Check direction: positive or negative

### Model Fit

**Goodness of Fit (GoF)**:
- GoF ≥ 0.36: Large
- GoF ≥ 0.25: Medium
- GoF ≥ 0.10: Small

---

## Exporting Data

### Available Formats

#### 1. CSV (Universal)
- Simple comma-separated values
- Import into any software
- Best for: General use

#### 2. Excel (.xlsx)
- Multiple sheets:
  - **Data**: Survey responses
  - **Constructs**: Item mapping
  - **Reliability**: Validation metrics
- Best for: Manual review, SPSS import

#### 3. SPSS (.sps)
- CSV data file + SPSS syntax file
- Includes:
  - Variable labels
  - Value labels (1-7 scale)
  - Import commands
- Best for: SPSS/AMOS analysis

#### 4. SmartPLS (.csv)
- Optimized for SmartPLS 4.0
- Direct import
- Includes model specification
- Best for: SmartPLS analysis

#### 5. JSON
- Full metadata
- Validation results included
- Programmatic access
- Best for: R, Python, custom analysis

### How to Export

1. Go to "Export" page
2. Select format
3. Click "Export as [Format]"
4. File downloads automatically
5. Import into your analysis software

---

## Advanced Features

### Sample Size Calculator

Calculate recommended sample size based on:
- Number of constructs
- Items per construct
- Desired power (0.8 recommended)
- Effect size (small/medium/large)

**Formula**:
- Minimum = 10 × max(paths to construct, items in construct)
- Recommended adjusts for effect size and power

### Model Templates

Pre-configured research models:
- **TAM** (Technology Acceptance Model)
- **UTAUT** (Unified Theory of Acceptance and Use of Technology)
- **TPB** (Theory of Planned Behavior)
- **CSR-Performance Model**

Use templates as starting points and customize.

### Missing Data Simulation

Add realistic missing data:
- **MCAR** (Missing Completely at Random)
- **MAR** (Missing at Random)
- **MNAR** (Missing Not at Random)

### Multi-Group Analysis

Generate data for different groups:
- Demographics-based groups
- Different effect sizes per group
- Test invariance

---

## Best Practices

### 1. Design Your Model First

Before using the tool:
- Draw your conceptual model
- Define all constructs and items
- Specify expected relationships
- Determine sample size

### 2. Use Realistic Parameters

- **Mean**: 4.0-6.0 for positive constructs
- **SD**: 0.8-1.5 for typical Likert data
- **Skewness**: -0.5 to 0.5 for mild asymmetry
- **Paths**: 0.2-0.6 for realistic effects

### 3. Balance Your Model

- 3-7 items per construct (4 is common)
- Not too many paths (avoid overfitting)
- Reasonable effect sizes (not all large)

### 4. Validate Before Use

Always:
- Run pre-validation
- Check all metrics pass
- Review correlation matrix
- Adjust if needed

### 5. Document Your Data

- Save generation parameters
- Note any adjustments made
- Keep validation report
- Document for teaching purposes

---

## FAQ

### Q: What sample size should I use?

**A**: General rule: **10 times** the larger of:
- Maximum paths pointing to any construct
- Maximum items in any construct

Example: 5 constructs, 4 items each, max 2 paths to a construct
- Minimum: 10 × max(4, 2) = 40
- Recommended: 200-300

### Q: Why is my data failing validation?

**A**: Common reasons:
1. **Conflicting parameters**: Mean=6.0 with negative skewness on 7-point scale
2. **Too many items**: Harder to achieve high reliability
3. **Path conflicts**: Circular paths or impossible correlations
4. **Extreme values**: Very high/low means with low SD

**Solution**: Adjust parameters more conservatively.

### Q: Can I use this data for my actual thesis?

**A**: **NO**. This generates **synthetic data** for:
- ✅ Learning statistical methods
- ✅ Practicing analysis software
- ✅ Teaching research methodology
- ❌ Actual research publication

### Q: What Likert scale should I use?

**A**: Most common in research:
- **7-point**: Most popular (balanced, good variance)
- **5-point**: Simpler, easier for respondents
- **10-point**: More granular

Recommendation: **7-point scale**

### Q: How do I import into SmartPLS?

**A**:
1. Export as "SmartPLS" format
2. Open SmartPLS 4.0
3. Create new project
4. Import CSV data
5. Build your model using the item mapping

### Q: Can I generate longitudinal data?

**A**: Current version generates cross-sectional data. For longitudinal:
- Generate multiple datasets
- Add time variable
- Adjust parameters for waves

### Q: What if I need more than 10,000 samples?

**A**: Current limit is 10,000 for:
- Performance reasons
- Typical research needs

For larger samples, generate multiple batches and combine.

### Q: How accurate are the validation tests?

**A**: The tool uses:
- Industry-standard algorithms
- Peer-reviewed formulas
- Same calculations as SPSS/SmartPLS

Validation results match commercial software.

### Q: Can I modify the generated data?

**A**: Yes! Export to Excel or CSV and:
- Add/remove cases
- Modify specific values
- Add more variables
- Adjust demographics

But validation may no longer hold.

---

## Example Workflow

### Complete Example: Technology Acceptance Study

**1. Define Model**

Constructs:
- Perceived Usefulness (PU) - 4 items
- Perceived Ease of Use (PEOU) - 4 items
- Intention to Use (ITU) - 3 items

Paths:
- PEOU → PU: β=0.45
- PU → ITU: β=0.60
- PEOU → ITU: β=0.25

**2. Set Item Parameters**

All items:
- Mean: 5.0-5.5 (positive attitude)
- SD: 1.0-1.2 (typical variation)
- Skewness: -0.3 to -0.5 (slight negative)
- Kurtosis: 0.0 (normal)

**3. Add Demographics**

- Age: 22-55, Mean=32, SD=8
- Gender: Male/Female/Other (48%/48%/4%)
- Education: High School/Bachelor/Master/PhD

**4. Generate**

- Sample Size: 300
- Likert Scale: 7-point
- Add Noise: Yes (0.05)

**5. Validate**

Check all metrics pass:
- Cronbach's Alpha > 0.8
- AVE > 0.5
- HTMT < 0.85
- VIF < 5

**6. Export**

- Export as SmartPLS CSV
- Import into SmartPLS 4.0
- Run PLS algorithm
- Analyze results

**7. Use for Teaching**

- Demonstrate PLS-SEM
- Show measurement model assessment
- Explain structural model
- Practice interpretation

---

## Support & Resources

### Documentation
- Setup Guide: docs/SETUP_GUIDE.md
- README: README.md
- API Docs: http://localhost:8000/api/docs

### References
- Hair et al. (2019) - PLS-SEM guidelines
- Henseler et al. (2015) - HTMT
- Fornell & Larcker (1981) - Discriminant validity

### Best Practices Resources
- SmartPLS documentation
- PLS-SEM books and tutorials
- Research methodology guides

---

**Remember**: This tool is for educational purposes only. Use responsibly and ethically!
