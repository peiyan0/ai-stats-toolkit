# File: blueprints/anova.py
from flask import Blueprint, request, render_template
import sqlite3

from stats_logic.anova import anova
from stats_logic.utils import add_to_history
from stats_logic.sample_datasets import get_anova_samples

anova_views = Blueprint("anova", __name__)

@anova_views.route('/anova', methods=['GET','POST'])
def anova_calc():
    anova_samples = get_anova_samples()
    if request.method == 'POST':
        groups_input = request.form.get('anova_data') # Updated field name to match my previous UI change
        try:
            # Process input in format: group1:1,2,3;group2:4,5,6
            groups = {}
            for group_str in groups_input.split(';'):
                if ':' in group_str:
                    group_name, group_data = group_str.split(':', 1)
                    groups[group_name.strip()] = [float(x.strip()) for x in group_data.split(',')]
            
            if len(groups) < 2:
                error = "ANOVA requires at least 2 groups"
                return render_template('calculations/anova.html',
                                    error=error,
                                    samples=anova_samples)
            
            from stats_logic.utils import sanitize_data
            arrays = list(groups.values())
            result = sanitize_data(anova(arrays))
            
            add_to_history('ANOVA', groups, result)
            return render_template('calculations/anova.html',
                                result=result,
                                groups=groups,
                                samples=anova_samples,
                                input_data=groups_input)
        except Exception as e:
            error = f"Invalid input format. Please use format: 'group1:1,2,3;group2:4,5,6'. Error: {str(e)}"
            return render_template('calculations/anova.html',
                                 error=error,
                                 samples=anova_samples)
    
    return render_template('calculations/anova.html', samples=anova_samples)
