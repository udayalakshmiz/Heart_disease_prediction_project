**Heart Disease Prediction System**

**Project Overview**

The Heart Disease Prediction System is a machine learning-based application that predicts the likelihood of heart disease in a patient using medical parameters. This project aims to assist healthcare professionals in early diagnosis and decision-making.

**Objectives**

* Predict the presence of heart disease using patient data
* Compare multiple machine learning algorithms
* Improve model accuracy using hyperparameter tuning
* Visualize data insights using interactive plots

**Dataset**
Dataset Name: Heart Failure Prediction Dataset
Source: Kaggle
Link: https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction

**Dataset Description**

* The dataset contains 918 patient records and 11 clinical features ()
* It is created by combining multiple heart disease datasets (UCI repository) ()
* Used for predicting the presence of heart disease

**Technologies Used**

* Python
* NumPy
* Pandas
* Plotly (for visualization)
* Scikit-learn (Machine Learning)
* Google Colab

**Project Workflow**

1. **Data Collection**

   * Loaded dataset from Kaggle

2. **Data Preprocessing**

   * Handled missing values using KNN Imputer
   * Converted categorical data into numerical form
   * Removed duplicates and handled invalid values

3. **Exploratory Data Analysis (EDA)**

   * Histograms for distribution analysis
   * Sunburst charts for hierarchical relationships
   * Violin plots for feature comparison
   * Correlation analysis

4. **Feature Selection**

   * Selected relevant features based on correlation

5. **Model Building**

   * Logistic Regression
   * Support Vector Machine (SVM)
   * Decision Tree
   * Random Forest

6. **Model Evaluation**

   * Accuracy Score
   * F1 Score
   * Confusion Matrix

7. **Hyperparameter Tuning**

   * Used GridSearchCV to improve model performance

**Results**

| Model               | Performance |
| ------------------- | ----------- |
| Logistic Regression | Good        |
| SVM                 | Good        |
| Decision Tree       | Moderate    |
| Random Forest       | Best        |

* Random Forest achieved the highest performance due to ensemble learning.

**Visualizations**

* Interactive histograms
* Sunburst charts
* Violin plots
* Feature importance graph
* Confusion matrix

**How to Run the Project**

1. Open Google Colab
2. Upload the dataset to Google Drive
3. Update file path in the code
4. Run all cells step-by-step

**Future Enhancements**

* Build a web application using Flask or MERN stack
* Integrate real-time patient data
* Use advanced models like XGBoost or Deep Learning
* Implement Explainable AI (SHAP, LIME)
* Add multi-disease prediction capability

**Conclusion**

This project demonstrates the effectiveness of machine learning in predicting heart disease. It highlights how data preprocessing, visualization, and model optimization contribute to building a reliable predictive system.

**Author**

Zagabathuni Udaya Lakshmi
