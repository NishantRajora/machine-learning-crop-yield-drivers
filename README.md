# Crop Yield Driver Discovery using Feature Selection and XGBoost

## Overview
Agriculture is a critical sector in India, directly impacting food security and the national economy. Crop yield depends on multiple interacting factors such as climate conditions, soil characteristics, vegetation health, and agricultural practices. Traditional statistical approaches often struggle to model these complex and nonlinear relationships.

This project applies Machine Learning—specifically XGBoost combined with feature selection and explainable AI techniques—to:

- Predict crop yield with high accuracy  
- Identify and rank the most significant yield drivers  
- Select the best-performing model through rigorous evaluation  

The study focuses on Indian agricultural data and follows a reproducible end-to-end machine learning pipeline.

---

## Project Objectives
- Identify key factors influencing crop yield using feature selection methods  
- Train and optimize an XGBoost regression model  
- Compare XGBoost performance with baseline machine learning models  
- Interpret model predictions using SHAP (SHapley Additive Explanations)  
- Generate actionable insights for agricultural decision-making  

---

## Dataset Description
The project utilizes publicly available Indian agricultural datasets, which may include:

- Crop yield data (state/district level)  
- Weather data (rainfall, temperature, humidity)  
- Soil attributes  
- Remote sensing indices (NDVI, EVI)  
- Agricultural input variables (fertilizer usage, area sown)  

**Target Variable:** Crop Yield (e.g., tonnes per hectare)

---

## Tools and Technologies

**Programming Language:** Python  

**Machine Learning Models:**  
- XGBoost  
- Random Forest  
- Linear Regression  

**Feature Selection Techniques:**  
- Correlation-based filtering  
- Recursive Feature Elimination (RFE)  
- Embedded feature importance (XGBoost)  

**Explainability:**  
- SHAP  

**Libraries Used:**  
NumPy, Pandas, Scikit-learn, XGBoost, SHAP, Matplotlib, Seaborn  

---

## Methodology

### 1. Data Preprocessing
- Handling missing values  
- Feature scaling and encoding  
- Data normalization  

### 2. Feature Selection
- Correlation-based filtering  
- Recursive Feature Elimination (RFE)  
- Embedded feature importance from XGBoost  

### 3. Model Training
- XGBoost regression model  
- Hyperparameter tuning using cross-validation  

### 4. Model Evaluation
- Evaluation metrics: RMSE, MAE, R²  
- Performance comparison with baseline models  

### 5. Model Explainability
- SHAP values for global interpretation  
- SHAP analysis for local prediction explanations  
- Visualization of top yield drivers  

---

## Results
- XGBoost achieves superior predictive performance compared to baseline models  
- Feature selection improves model stability and reduces noise  
- SHAP analysis highlights weather variables and vegetation indices as dominant yield drivers  
- Results are interpretable and practically actionable  

---

## Key Insights
- Rainfall and temperature strongly influence crop yield  
- NDVI is a reliable indicator of crop health  
- Feature selection enhances both model performance and interpretability  
- Explainable AI bridges the gap between machine learning outputs and real-world agricultural decision-making  

---

## Ethical and Practical Considerations
- Model predictions are dependent on data quality and coverage  
- Outputs should support, not replace, expert agricultural guidance  
- Responsible interpretation is necessary for policy-level applications  

---

## Future Scope
- Crop-specific modeling (e.g., rice, wheat, maize)  
- Integration of real-time satellite data  
- Deployment as a web-based decision support system  
- Inclusion of socio-economic variables  
- Time-series forecasting for seasonal yield prediction  

---

## References
- https://www.sciencedirect.com/science/article/pii/S2772375524003228  
- https://pmc.ncbi.nlm.nih.gov/articles/PMC11667600/  
- https://www.sciencedirect.com/science/article/pii/S2772671124001918  
- https://www.mdpi.com/2077-0472/14/6/794  
- https://www.nature.com/articles/s44264-025-00052-6  

---

## Author
Nishant Rajora  
Undergraduate – Data Science  
The NorthCap University  

---

## Acknowledgements
This project was developed as part of an academic evaluation and is inspired by recent research in machine learning and precision agriculture.