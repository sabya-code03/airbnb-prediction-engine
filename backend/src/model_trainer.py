import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
import joblib

print("Loading data...")
df = pd.read_csv('backend/data/processed.csv')

X_full = df.drop(columns=['price'])
y = df['price']

# 1. FILTER FEATURES: Drop stray dates and text
categorical_features = ['room_type', 'city', 'host_is_superhost', 'host_has_profile_pic', 'host_identity_verified', 'instant_bookable']
numeric_features = X_full.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Isolate only the features we need, discarding everything else
X = X_full[numeric_features + categorical_features]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Applying log transformation...")
y_train_log = np.log1p(y_train)
y_test_log = np.log1p(y_test)

# 2. THE PREPROCESSOR: Route data types safely
preprocessor = ColumnTransformer(
    transformers=[
        ('num', SimpleImputer(strategy='median', add_indicator=True), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# 3. THE PIPELINE
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', RandomForestRegressor(random_state=42, n_jobs=1))
])

# 4. HYPERPARAMETER TUNING
param_distributions = {
    'model__n_estimators': [100, 200],
    'model__max_depth': [10, 15, 20],
    'model__min_samples_leaf': [2, 5, 10]
}

print("Tuning hyperparameters (this might take a minute)...")
search = RandomizedSearchCV(
    pipeline, 
    param_distributions=param_distributions, 
    n_iter=2,
    cv=3, 
    scoring='neg_mean_absolute_error',
    random_state=42,
    verbose=3  # <-- Add this line!
)
search.fit(X_train, y_train_log)
best_model = search.best_estimator_

# 5. BASELINE COMPARISON
dummy = DummyRegressor(strategy='median')
dummy.fit(X_train, y_train_log)

# 6. EVALUATION
print("Evaluating model...")
y_pred_log = best_model.predict(X_test)
y_pred = np.expm1(y_pred_log) 
y_baseline = np.expm1(dummy.predict(X_test))

print("\n--- Evaluation Metrics ---")
print(f"Baseline MAE (Predicting Median): {mean_absolute_error(y_test, y_baseline):.2f}")
print(f"Random Forest MAE: {mean_absolute_error(y_test, y_pred):.2f}")
print(f"Model RMSE: {root_mean_squared_error(y_test, y_pred):.2f}")
print(f"Model R²: {r2_score(y_test, y_pred):.4f}")

print("\nSaving optimized model...")
joblib.dump(best_model, 'backend/models/best_model.joblib')
print("Done! Ready for deployment.")