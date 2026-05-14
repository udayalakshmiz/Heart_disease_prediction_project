import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Restrict CORS to specific frontend origin for better security
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

# Global variables for model artifacts
MODEL_ARTIFACTS = {
    'rf_model': None,
    'chol_imputer': None,
    'bp_imputer': None,
    'categorical_mapping': None,
    'feature_columns': None,
    'loaded': False
}

def load_artifacts():
    """Startup guard to load model artifacts with error handling."""
    MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    try:
        MODEL_ARTIFACTS['rf_model'] = joblib.load(os.path.join(MODEL_DIR, 'rf_model.pkl'))
        MODEL_ARTIFACTS['chol_imputer'] = joblib.load(os.path.join(MODEL_DIR, 'chol_imputer.pkl'))
        MODEL_ARTIFACTS['bp_imputer'] = joblib.load(os.path.join(MODEL_DIR, 'bp_imputer.pkl'))
        MODEL_ARTIFACTS['categorical_mapping'] = joblib.load(os.path.join(MODEL_DIR, 'categorical_mapping.pkl'))
        MODEL_ARTIFACTS['feature_columns'] = joblib.load(os.path.join(MODEL_DIR, 'feature_columns.pkl'))
        MODEL_ARTIFACTS['loaded'] = True
        print("✓ All model artifacts loaded successfully.")
    except Exception as e:
        print(f"✗ CRITICAL ERROR: Failed to load model artifacts: {e}")
        MODEL_ARTIFACTS['loaded'] = False

# Initialize artifacts on startup
load_artifacts()

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint for monitoring the API and model status."""
    if MODEL_ARTIFACTS['loaded']:
        return jsonify({'status': 'healthy', 'model_loaded': True}), 200
    else:
        return jsonify({
            'status': 'degraded', 
            'model_loaded': False,
            'error': 'Model artifacts failed to load. Please check the models/ directory.'
        }), 503

@app.route('/predict', methods=['POST'])
def predict():
    # Check if models are loaded before processing
    if not MODEL_ARTIFACTS['loaded']:
        return jsonify({'error': 'Prediction service is currently unavailable (model not loaded).'}), 503

    try:
        data = request.json
        print(f"Received data: {data}")
        
        # Create DataFrame from input
        df = pd.DataFrame([data])
        
        # Ensure we have all necessary columns
        feature_cols = MODEL_ARTIFACTS['feature_columns']
        for col in feature_cols:
            if col not in df.columns:
                return jsonify({'error': f'Missing column: {col}'}), 400
        
        # Validation for numeric ranges
        validation_ranges = {
            'Age': (1, 120),
            'RestingBP': (60, 250),
            'Cholesterol': (0, 600),
            'MaxHR': (60, 220),
            'Oldpeak': (-2.6, 6.2)
        }
        
        for col, (min_val, max_val) in validation_ranges.items():
            if col in df.columns:
                val = float(df[col].iloc[0])
                if val < min_val or val > max_val:
                    return jsonify({'error': f'{col} must be between {min_val} and {max_val}'}), 400
                
        # Reorder columns to match training
        df = df[feature_cols]
        
        # Apply categorical mapping with strict checking
        cat_mapping = MODEL_ARTIFACTS['categorical_mapping']
        for col, mapping in cat_mapping.items():
            if col in df.columns:
                val = df[col].iloc[0]
                if val not in mapping:
                    return jsonify({'error': f'Invalid value for {col}: {val}'}), 400
                df[col] = mapping[val]
                
        # Replace 0s with NaN for imputation (specifically for BP and Cholesterol)
        df['Cholesterol'] = df['Cholesterol'].replace(0, np.nan)
        df['RestingBP'] = df['RestingBP'].replace(0, np.nan)
        
        # Apply imputation using stored imputers
        df_chol_imputed = MODEL_ARTIFACTS['chol_imputer'].transform(df)
        df = pd.DataFrame(df_chol_imputed, columns=df.columns)
        
        df_bp_imputed = MODEL_ARTIFACTS['bp_imputer'].transform(df)
        df = pd.DataFrame(df_bp_imputed, columns=df.columns)
        
        # Convert types as in training
        withoutOldPeak = df.columns.drop('Oldpeak')
        df[withoutOldPeak] = df[withoutOldPeak].astype('int32')
        
        # Predict using stored model
        rf_model = MODEL_ARTIFACTS['rf_model']
        prediction = rf_model.predict(df)[0]
        
        # Calculate probability
        probability = rf_model.predict_proba(df)[0][1] if hasattr(rf_model, 'predict_proba') else None
        
        return jsonify({
            'prediction': int(prediction),
            'probability': float(probability) if probability is not None else None,
            'message': 'High Risk Detected' if prediction == 1 else 'Low Risk Detected'
        })
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
