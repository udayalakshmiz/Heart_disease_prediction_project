import numpy as np
import pandas as pd
import warnings
import os
import joblib
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

warnings.filterwarnings('ignore')

def train_and_export():
    print("Loading dataset...")
    heart_df = pd.read_csv('Dataset/heart.csv')

    print("Encoding categorical variables...")
    categorical_col = heart_df.select_dtypes(include='object').columns
    
    # Store mapping to use during prediction
    categorical_mapping = {}
    
    for col in categorical_col:
        unique_vals = heart_df[col].unique()
        mapping = {val: i for i, val in enumerate(unique_vals)}
        categorical_mapping[col] = mapping
        heart_df[col].replace(unique_vals, range(heart_df[col].nunique()), inplace=True)
    
    # Separate features and target before imputation to prevent data leakage and allow inference on just features
    X = heart_df.drop('HeartDisease', axis=1)
    y = heart_df['HeartDisease']

    print("Imputing missing values in Cholesterol...")
    X['Cholesterol'].replace(0, np.nan, inplace=True)
    chol_imputer = KNNImputer(n_neighbors=3)
    after_impute_chol = chol_imputer.fit_transform(X)
    X = pd.DataFrame(after_impute_chol, columns=X.columns)

    print("Imputing missing values in RestingBP...")
    X['RestingBP'].replace(0, np.nan, inplace=True)
    bp_imputer = KNNImputer(n_neighbors=3)
    after_impute_bp = bp_imputer.fit_transform(X)
    X = pd.DataFrame(after_impute_bp, columns=X.columns)

    withoutOldPeak = X.columns.drop('Oldpeak')
    X[withoutOldPeak] = X[withoutOldPeak].astype('int32')

    print("Training Random Forest model...")
    rfc = RandomForestClassifier(class_weight='balanced')
    param_grid = {
        'n_estimators': [50, 100],
        'max_features': ['sqrt', 'log2'],
        'max_depth': [3, 6, 9],
        'max_leaf_nodes': [3, 6]
    }
    
    print("Running GridSearchCV...")
    # Reduced the grid size slightly so it finishes reasonably fast
    grid_search = GridSearchCV(rfc, param_grid=param_grid, cv=3, n_jobs=-1).fit(X, y)
    print(f"Best parameters: {grid_search.best_params_}")
    
    rfctree = RandomForestClassifier(**grid_search.best_params_, class_weight='balanced').fit(X, y)
    
    print("Exporting model and artifacts...")
    os.makedirs('models', exist_ok=True)
    joblib.dump(rfctree, 'models/rf_model.pkl')
    joblib.dump(chol_imputer, 'models/chol_imputer.pkl')
    joblib.dump(bp_imputer, 'models/bp_imputer.pkl')
    joblib.dump(categorical_mapping, 'models/categorical_mapping.pkl')
    # Save column names to ensure ordering during inference
    joblib.dump(list(X.columns), 'models/feature_columns.pkl')
    
    print("Export successful!")

if __name__ == "__main__":
    train_and_export()
