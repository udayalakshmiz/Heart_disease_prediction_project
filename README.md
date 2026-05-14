# CardioDetect — Heart Disease Prediction System

A full-stack machine learning web application that predicts the likelihood of heart disease using clinical parameters. Built with a React frontend, Flask REST API backend, and a Random Forest classifier trained on 918 patient records.

---

## Live Demo Preview

> Input patient vitals → Get instant risk assessment with probability score and clinical guidance.

---

## Project Structure

```
heart-disease-prediction/
│
├── Dataset/
│   └── heart.csv                  # Kaggle heart failure dataset (918 records)
│
├── models/                        # Auto-generated after training
│   ├── rf_model.pkl
│   ├── chol_imputer.pkl
│   ├── bp_imputer.pkl
│   ├── categorical_mapping.pkl
│   └── feature_columns.pkl
│
├── backend/
│   ├── app.py                     # Flask REST API
│   └── requirements.txt           # Python dependencies
│
├── frontend/
│   ├── src/                       # React components
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── train_and_export.py            # Model training + artifact export
└── Heart_Disease_Predictor.ipynb  # Original EDA + model exploration notebook
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Vite |
| Backend | Flask, Flask-CORS |
| ML Model | Scikit-learn (Random Forest) |
| Data Processing | Pandas, NumPy, KNN Imputer |
| Model Persistence | Joblib |
| EDA & Visualization | Plotly |

---

## Dataset

**Name:** Heart Failure Prediction Dataset  
**Source:** [Kaggle — fedesoriano](https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction)  
**Records:** 918 patients | **Features:** 11 clinical inputs + 1 target  
**Origin:** Combined from multiple UCI heart disease datasets

### Features

| Feature | Description |
|---|---|
| Age | Patient age in years |
| Sex | Biological sex (M/F) |
| ChestPainType | TA, ATA, NAP, ASY |
| RestingBP | Resting blood pressure (mm Hg) |
| Cholesterol | Serum cholesterol (mg/dl) |
| FastingBS | Fasting blood sugar > 120 mg/dl (1/0) |
| RestingECG | Normal, ST, LVH |
| MaxHR | Maximum heart rate achieved |
| ExerciseAngina | Exercise-induced angina (Y/N) |
| Oldpeak | ST depression induced by exercise |
| ST_Slope | Slope of peak exercise ST segment (Up/Flat/Down) |
| **HeartDisease** | **Target: 1 = disease, 0 = normal** |

---

## ML Pipeline

### 1. Data Preprocessing
- Replaced invalid `0` values in `Cholesterol` and `RestingBP` with `NaN`
- Applied **KNN Imputer** (k=3) separately for each field to prevent data leakage
- Label-encoded categorical features using a stored mapping (for consistent inference)
- Removed duplicate records

### 2. Exploratory Data Analysis (Notebook)
- Distribution histograms per feature
- Sunburst charts for hierarchical relationships
- Violin plots for feature comparison across disease classes
- Correlation heatmap for feature selection

### 3. Models Trained & Compared

| Model | Performance |
|---|---|
| Logistic Regression | Good |
| Support Vector Machine | Good |
| Decision Tree | Moderate |
| **Random Forest** | **Best** |

### 4. Hyperparameter Tuning
Used `GridSearchCV` (3-fold CV) to optimize:
- `n_estimators`: [50, 100]
- `max_features`: ['sqrt', 'log2']
- `max_depth`: [3, 6, 9]
- `max_leaf_nodes`: [3, 6]

Random Forest with `class_weight='balanced'` achieved the best results due to ensemble learning and robustness to class imbalance.

---

## How to Run

### Prerequisites
- Python 3.8+
- Node.js 18+

---

### Step 1 — Train and Export the Model

```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Place heart.csv inside a Dataset/ folder, then run:
python train_and_export.py
```

This generates all `.pkl` files inside the `models/` directory.

---

### Step 2 — Start the Flask Backend

```bash
cd backend
python app.py
```

Backend runs at `http://localhost:5000`

**API Endpoint:**
```
POST /predict
Content-Type: application/json

{
  "Age": 52, "Sex": "M", "ChestPainType": "ASY",
  "RestingBP": 160, "Cholesterol": 340, "FastingBS": 1,
  "RestingECG": "LVH", "MaxHR": 105, "ExerciseAngina": "Y",
  "Oldpeak": 3.5, "ST_Slope": "Flat"
}
```

**Response:**
```json
{
  "prediction": 1,
  "probability": 0.87,
  "message": "Heart disease detected"
}
```

---

### Step 3 — Start the React Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

---

## Test Cases

Use these to verify the end-to-end system:

| Case | Age | Sex | ChestPain | BP | Cholesterol | MaxHR | ExAngina | Oldpeak | STSlope | Expected |
|---|---|---|---|---|---|---|---|---|---|---|
| Low Risk | 35 | F | ATA | 120 | 200 | 175 | No | 0.0 | Up | ✅ No Disease |
| Borderline | 52 | M | NAP | 140 | 260 | 140 | No | 1.5 | Flat | ⚠️ Moderate |
| High Risk | 63 | M | ASY | 160 | 340 | 105 | Yes | 3.5 | Flat | 🔴 Disease |
| Very High Risk | 70 | M | ASY | 180 | 400 | 90 | Yes | 5.0 | Down | 🔴 Disease |

---

## Key Risk Factors (by feature importance)

1. **ASY Chest Pain** — strongest single predictor
2. **ST Slope = Flat / Down** — high-risk signal
3. **Exercise-Induced Angina** — strong indicator
4. **Low Maximum Heart Rate** — inverse correlation with health
5. **High Oldpeak** — significant ST depression

---

## Disclaimer

> ⚠️ This tool is for **educational and informational purposes only**. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for medical decisions.

---

## Future Enhancements

- [ ] XGBoost / LightGBM model comparison
- [ ] SHAP values for explainable predictions
- [ ] Real-time patient data integration
- [ ] Multi-disease prediction support
- [ ] Docker containerization for easy deployment
- [ ] CI/CD pipeline

---

## Author

**Zagabathuni Udaya Lakshmi**  
Heart Disease Prediction System — Full Stack ML Project
