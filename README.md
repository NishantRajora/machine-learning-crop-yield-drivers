# 🌾 Crop Yield Driver Discovery using Feature Selection & XGBoost

## 📌 Overview
Agriculture is a critical sector in India, directly impacting food security and the economy. Crop yield depends on several interacting factors such as climate, soil conditions, vegetation health, and farming practices. Traditional statistical methods often fail to model these complex, nonlinear relationships.

This project applies **Machine Learning**, specifically **XGBoost combined with feature selection and explainable AI**, to:
- Predict crop yield accurately
- Identify and rank the most important yield drivers
- Select the best-performing model through rigorous evaluation

The project focuses on **Indian agricultural data** and follows a reproducible end-to-end ML pipeline.

---

## 🎯 Project Objectives
- Identify key factors affecting crop yield using feature selection
- Train and tune an XGBoost regression model
- Compare XGBoost with baseline ML models
- Interpret predictions using SHAP
- Provide actionable insights for agricultural decision-making

---

## 📂 Project Structure
crop-yield-driver-discovery/
│
├── data/
│ ├── raw/ # Original datasets
│ ├── processed/ # Cleaned and transformed data
│
├── notebooks/
│ ├── 01_data_analysis.ipynb
│ ├── 02_feature_selection.ipynb
│ ├── 03_model_training.ipynb
│ ├── 04_model_evaluation.ipynb
│ ├── 05_model_explainability.ipynb
│
├── src/
│ ├── preprocessing.py
│ ├── feature_selection.py
│ ├── train_model.py
│ ├── evaluate_model.py
│
├── results/
│ ├── metrics/
│ ├── feature_importance/
│ ├── shap_plots/
│
├── requirements.txt
├── README.md
└── LICENSE


---

## 📊 Dataset Description
The project uses publicly available **Indian agricultural datasets**, which may include:
- Crop yield data (state/district level)
- Weather data (rainfall, temperature, humidity)
- Soil attributes
- Remote sensing indices (NDVI, EVI)
- Agricultural inputs (fertilizer usage, area sown)

**Target Variable:** Crop Yield (e.g., tonnes/hectare)

---

## 🛠️ Tools & Technologies
- **Language:** Python  
- **Machine Learning:** XGBoost, Random Forest, Linear Regression  
- **Feature Selection:** RFE, filter methods, embedded methods  
- **Explainability:** SHAP  
- **Libraries:** NumPy, Pandas, Scikit-learn, XGBoost, SHAP, Matplotlib, Seaborn  

---

## ⚙️ Methodology
1. **Data Preprocessing**
   - Missing value handling
   - Feature scaling and encoding
   - Data normalization

2. **Feature Selection**
   - Correlation-based filtering
   - Recursive Feature Elimination (RFE)
   - Embedded feature importance from XGBoost

3. **Model Training**
   - XGBoost regression model
   - Hyperparameter tuning using cross-validation

4. **Model Evaluation**
   - Metrics: RMSE, MAE, R²
   - Comparison with baseline models

5. **Model Explainability**
   - SHAP values for global and local interpretation
   - Visualization of top yield drivers

---

## 📈 Results
- XGBoost achieves superior predictive accuracy
- Feature selection improves stability and reduces noise
- SHAP highlights weather and vegetation indices as dominant yield drivers
- Results are interpretable and actionable

---

## 📌 Key Insights
- Rainfall and temperature strongly influence yield
- NDVI is a reliable indicator of crop health
- Feature selection enhances both performance and interpretability
- Explainable AI bridges ML outputs and real-world decisions

---

## ⚖️ Ethical & Practical Considerations
- Model predictions depend on data quality
- Outputs should support—not replace—expert agricultural advice
- Responsible interpretation is essential for policy usage

---

## 🚀 Future Scope
- Crop-specific modeling (rice, wheat, maize)
- Integration of real-time satellite data
- Deployment as a web-based decision support system
- Inclusion of socio-economic variables
- Time-series forecasting for seasonal yield prediction

---

## 📚 References
- https://www.sciencedirect.com/science/article/pii/S2772375524003228  
- https://pmc.ncbi.nlm.nih.gov/articles/PMC11667600/  
- https://www.sciencedirect.com/science/article/pii/S2772671124001918  
- https://www.mdpi.com/2077-0472/14/6/794  
- https://www.nature.com/articles/s44264-025-00052-6  

---

## 👤 Author
**Nishant Rajora**  
Undergraduate – Data Science  
The NorthCap University  

---

## ⭐ Acknowledgements
This project is developed as part of an academic evaluation and is inspired by recent research in machine learning and precision agriculture.