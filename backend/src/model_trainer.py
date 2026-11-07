import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

def train_and_evaluate(model_dir):
    # 1. Load the engineered data
    X_train, X_test, y_train, y_test = joblib.load(f'{model_dir}/train_test_data.joblib')
    
    # 2. Define models to compare (using n_jobs=-1 to use all CPU cores)
    models = {
        'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=15, min_samples_leaf=5, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    
    results = []
    best_r2 = -float('inf')
    best_model_name = ""
    best_model = None
    
    # 3. Train and evaluate each model
    print("Training models... This might take a minute.")
    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        
        r2 = r2_score(y_test, predictions)
        rmse = mean_squared_error(y_test, predictions) ** 0.5
        
        results.append({'Model': name, 'R2 Score': round(r2, 4), 'RMSE': round(rmse, 2)})
        
        # Track the best performing model
        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_model = model
            
    # 4. Display the comparison table
    results_df = pd.DataFrame(results)
    print("\n--- Model Comparison Results ---")
    print(results_df.to_string(index=False))
    
    # 5. Export the winning model
    joblib.dump(best_model, f'{model_dir}/best_model.joblib')
    print(f"\nWinning model ({best_model_name}) saved to {model_dir}/best_model.joblib")
if __name__ == "__main__":
    train_and_evaluate('models')