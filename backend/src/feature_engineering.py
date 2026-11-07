import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def execute_pipeline(input_csv, model_dir):
    df = pd.read_csv(input_csv)
    
    X = df.drop(columns=['price'])
    y = df['price']
    
    # Split data to prevent data leakage
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    # NEW FIX: Only keep categorical columns with fewer than 50 unique values
    all_cat_cols = X_train.select_dtypes(include=['object']).columns.tolist()
    cat_cols = [col for col in all_cat_cols if X_train[col].nunique() < 50]
    
    # Drop the high-cardinality text columns to save memory
    cols_to_drop = [col for col in all_cat_cols if col not in cat_cols]
    X_train = X_train.drop(columns=cols_to_drop)
    X_test = X_test.drop(columns=cols_to_drop)
    
    preprocessor = ColumnTransformer(transformers=[
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols)
    ])
    
    # Fit strictly on training data, transform both
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    os.makedirs(model_dir, exist_ok=True)
    
    joblib.dump(preprocessor, f'{model_dir}/preprocessor.joblib')
    joblib.dump((X_train_processed, X_test_processed, y_train, y_test), f'{model_dir}/train_test_data.joblib')
    
    print(f"Feature engineering complete. Artifacts saved to {model_dir}/")
    

if __name__ == "__main__":
        execute_pipeline('data/processed.csv', 'models')