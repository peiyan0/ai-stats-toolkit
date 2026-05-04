from flask import Blueprint, request, render_template
from stats_logic.probability import normal_distribution_analysis
from stats_logic.utils import add_to_history

probability_views = Blueprint("probability", __name__)

@probability_views.route('/normal', methods=['GET', 'POST'])
def normal_dist():
    if request.method == 'POST':
        try:
            x = float(request.form.get('x'))
            mu = float(request.form.get('mu'))
            sigma = float(request.form.get('sigma'))
            
            if sigma <= 0:
                return render_template('calculations/normal.html', error="Standard deviation must be positive.")
            
            result = normal_distribution_analysis(x, mu, sigma)
            
            add_to_history('Normal Distribution', 
                           {'x': x, 'mu': mu, 'sigma': sigma}, 
                           result)
            
            return render_template('calculations/normal.html', 
                                 result=result, 
                                 x=x, mu=mu, sigma=sigma)
        except (ValueError, TypeError):
            return render_template('calculations/normal.html', error="Invalid numeric input.")
            
    return render_template('calculations/normal.html')
