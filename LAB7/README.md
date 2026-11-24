# Lab 7: Fuzz Testing with Hypothesis
**Domain:** Blood Donation Screening System (`processor.py`)  
**Student Name:** P Manas Siddhardha  
**SRN:** PES1UG24AM186  
**Repository:** [SETAPESU26/L6_L7_05_blood_donation_screening](https://github.com/SETAPESU26/L6_L7_05_blood_donation_screening)  

---

## 📌 Deliverables Overview

All required deliverables for Lab 7 are present directly in this folder:

| # | Deliverable | File Path | Description |
|---|---|---|---|
| 1 | **Lab Report with Screenshots (PDF)** | [`PES1UG24AM186_LAB7_REPORT.pdf`](PES1UG24AM186_LAB7_REPORT.pdf) | Complete 7-page academic report containing methodology, terminal screenshots for all steps, bug analysis table, before/after comparisons, reflection Q&A, and full source code. |
| 2 | **Fixed Application Python Script** | [`processor.py`](processor.py) | Hardened implementation defending against invalid types, out-of-bound indices, missing tokens, division by zero, NaN/Inf, and physiological boundary violations. |
| 3 | **Updated Fuzz Test Suite** | [`test_processor.py`](test_processor.py) | Property-based fuzz test suite using Hypothesis (`@given(st.text() \| st.none())`) with defensive assertion harnesses. |
| 4 | **Screenshots Directory** | [`screenshots/`](screenshots/) | High-resolution terminal captures documenting Steps 2, 4, 5, and 6. |

---

## 🧪 Summary of Results

| Target Function | Test Property | Buggy Code Result | Hardened Code Result |
|---|---|---|---|
| `validate_blood_type` | `test_validate_blood_type_no_crash` | ❌ **FAILED** (`AttributeError`, `IndexError`, `KeyError`) | ✅ **PASSED** (100+ fuzzed runs, 0 crashes) |
| `calculate_pulse_pressure` | `test_calculate_pulse_pressure_safe` | ❌ **FAILED** (`AttributeError`, `ValueError`, `ZeroDivisionError`) | ✅ **PASSED** (100+ fuzzed runs, 0 crashes) |
| `parse_donor_registry` | `test_parse_donor_registry_safe` | ❌ **FAILED** (`AttributeError`, `IndexError`, `ValueError`) | ✅ **PASSED** (100+ fuzzed runs, 0 crashes) |

---

## 🚀 Execution Instructions

### 1. Install Dependencies
```bash
pip install hypothesis pytest reportlab
```

### 2. Run the Hardened Application
```bash
python processor.py
```

### 3. Run Hypothesis Fuzz Tests
```bash
python -m pytest test_processor.py -v
```

### 4. Rebuild Deliverable PDF & Screenshots (Optional)
```bash
python generate_screenshots.py
python build_report_pdf.py
```
