# Quick Reference Guide

## 🚀 Quick Start (2 minutes)

### 1. Clone & Install
```bash
git clone https://github.com/1511Darshan/AICTE-FIRE-CLASSIFICATION.git
cd AICTE-FIRE-CLASSIFICATION
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Download Data (or use sample)
```bash
# Option A: Use built-in sample dataset (no download needed!)
jupyter notebook                  # Open any notebook

# Option B: Download raw data from NASA FIRMS
# 1. Visit https://firms.modaps.eosdis.nasa.gov/download/
# 2. Select India, 2021-2023, CSV format
# 3. Extract to data/raw/
```

### 3. Run Analysis
```bash
# See notebook analysis
jupyter notebook

# Or use modular Python scripts (once created)
python -c "from src.data_load import load_modis_batch; df = load_modis_batch('data/raw/')"
```

---

## 📂 Repository Structure

```
.
├── README.md                       # Main documentation
├── IMPROVEMENTS.md                 # This file
├── LICENSE                         # MIT License
├── CONTRIBUTING.md                 # Contribution guidelines
├── requirements.txt                # Python dependencies (pip install -r)
├── .gitignore                      # Git rules (excludes large CSVs)
│
├── data/
│   ├── raw/                        # ⚠️ Large CSVs (not tracked)
│   ├── sample/                     # ✅ Small sample (tracked, ~1 MB)
│   └── metadata.md                 # Column descriptions & provenance
│
├── src/                            # Python modules (reusable code)
│   ├── __init__.py
│   ├── data_load.py                # Load & validate data
│   ├── preprocess.py               # Clean, filter, handle missing values
│   ├── features.py                 # Feature engineering
│   ├── train.py                    # Model training
│   └── evaluate.py                 # Metrics & reporting
│
├── notebooks/                      # Jupyter notebooks
│   ├── exploration.ipynb           # (to be created: EDA)
│   └── report.ipynb                # (to be created: clean results)
│
├── config/
│   └── train.yaml                  # Hyperparameters & configuration
│
├── tests/                          # Unit tests
│   ├── __init__.py
│   └── test_preprocess.py          # Tests for preprocessing
│
├── models/                         # Saved model artifacts (not tracked)
│   └── .gitkeep
│
└── .github/workflows/
    └── ci.yml                      # GitHub Actions CI pipeline
```

---

## 🔧 Common Tasks

### Load and Preprocess Data
```python
import src.data_load as dl
import src.preprocess as pp

# Load
df = dl.load_modis_csv('data/raw/modis_2023_India.csv')

# Preprocess (full pipeline)
df = pp.full_preprocessing_pipeline(df, confidence_threshold=50)

# Save
dl.save_modis_csv(df, 'data/processed/clean_2023.csv')
```

### Feature Engineering
```python
import src.features as feat

df = feat.engineer_all_features(df)
df_scaled, scaler = feat.scale_features(df[feature_cols])
selected_features, selector = feat.select_best_features(df_scaled, df['type'], k=10)
```

### Train Models
```python
from sklearn.model_selection import train_test_split
import src.train as train_module

X = df[feature_cols]
y = df['type']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Train
rf_model = train_module.train_random_forest(X_train, y_train)
results = train_module.evaluate_model(rf_model, X_test, y_test, "Random Forest")
```

### Evaluate Results
```python
import src.evaluate as eval_module

# Per-class metrics
metrics = eval_module.compute_per_class_metrics(y_test, y_pred)

# Feature importance
importance_df = eval_module.feature_importance_summary(rf_model, feature_cols, top_k=10)
```

---

## 📊 Key Files

| File | Purpose |
|------|---------|
| `README.md` | 📖 Main overview & quickstart |
| `data/metadata.md` | 📋 Data dictionary & provenance |
| `requirements.txt` | 📦 Python dependencies |
| `src/data_load.py` | 💾 Data I/O & validation |
| `src/preprocess.py` | 🧹 Data cleaning |
| `src/features.py` | ⚙️ Feature engineering |
| `src/train.py` | 🤖 Model training |
| `src/evaluate.py` | 📊 Evaluation metrics |
| `config/train.yaml` | ⚙️ Hyperparameters |
| `tests/test_preprocess.py` | ✅ Unit tests |

---

## ✅ Reproducibility Checklist

- ✅ **Dependencies locked** → `requirements.txt`
- ✅ **Random seeds fixed** → `random_state=42` everywhere
- ✅ **Data documented** → `data/metadata.md` with column descriptions
- ✅ **Data provenance** → Attributed to NASA FIRMS
- ✅ **Code modular** → Reusable functions in `src/`
- ✅ **Configuration centralized** → `config/train.yaml`
- ✅ **Results tracked** → Baseline metrics in `README.md`
- ✅ **License clear** → MIT License
- ✅ **CI/CD setup** → `.github/workflows/ci.yml`
- ✅ **Tests provided** → `tests/test_preprocess.py` (expandable)

---

## 🔗 Important Links

- **NASA FIRMS**: https://firms.modaps.eosdis.nasa.gov/ (data source)
- **GitHub Issues**: Report bugs here
- **Pull Requests**: Submit improvements
- **Project Board**: Track development

---

## ⚠️ Known Limitations

1. **MODIS accuracy**: ±0.5 km (Terra), ±1–2 km (Aqua)
2. **Class imbalance**: Vegetation fires dominate (~70%)
3. **Temporal lag**: NRT data ~3 hours, Standard ~1 day
4. **False positives**: Clouds, flares, urban heat (2–5%)

### Mitigation Strategies

- Use `confidence >= 75` for critical applications
- Stratified train/test splits
- Report F1 per class (not just accuracy)
- Apply domain expert validation

---

## 🚀 Next Steps

1. **Short-term** (today):
   - Download sample data or use built-in sample
   - Run preprocessing pipeline
   - Train models and compare

2. **Medium-term** (this week):
   - Create `notebooks/exploration.ipynb` with EDA
   - Extract & clean data from main notebook
   - Run unit tests: `pytest tests/`

3. **Long-term** (optional):
   - Add geospatial analysis (geopandas, folium)
   - Create Streamlit demo app
   - Add SHAP explainability
   - Deploy to cloud

---

## 📞 Need Help?

- 📖 **Quick questions**: Check `README.md`
- 📊 **Data questions**: See `data/metadata.md`
- 👨‍💻 **How to contribute**: Read `CONTRIBUTING.md`
- 🐛 **Report bugs**: GitHub Issues

---

**Last updated**: November 19, 2025  
**Version**: 0.1.0  
**Status**: ✅ Ready for use
