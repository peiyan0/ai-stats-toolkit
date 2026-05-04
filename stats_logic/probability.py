import math

def normal_pdf(x, mu=0, sigma=1):
    """Calculates the probability density function for a normal distribution."""
    if sigma <= 0: return 0
    exponent = math.exp(-((x - mu)**2) / (2 * sigma**2))
    return (1 / (sigma * math.sqrt(2 * math.pi))) * exponent

def normal_cdf(x, mu=0, sigma=1):
    """Calculates the cumulative distribution function for a normal distribution."""
    if sigma <= 0: return 0
    return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))

def get_z_score(x, mu, sigma):
    if sigma <= 0: return 0
    return (x - mu) / sigma

def get_p_value(z, tail='two'):
    """Calculates p-value from z-score."""
    p_one_tail = 1 - normal_cdf(abs(z))
    if tail == 'two':
        return p_one_tail * 2
    return p_one_tail

def normal_distribution_analysis(x, mu, sigma):
    """
    Returns full analysis for a value in a normal distribution.
    """
    z = get_z_score(x, mu, sigma)
    p_two_tail = get_p_value(z, 'two')
    p_left = normal_cdf(x, mu, sigma)
    p_right = 1 - p_left
    
    return {
        "z_score": round(z, 4),
        "p_two_tail": round(p_two_tail, 4),
        "p_left_tail": round(p_left, 4),
        "p_right_tail": round(p_right, 4),
        "pdf_value": round(normal_pdf(x, mu, sigma), 4)
    }
