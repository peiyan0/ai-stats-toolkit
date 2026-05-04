# File: blueprints/confidence.py
from flask import Blueprint, request, render_template
import sqlite3

from stats_logic.confidence_intervals import two_pop_CI, dep_data, two_samp_prop
from stats_logic.utils import add_to_history
from stats_logic.sample_datasets import get_confidence_samples

confidence_views = Blueprint("confidence", __name__)

@confidence_views.route('/confidence', methods=['GET','POST'])
def confidence_intervals():
    calculation_type = request.args.get('type', 'two_pop')
    ci_samples = get_confidence_samples()
    
    if request.method == 'POST':
        if calculation_type == 'two_pop':
            try:
                n1 = float(request.form.get('n1'))
                x1 = float(request.form.get('x1'))
                s1 = float(request.form.get('s1'))
                n2 = float(request.form.get('n2'))
                x2 = float(request.form.get('x2'))
                s2 = float(request.form.get('s2'))
                t = float(request.form.get('t_value'))
                equal_var = request.form.get('equal_var') == 'true'
                
                args = [[n1, x1, s1], [n2, x2, s2], t, "equal" if equal_var else "unequal"]
                result = two_pop_CI(args)
                
                add_to_history('Two Population CI', 
                             {'n1': n1, 'x1': x1, 's1': s1,
                              'n2': n2, 'x2': x2, 's2': s2,
                              't': t, 'equal_variance': equal_var},
                              result)
                
                return render_template('calculations/confidence.html',
                                     result=result,
                                     calculation_type=calculation_type,
                                     samples=ci_samples)
            except ValueError:
                error = "Invalid input. Please enter numeric values."
                return render_template('calculations/confidence.html',
                                     error=error,
                                     calculation_type=calculation_type,
                                     samples=ci_samples)
        
        elif calculation_type == 'dep_data':
            try:
                before = [float(x.strip()) for x in request.form.get('before_data').split(',')]
                after = [float(x.strip()) for x in request.form.get('after_data').split(',')]
                
                if len(before) != len(after):
                    error = "Before and after data must have the same number of values"
                    return render_template('calculations/confidence.html',
                                         error=error,
                                         calculation_type=calculation_type,
                                         samples=ci_samples)
                
                result = dep_data([before, after])
                
                add_to_history('Dependent Data T-Test',
                             {'before': before, 'after': after},
                             result)
                
                return render_template('calculations/confidence.html',
                                     result=result,
                                     calculation_type=calculation_type,
                                     samples=ci_samples)
            except ValueError:
                error = "Invalid input. Please enter numbers separated by commas."
                return render_template('calculations/confidence.html',
                                     error=error,
                                     calculation_type=calculation_type,
                                     samples=ci_samples)
        
        elif calculation_type == 'two_samp_prop':
            try:
                n1 = float(request.form.get('n1'))
                p1 = float(request.form.get('p1'))
                n2 = float(request.form.get('n2'))
                p2 = float(request.form.get('p2'))
                
                result = two_samp_prop([[n1, p1], [n2, p2]])
                
                add_to_history('Two Sample Proportion',
                             {'n1': n1, 'p1': p1, 'n2': n2, 'p2': p2},
                             result)
                
                return render_template('calculations/confidence.html',
                                     result=result,
                                     calculation_type=calculation_type,
                                     samples=ci_samples)
            except ValueError:
                error = "Invalid input. Please enter numeric values."
                return render_template('calculations/confidence.html',
                                     error=error,
                                     calculation_type=calculation_type,
                                     samples=ci_samples)
    
    return render_template('calculations/confidence.html',
                         calculation_type=calculation_type,
                         samples=ci_samples,
                         pre_load={
                             'n1': request.args.get('n1', ''),
                             'x1': request.args.get('x1', ''),
                             's1': request.args.get('s1', ''),
                             'n2': request.args.get('n2', ''),
                             'x2': request.args.get('x2', ''),
                             's2': request.args.get('s2', ''),
                             't': request.args.get('t', ''),
                             'var': request.args.get('var', 'equal')
                         })
