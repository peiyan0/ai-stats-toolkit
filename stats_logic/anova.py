from scipy import stats

def anova(arrays):
    """
    Performs One-Way ANOVA with effect size and assumption checking.
    """
    k = len(arrays)
    n = sum(len(array) for array in arrays)
    if n <= k: return {"error": "Sample size too small for ANOVA."}
    
    # Calculate ANOVA
    f_stat, p_val = stats.f_oneway(*arrays)
    
    # Assumption Check (Levene's)
    levene_p = stats.levene(*arrays).pvalue
    
    grand_mean = sum(sum(array) for array in arrays) / n

    df_between = k - 1
    df_within = n - k
    
    SSB = sum(len(array) * (sum(array) / len(array) - grand_mean) ** 2 for array in arrays)
    SSW = sum(sum((x - sum(array) / len(array)) ** 2 for x in array) for array in arrays)
    SST = SSB + SSW
    
    MSB = SSB / df_between
    MSW = SSW / df_within
    
    # Effect Size
    eta_sq = SSB / SST
    omega_sq = (SSB - df_between * MSW) / (SST + MSW)
    
    return {
        "k": k,
        "n": n,
        "p_value": round(p_val, 4),
        "f_test": round(f_stat, 4),
        "levene_p": round(levene_p, 4),
        "grand_mean": round(grand_mean, 4),
        "SSB": round(SSB, 4),
        "SSW": round(SSW, 4),
        "SST": round(SST, 4),
        "MSB": round(MSB, 4),
        "MSW": round(MSW, 4),
        "df_between": df_between,
        "df_within": df_within,
        "eta_squared": round(eta_sq, 4),
        "omega_squared": round(max(0, omega_sq), 4)
    }
