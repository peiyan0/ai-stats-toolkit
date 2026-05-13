from collections import Counter
import math

def mean(data):
    if not data: return 0
    return sum(data) / len(data)

def harmonic_mean(data):
    if not data or any(x <= 0 for x in data): return 0
    return len(data) / sum(1.0 / x for x in data)

def geometric_mean(data):
    """
    Numerically stable Geometric Mean.
    Uses log sum exp to prevent arithmetic overflow for large datasets.
    """
    if not data or any(x <= 0 for x in data): return 0
    try:
        log_sum = sum(math.log(x) for x in data)
        return math.exp(log_sum / len(data))
    except (ValueError, OverflowError):
        return 0

def median(data):
    if not data: return 0
    sortedData = sorted(data)
    middle = len(data) // 2
    if len(data) % 2 == 0:
        return (sortedData[middle - 1] + sortedData[middle]) / 2.0
    else:
        return sortedData[middle]

def mode(data):
    if not data: return []
    count = Counter(data)
    maxCount = max(count.values())
    modes = [key for key, value in count.items() if value == maxCount]
    return modes

def get_range(data):
    if not data: return 0
    return max(data) - min(data)

def variance(data, is_sample=True, mean_val=None):
    if not data or len(data) < 2: return 0
    m = mean_val if mean_val is not None else mean(data)
    denominator = len(data) - 1 if is_sample else len(data)
    return sum((x - m) ** 2 for x in data) / denominator

def std_dev(data, is_sample=True, mean_val=None):
    return variance(data, is_sample, mean_val) ** 0.5

def coefficient_of_variation(data, mean_val=None, std_val=None):
    m = mean_val if mean_val is not None else mean(data)
    if m == 0: return 0
    s = std_val if std_val is not None else std_dev(data)
    return (s / m) * 100

def standard_error(data, std_val=None):
    if not data: return 0
    s = std_val if std_val is not None else std_dev(data)
    return s / (len(data) ** 0.5)

def get_skewness(data, mean_val=None, std_val=None):
    """Calculates Sample Skewness (Adjusted Fisher-Pearson) with caching support."""
    n = len(data)
    if n < 3: return 0
    m = mean_val if mean_val is not None else mean(data)
    s = std_val if std_val is not None else std_dev(data, mean_val=m)
    if s == 0: return 0
    
    m3 = sum((x - m) ** 3 for x in data) / n
    # Bias correction for sample skewness
    return (math.sqrt(n * (n - 1)) / (n - 2)) * (m3 / (s ** 3))

def get_kurtosis(data, mean_val=None, std_val=None):
    """Calculates Sample Excess Kurtosis with caching support."""
    n = len(data)
    if n < 4: return 0
    m = mean_val if mean_val is not None else mean(data)
    s = std_val if std_val is not None else std_dev(data, mean_val=m)
    if s == 0: return 0
    
    m4 = sum((x - m) ** 4 for x in data) / n
    # Bias correction for sample kurtosis
    pre_factor = (n - 1) / ((n - 2) * (n - 3))
    term1 = (n + 1) * (m4 / (s ** 4))
    term2 = 3 * (n - 1)
    return pre_factor * (term1 - term2)

def get_quartiles_and_outliers(data, sorted_data=None):
    if not data: return {"q1": 0, "q2": 0, "q3": 0, "iqr": 0, "outliers": []}
    sortedList = sorted_data if sorted_data is not None else sorted(data)
    n = len(sortedList)
    
    # Standard quantile index mapping
    q1 = sortedList[int(n * 0.25)]
    q2 = median(sortedList)
    q3 = sortedList[int(n * 0.75)]
    iqr = q3 - q1
    
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    outliers = [i for i in data if i < lower_bound or i > upper_bound]
    
    return {
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "iqr": iqr,
        "outliers": outliers
    }

def get_full_analysis(data):
    if not data: return {}
    
    # Pre-calculate (cache) core statistics so helpers don't run redundant loops
    n = len(data)
    sorted_data = sorted(data)
    mean_val = mean(data)
    std_val = std_dev(data, is_sample=True, mean_val=mean_val)
    
    return {
        "mean": round(mean_val, 4),
        "median": round(median(data), 4),
        "mode": mode(data),
        "harmonic_mean": round(harmonic_mean(data), 4),
        "geometric_mean": round(geometric_mean(data), 4),
        "range": round(get_range(data), 4),
        "variance": round(variance(data, is_sample=True, mean_val=mean_val), 4),
        "std_dev": round(std_val, 4),
        "cv": round(coefficient_of_variation(data, mean_val=mean_val, std_val=std_val), 2),
        "std_error": round(standard_error(data, std_val=std_val), 4),
        "skewness": round(get_skewness(data, mean_val=mean_val, std_val=std_val), 4),
        "kurtosis": round(get_kurtosis(data, mean_val=mean_val, std_val=std_val), 4),
        "quartiles": get_quartiles_and_outliers(data, sorted_data=sorted_data),
        "n": n
    }
