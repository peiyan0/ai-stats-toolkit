import math
from scipy import stats
from stats_logic.descriptive import mean, std_dev

def one_sample_t_test(data, pop_mean):
    """
    Calculates the t-statistic and p-value for a one-sample t-test.
    """
    n = len(data)
    if n < 2: return {"error": "Sample size too small (n < 2)."}
    
    x_bar = mean(data)
    s = std_dev(data)
    if s == 0: return {"error": "Standard deviation is zero."}
    
    t_stat = (x_bar - pop_mean) / (s / math.sqrt(n))
    df = n - 1
    p_val = stats.t.sf(abs(t_stat), df) * 2
    
    return {
        "t_stat": round(t_stat, 4),
        "p_value": round(p_val, 4),
        "df": df,
        "sample_mean": round(x_bar, 4),
        "pop_mean": pop_mean
    }

def two_sample_t_test(data1, data2, equal_var=True):
    """
    Calculates the t-statistic and p-value for a two-sample t-test.
    """
    n1, n2 = len(data1), len(data2)
    if n1 < 2 or n2 < 2: return {"error": "Sample sizes too small (min 2 per group)."}
    
    x1_bar, x2_bar = mean(data1), mean(data2)
    s1, s2 = std_dev(data1), std_dev(data2)
    
    if equal_var:
        df = n1 + n2 - 2
        pooled_var = ((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / df
        se = math.sqrt(pooled_var * (1/n1 + 1/n2))
    else:
        # Welch's T-test
        se1 = s1**2 / n1
        se2 = s2**2 / n2
        se = math.sqrt(se1 + se2)
        df = (se1 + se2)**2 / ((se1**2 / (n1 - 1)) + (se2**2 / (n2 - 1)))
    
    if se == 0: return {"error": "Standard error is zero."}
    
    t_stat = (x1_bar - x2_bar) / se
    p_val = stats.t.sf(abs(t_stat), df) * 2
    
    return {
        "t_stat": round(t_stat, 4),
        "p_value": round(p_val, 4),
        "df": round(df, 2),
        "mean1": round(x1_bar, 4),
        "mean2": round(x2_bar, 4),
        "mean_diff": round(x1_bar - x2_bar, 4),
        "se": round(se, 4)
    }
