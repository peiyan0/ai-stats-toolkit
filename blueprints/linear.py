from flask import Blueprint, request, render_template
import sqlite3

from stats_logic.linear_regression import linear_regression
from stats_logic.utils import add_to_history
from stats_logic.sample_datasets import get_linear_samples

linear_views = Blueprint("linear", __name__)

@linear_views.route('/linear', methods=['GET','POST'])
def linear_regression_calc():
    linear_samples = get_linear_samples()
    if request.method == 'POST':
        x_input = request.form.get('x_data')
        y_input = request.form.get('y_data')
        try:
            x_data = [float(x.strip()) for x in x_input.split(',') if x.strip()]
            y_data = [float(y.strip()) for y in y_input.split(',') if y.strip()]
            
            if len(x_data) != len(y_data):
                error = "X and Y data must have the same number of values."
                return render_template('calculations/linear.html', error=error, samples=linear_samples, x_data=x_input, y_data=y_input)
            
            if not x_data:
                raise ValueError("Empty input")
            
            result = linear_regression(x_data, y_data)
            
            if "error" in result:
                return render_template('calculations/linear.html', error=result["error"], samples=linear_samples, x_data=x_input, y_data=y_input)

            add_to_history('Linear Regression', {'x': x_data, 'y': y_data}, result)
            
            return render_template('calculations/linear.html',
                                 result=result,
                                 samples=linear_samples,
                                 x_data=x_input,
                                 y_data=y_input)
        except Exception:
            error = "Invalid input. Please enter numbers separated by commas (e.g., 1, 2, 3)."
            return render_template('calculations/linear.html', error=error, samples=linear_samples, x_data=x_input, y_data=y_input)
    
    return render_template('calculations/linear.html', samples=linear_samples)
