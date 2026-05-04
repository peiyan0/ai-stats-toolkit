from flask import Blueprint, request, render_template
import sqlite3

from stats_logic.descriptive import get_full_analysis
from stats_logic.utils import add_to_history
from stats_logic.sample_datasets import get_descriptive_samples

descriptive_views = Blueprint("descriptive", __name__)

@descriptive_views.route('/descriptive', methods=['GET','POST'])
def descriptive_stats(): 
    desc_samples = get_descriptive_samples()
    if request.method == 'POST':
        data_input = request.form.get('data')
        try:
            data = [float(x.strip()) for x in data_input.split(',') if x.strip()]
            if not data:
                raise ValueError("Empty input")
                
            result = get_full_analysis(data)
            
            add_to_history('Descriptive Statistics', data, result)
            return render_template('calculations/descriptive.html', 
                                 result=result, 
                                 samples=desc_samples,
                                 input_data=data_input)
        except Exception:
            error = "Invalid input. Please enter numbers separated by commas (e.g., 10, 20, 30)."
            return render_template('calculations/descriptive.html', 
                                 error=error,
                                 samples=desc_samples,
                                 input_data=data_input)
    
    return render_template('calculations/descriptive.html', samples=desc_samples, input_data=request.args.get('data', ''))
