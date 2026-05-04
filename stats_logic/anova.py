def anova(arrays):
    """
    Performs One-Way ANOVA with effect size calculations.
    """
    k = len(arrays)
    n = sum(len(array) for array in arrays)
    if n <= k: return {"error": "Sample size too small for ANOVA."}
    
    grand_mean = sum(sum(array) for array in arrays) / n

    df_between = k - 1
    df_within = n - k
    
    SSB = sum(len(array) * (sum(array) / len(array) - grand_mean) ** 2 for array in arrays)
    SSW = sum(sum((x - sum(array) / len(array)) ** 2 for x in array) for array in arrays)
    SST = SSB + SSW
    
    MSB = SSB / df_between
    MSW = SSW / df_within
    
    if MSW == 0: return {"error": "Within-group variance is zero."}
    
    F_test = MSB / MSW
    
    # Effect Size Calculations
    eta_sq = SSB / SST
    # Omega squared is a less biased estimate of effect size
    omega_sq = (SSB - df_between * MSW) / (SST + MSW)
    
    return {
        "k": k,
        "n": n,
        "grand_mean": round(grand_mean, 4),
        "SSB": round(SSB, 4),
        "SSW": round(SSW, 4),
        "SST": round(SST, 4),
        "MSB": round(MSB, 4),
        "MSW": round(MSW, 4),
        "F_test": round(F_test, 4),
        "df_between": df_between,
        "df_within": df_within,
        "eta_squared": round(eta_sq, 4),
        "omega_squared": round(max(0, omega_sq), 4) # Can be negative in small samples
    }
