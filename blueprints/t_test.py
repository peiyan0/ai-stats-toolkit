from flask import Blueprint, request, render_template
from stats_logic.hypothesis_testing import two_sample_t_test
from stats_logic.utils import add_to_history
from stats_logic.sample_datasets import get_anova_samples # Reusing group logic

t_test_views = Blueprint("t_test", __name__)

@t_test_views.route('/t-test', methods=['GET', 'POST'])
def t_test_calc():
    samples = get_anova_samples() # Can use same group format
    if request.method == 'POST':
        data_input = request.form.get('t_test_data')
        try:
            groups = {}
            for group_str in data_input.split(';'):
                if ':' in group_str:
                    name, vals = group_str.split(':', 1)
                    groups[name.strip()] = [float(x.strip()) for x in vals.split(',')]
            
            if len(groups) != 2:
                return render_template('calculations/t_test.html', 
                                    error="Two-sample T-test requires exactly 2 groups.",
                                    samples=samples)
            
            group_names = list(groups.keys())
            data1 = groups[group_names[0]]
            data2 = groups[group_names[1]]
            
            result = two_sample_t_test(data1, data2)
            
            add_to_history('T-test', groups, result)
            return render_template('calculations/t_test.html',
                                 result=result,
                                 groups=groups,
                                 group_names=group_names,
                                 samples=samples,
                                 input_data=data_input)
        except Exception as e:
            return render_template('calculations/t_test.html',
                                 error=f"Invalid format: {str(e)}",
                                 samples=samples)
            
    return render_template('calculations/t_test.html', samples=samples)
