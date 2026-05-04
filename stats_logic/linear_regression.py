import math

def linear_regression(x, y): 
    """
    Performs Linear Regression with diagnostic metrics.
    """
    n = len(x)
    if n < 2: return {"error": "At least two data points required."}
    
    x_min = min(x)
    x_max = max(x)
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    
    x2_sum = sum(i ** 2 for i in x)
    y2_sum = sum(i ** 2 for i in y)
    xy_sum = sum(i * j for i,j in zip(x,y))

    SSxx = x2_sum - (sum(x) ** 2) / n
    SSxy = xy_sum - (sum(x) * sum(y)) / n
    SSyy = y2_sum - (sum(y) ** 2) / n

    if SSxx == 0: return {"error": "Independent variable has zero variance."}
    
    b = SSxy / SSxx
    a = y_mean - b * x_mean
    
    # Predicted Y values
    y_pred = [a + b * val for val in x]
    # Residuals
    residuals = [y_val - p_val for y_val, p_val in zip(y, y_pred)]
    # Residual Sum of Squares
    RSS = sum(r**2 for r in residuals)
    # Mean Squared Error
    MSE = RSS / (n - 2) if n > 2 else 0
    # Standard Error of Estimate
    SEE = math.sqrt(MSE)
    
    # R-squared and Correlation
    if SSyy == 0:
        r2 = 1.0
        r = 1.0
    else:
        r2 = (b * SSxy) / SSyy
        r = SSxy / (math.sqrt(SSxx) * math.sqrt(SSyy)) if (SSxx * SSyy) > 0 else 0
    
    return {
        "equation": f"y = {a:.4f} + {b:.4f}x",
        "r_squared": round(r2, 4),
        "correlation": round(r, 4),
        "slope": round(b, 4),
        "intercept": round(a, 4),
        "x_range": [x_min, x_max],
        "std_error_est": round(SEE, 4),
        "rss": round(RSS, 4),
        "mse": round(MSE, 4),
        "n": n
    }
