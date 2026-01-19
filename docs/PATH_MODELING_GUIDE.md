# Path Modeling Guide

## Current Implementation: Direct Paths (A → B)

The current version supports **DIRECT PATHS** between constructs. This is the foundation for all structural models.

---

## ✅ What You CAN Do

### 1. Simple Direct Paths (A → B)
```
Trust → Satisfaction
```
**How to add:**
1. Create two constructs: `Trust`, `Satisfaction`
2. Add path: From=Trust, To=Satisfaction, Beta=0.5

### 2. Multiple Direct Paths
```
Trust → Satisfaction
Trust → Loyalty
Satisfaction → Loyalty
```
**How to add:**
1. Create three constructs
2. Add three separate paths

### 3. Mediation Model (Manual Setup)
For mediation analysis (A → B → C), create **TWO direct paths**:

```
Model: Trust → Satisfaction → Loyalty
```

**Setup:**
1. Create 3 constructs: `Trust`, `Satisfaction`, `Loyalty`
2. Add Path 1: From=Trust, To=Satisfaction, Beta=0.4
3. Add Path 2: From=Satisfaction, To=Loyalty, Beta=0.6

**Analysis:**
- **Direct effect**: Trust → Loyalty (add this path too with Beta=0.2)
- **Indirect effect**: Trust → Satisfaction → Loyalty (calculated in SmartPLS)
- **Total effect**: Direct + Indirect

### 4. Complex Models
```
           ┌─────────────┐
           │   Quality   │
           └──────┬──────┘
                  │
         ┌────────┴────────┐
         ↓                 ↓
    ┌────────┐      ┌──────────┐
    │  Trust │ ───→ │  Loyalty │
    └────────┘      └──────────┘
```

**Setup:**
1. Create 3 constructs
2. Add Path 1: Quality → Trust, Beta=0.5
3. Add Path 2: Quality → Loyalty, Beta=0.3
4. Add Path 3: Trust → Loyalty, Beta=0.4

---

## 📊 Real Example: Technology Acceptance Model (TAM)

### Constructs:
1. **Perceived Ease of Use (PEOU)** - 4 items
2. **Perceived Usefulness (PU)** - 4 items
3. **Intention to Use (ITU)** - 3 items

### Paths (All Direct):
1. PEOU → PU: Beta = 0.45 (Significant)
2. PU → ITU: Beta = 0.60 (Significant)
3. PEOU → ITU: Beta = 0.25 (Significant)

### In the Generator:
```
Step 1: Add Construct "PEOU" with 4 items
Step 2: Add Construct "PU" with 4 items
Step 3: Add Construct "ITU" with 3 items
Step 4: Add Path: PEOU → PU, Beta=0.45
Step 5: Add Path: PU → ITU, Beta=0.60
Step 6: Add Path: PEOU → ITU, Beta=0.25
Step 7: Generate!
```

---

## 🎯 How to Model Different Relationships

### Direct Effect Only
```
A → B
```
Add 1 path: A → B

### Mediation (Indirect Effect)
```
A → B → C
```
Add 2 paths:
- A → B
- B → C

For **full mediation analysis** in SmartPLS, also add:
- A → C (direct effect)

SmartPLS will calculate:
- Direct: A → C
- Indirect: A → B → C
- Total: Direct + Indirect

### Multiple Predictors
```
A → C
B → C
```
Add 2 paths:
- A → C
- B → C

### Chain Model
```
A → B → C → D
```
Add 3 paths:
- A → B
- B → C
- C → D

---

## 💡 Understanding Path Coefficients (Beta)

### Beta Value Guidelines:
- **Small effect**: 0.1 to 0.3
- **Medium effect**: 0.3 to 0.5
- **Large effect**: 0.5 to 0.7

### Example Settings:
```
Strong predictor: Beta = 0.6
Moderate predictor: Beta = 0.4
Weak predictor: Beta = 0.2
```

### Negative Relationships:
```
Negative effect: Beta = -0.3
(As A increases, B decreases)
```

---

## 🔧 Moderation (Interaction Effects)

**Current Version**: Moderation is NOT automatically calculated.

**Workaround**:
1. Generate your base data with main effects
2. Export to SPSS/SmartPLS
3. Create interaction term manually (A × M)
4. Run moderation analysis in SmartPLS

**Example:**
```
Main effects in generator:
- Quality → Satisfaction: Beta=0.5
- Trust → Satisfaction: Beta=0.4

Then in SmartPLS:
- Create Quality×Trust interaction
- Test moderation effect
```

---

## ✅ Best Practices

### 1. Start Simple
```
Begin with 2-3 constructs
Add 1-2 paths
Test and validate
```

### 2. Realistic Betas
```
Use values between 0.2 - 0.6
Avoid too many large effects (0.7+)
Balance positive relationships
```

### 3. Check VIF
```
Avoid multicollinearity
Don't make too many paths to same construct
Keep VIF < 5
```

### 4. Model Fit
```
With 2-3 constructs: Keep it simple
With 4+ constructs: More complex OK
Always validate results
```

---

## 📝 Quick Reference

| Relationship Type | Paths to Add | Example |
|-------------------|--------------|---------|
| Direct | 1 path | A → B |
| Mediation | 2+ paths | A → B, B → C |
| Multiple IVs | Multiple paths | A → C, B → C |
| Chain | Sequential paths | A → B → C → D |
| Complex | All connections | Multiple paths |

---

## 🎓 Advanced: Mediation Analysis in SmartPLS

After generating data:

**Full Mediation Model:**
```
Generator Setup:
- Path 1: A → B (mediator)
- Path 2: B → C (outcome)
- Path 3: A → C (direct)

SmartPLS Analysis:
1. Import generated data
2. Build model with all 3 paths
3. Run PLS Algorithm
4. Run Bootstrapping
5. Check:
   - Direct effect (A → C)
   - Indirect effect (A → B → C)
   - Total effect
   - % mediation
```

**Interpretation:**
- If direct effect becomes non-significant → Full mediation
- If direct effect reduces but still significant → Partial mediation
- If indirect not significant → No mediation

---

## 💡 Tips

1. **Always test first** with simple 2-construct model
2. **Use realistic betas** (0.2-0.6 range)
3. **Check correlations** in validation results
4. **Export and verify** in SmartPLS
5. **Adjust if needed** and regenerate

---

## 🚀 Future Enhancements (Planned)

- Automatic mediation path setup
- Moderation effect calculation
- Interaction term generation
- Multi-level models
- Curvilinear relationships

---

## Need Help?

**Example Models**: See templates in the Generator page

**Documentation**: Check USER_MANUAL.md for detailed examples

**Quick Start**: QUICKSTART.md for simple walkthrough

---

**Current Version**: Direct paths (A → B) only
**Analysis**: Use SmartPLS for mediation/moderation calculations
**Flexibility**: Supports any model structure via multiple direct paths
