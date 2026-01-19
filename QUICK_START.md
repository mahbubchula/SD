# Quick Start Guide - Testing Indirect Effects

**Status:** All features working ✅ | Backend verified ✅ | Ready to test!

---

## 🚀 START SERVERS (2 Terminals)

### Terminal 1 - Backend
```bash
cd E:\06_GitHub_Repo\01_Active_Projects\advanced-survey-data-generator\backend
python -m uvicorn app.main:app --reload
```
✅ Wait for: `INFO: Application startup complete.`

### Terminal 2 - Frontend ⚠️ RESTART IF ALREADY RUNNING
```bash
# If running: Press Ctrl+C to stop first!
cd E:\06_GitHub_Repo\01_Active_Projects\advanced-survey-data-generator\frontend
npm run dev
```
✅ Wait for: `Local: http://localhost:3000/`

---

## 📊 TEST MEDIATION MODEL (5 Minutes)

### Step 1: Login
1. Open http://localhost:3000
2. Register/Login

### Step 2: Create Mediation Model in Generator

**Add 3 Constructs:**
- Click "Add Construct" → Name: **Trust** (keep 3 items)
- Click "Add Construct" → Name: **Quality** (keep 3 items)
- Click "Add Construct" → Name: **Satisfaction** (keep 3 items)

**Add 3 Paths (creates mediation):**
1. Click "Add Path"
   - From: Trust
   - To: Quality
   - Beta: **0.5**

2. Click "Add Path"
   - From: Quality
   - To: Satisfaction
   - Beta: **0.6**

3. Click "Add Path"
   - From: Trust
   - To: Satisfaction
   - Beta: **0.2**

**Generate:**
- Sample Size: 300
- Click "Generate Data"
- ✅ Wait for success message

### Step 3: Verify Validation Page (CRITICAL TEST)

**Click "Validation" in navigation**

✅ **You SHOULD see:**
- ✅ Real data (NOT "No Data Available")
- ✅ Section: "Indirect Effects (Mediation)" with ✨ NEW badge
- ✅ Table row: Trust → Quality → Satisfaction
- ✅ Indirect Effect: ~0.3 (because 0.5 × 0.6 = 0.3)
- ✅ Section: "Total Effects" with ✨ NEW badge
- ✅ Direct: 0.2, Indirect: 0.3, Total: 0.5
- ✅ VAF%: ~60%
- ✅ Moderation Analysis section
- ✅ Cross-Loadings section

❌ **If you see:**
- "No Validation Data Available" → You need to restart frontend!
- No Indirect Effects section → Frontend not restarted

---

## 🔧 TROUBLESHOOTING

### Problem: "No Validation Data Available"

**Solution:**
```bash
# In frontend terminal:
Ctrl+C  (stop frontend)
npm run dev  (restart)
```
Then clear browser cache: `Ctrl + Shift + R`

### Problem: Indirect Effects section not visible

**Check Browser Console:**
1. Press F12 (open DevTools)
2. Go to Console tab
3. Look for errors

**Check LocalStorage:**
1. Press F12
2. Go to Application tab
3. Click "Local Storage" → http://localhost:3000
4. Click on `validation_results`
5. Verify `structural_model` → `indirect_effects` exists

**If empty:** Your model doesn't have a mediation chain
- Need: A → B AND B → C (creates A → B → C)

---

## 📥 TEST EXPORT

1. Go to "Export" page
2. Click "Export as Excel"
3. Open downloaded .xlsx file
4. ✅ Verify sheets exist:
   - Data
   - Reliability
   - HTMT
   - Path Coefficients
   - **Indirect Effects** ← NEW
   - **Total Effects** ← NEW
   - R-Squared
   - VIF

---

## ✅ SUCCESS CHECKLIST

Your system works if ALL are true:

- ✅ Backend running (no errors)
- ✅ Frontend running (no errors)
- ✅ Can create 3 constructs
- ✅ Can create 3 paths (forming A→B→C chain)
- ✅ Can generate 300 samples
- ✅ Validation page shows REAL data
- ✅ **"Indirect Effects" section exists with ✨ NEW badge**
- ✅ **Table shows: Trust → Quality → Satisfaction**
- ✅ **Indirect effect value shown (~0.3)**
- ✅ **"Total Effects" section exists**
- ✅ **Shows Direct, Indirect, Total, VAF%**
- ✅ Excel export has "Indirect Effects" sheet
- ✅ Excel export has "Total Effects" sheet

---

## 📖 EXPECTED RESULTS

### Mediation Path
```
Trust → Quality → Satisfaction

Calculations:
  beta(Trust→Quality) = 0.5
  beta(Quality→Satisfaction) = 0.6

  Indirect Effect = 0.5 × 0.6 = 0.3
  Direct Effect = 0.2
  Total Effect = 0.2 + 0.3 = 0.5
  VAF% = (0.3 / 0.5) × 100 = 60%
  Mediation Type = Partial (because direct path exists)
```

### What Each Section Shows

**Direct Effects:**
- Trust → Quality: beta ≈ 0.5
- Quality → Satisfaction: beta ≈ 0.6
- Trust → Satisfaction: beta ≈ 0.2

**Indirect Effects (NEW):**
- Trust → Quality → Satisfaction
- Indirect Effect: ~0.3
- z-score, p-value, significance

**Total Effects (NEW):**
- From: Trust, To: Satisfaction
- Mediator: Quality
- Direct: 0.2, Indirect: 0.3, Total: 0.5
- VAF: 60%, Type: Partial mediation

**Moderation (NEW):**
- Tests Quality×Trust, Trust×Quality interactions
- Shows ΔR², f² effect sizes

**Cross-Loadings (NEW):**
- Each item loads highest on own construct
- Validates discriminant validity

---

## 🎯 WHAT'S NEW

### Features Added (All Working ✅):

1. **Indirect Effects (Mediation Analysis)**
   - Detects A → B → C paths
   - Calculates indirect effects (beta_AB × beta_BC)
   - Sobel test for significance
   - Shows on Validation page with ✨ NEW badge

2. **Total Effects**
   - Combines Direct + Indirect
   - Calculates VAF% (Variance Accounted For)
   - Determines mediation type (Full/Partial)
   - Shows on Validation page with ✨ NEW badge

3. **Moderation Analysis**
   - Creates interaction terms (X × M)
   - Calculates ΔR² and f² effect sizes
   - Determines Small/Medium/Large effects
   - Shows on Validation page with ✨ NEW badge

4. **Cross-Loadings**
   - Item loadings on all constructs
   - Validates discriminant validity
   - Shows on Validation page with ✨ NEW badge

5. **Enhanced Excel Export**
   - Added "Indirect Effects" sheet
   - Added "Total Effects" sheet
   - Added "Moderation" data (if detected)

---

## 📞 VERIFIED BY BACKEND TEST

Test result: **ALL TESTS PASSED ✅**

```
[OK] Indirect Effects (Mediation) working
[OK] Total Effects (Direct + Indirect) working
[OK] Moderation Analysis working
[OK] Cross-Loadings working
[OK] JSON serialization working
```

Test file: `backend/test_complete_system.py`

---

## 🔄 IF YOU NEED TO RESET

### Clear All Data:
1. Open DevTools (F12)
2. Application tab → Local Storage
3. Right-click http://localhost:3000 → Clear
4. Refresh page (F5)

### Start Fresh:
1. Stop both servers (Ctrl+C)
2. Start backend
3. Start frontend
4. Register new account
5. Create model again

---

## 💡 TIPS

### For Best Results:
- Use sample size ≥ 300
- Use beta values 0.3-0.7 for significant effects
- Create clear mediation chains (A→B→C)
- Keep item mean ≈ 4-5, SD ≈ 1.0-1.5

### Understanding Output:
- **Significant** = p-value < 0.05
- **R² > 0.25** = Weak to Moderate fit
- **VAF > 80%** = Full mediation
- **VAF 20-80%** = Partial mediation
- **HTMT < 0.85** = Discriminant validity OK

---

## 📚 MORE INFO

- Full checklist: `VERIFICATION_CHECKLIST.md`
- System status: `SYSTEM_STATUS.md`
- Startup guide: `STARTUP_COMMANDS.md`

---

**Ready to test? Start with Terminal 1 (Backend) above! 🚀**
