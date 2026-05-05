from flask import Blueprint, request, render_template, jsonify
from stats_logic.predictive import train_predictive_model
from stats_logic.utils import add_to_history
from stats_logic.sample_datasets import get_predictive_samples

predictive_views = Blueprint("predictive", __name__)

@predictive_views.route('/predictive', methods=['GET', 'POST'])
def predictive_dashboard():
    samples = get_predictive_samples()
    if request.method == 'POST':
        data_input = request.form.get('ml_data')
        model_type = request.form.get('model_type', 'linear')
        
        try:
            # Parse input format: target:1,2,3;feature1:4,5,6;feature2:7,8,9
            raw_data = {}
            for segment in data_input.split(';'):
                if ':' in segment:
                    name, vals = segment.split(':', 1)
                    raw_data[name.strip()] = [float(x.strip()) for x in vals.split(',')]
            
            if len(raw_data) < 2:
                return render_template('calculations/predictive.html', 
                                    error="Predictive models require at least one target and one feature.",
                                    samples=samples)
            
            keys = list(raw_data.keys())
            target_name = keys[0]
            feature_names = keys[1:]
            
            y = raw_data[target_name]
            features = [raw_data[name] for name in feature_names]
            
            # Verify lengths
            n = len(y)
            for f in features:
                if len(f) != n:
                    return render_template('calculations/predictive.html', 
                                        error="All variables must have the same number of data points.",
                                        samples=samples)
            
            from stats_logic.utils import sanitize_data
            result = sanitize_data(train_predictive_model(y, features, model_type, feature_names=feature_names))
            
            if "error" in result:
                return render_template('calculations/predictive.html', error=result["error"])
            
            # Enrich result for UI
            result['target_name'] = target_name
            result['feature_names'] = feature_names
            
            add_to_history(f'ML {model_type.capitalize()}', raw_data, result)
            return render_template('calculations/predictive.html', 
                                 result=result, 
                                 input_data=data_input,
                                 model_type=model_type,
                                 samples=samples)
            
        except Exception as e:
            return render_template('calculations/predictive.html', 
                                 error=f"Invalid data format: {str(e)}",
                                 samples=samples)
            
    return render_template('calculations/predictive.html', samples=samples)
