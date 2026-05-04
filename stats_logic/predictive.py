import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def train_predictive_model(y, features, model_type='linear'):
    """
    Trains a machine learning model using scikit-learn and returns predictive metrics.
    features: list of lists (each sublist is a feature column)
    """
    try:
        # Convert to numpy arrays
        Y = np.array(y)
        X = np.array(features).T # Transpose to get (n_samples, n_features)
        
        if len(Y) < 5:
            return {"error": "Insufficient data for predictive modeling. Minimum 5 samples required."}

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        if model_type == 'linear':
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            
            # Metrics
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)
            
            # Cross-validation (R2)
            cv_scores = cross_val_score(model, X, Y, cv=min(5, len(Y)//2))
            
            return {
                "type": "Regression",
                "mae": round(mae, 4),
                "mse": round(mse, 4),
                "rmse": round(rmse, 4),
                "r2": round(r2, 4),
                "cv_mean": round(cv_scores.mean(), 4),
                "cv_std": round(cv_scores.std(), 4),
                "coefficients": model.coef_.tolist(),
                "intercept": float(model.intercept_)
            }
            
        elif model_type == 'logistic':
            # Ensure Y is categorical/integer
            if not np.all(np.equal(np.mod(Y, 1), 0)):
                return {"error": "Logistic regression requires discrete/categorical target labels (integers)."}
                
            model = LogisticRegression(max_iter=1000)
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            
            # Metrics
            acc = accuracy_score(y_test, y_pred)
            # Use macro average for multi-class support if needed
            prec = precision_score(y_test, y_pred, average='macro', zero_division=0)
            rec = recall_score(y_test, y_pred, average='macro', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)
            
            return {
                "type": "Classification",
                "accuracy": round(acc, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "f1_score": round(f1, 4),
                "classes": np.unique(Y).tolist()
            }
            
        else:
            return {"error": "Unknown model type requested."}
            
    except Exception as e:
        return {"error": f"ML Processing Error: {str(e)}"}
