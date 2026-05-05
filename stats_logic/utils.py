import json
from datetime import datetime
from flask import session
import numpy as np

class StatEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        if isinstance(obj, (np.bool_)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return super(StatEncoder, self).default(obj)

def sanitize_data(data):
    """
    Recursively converts numpy types to standard Python types for JSON serialization.
    """
    if isinstance(data, dict):
        return {k: sanitize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_data(x) for x in data]
    elif isinstance(data, (np.integer, np.floating)):
        return float(data)
    elif isinstance(data, (np.bool_, bool)):
        return bool(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    else:
        return data

# add new entry to history
def add_to_history(calculation_type, input_data, result_data):
    try:
        # Sanitize everything before it touches the session or templates
        serializable_result = sanitize_data(result_data)
        serializable_input = sanitize_data(input_data)
        
        history_entry = {
            'type': calculation_type,
            'input_data': serializable_input,
            'result_data': serializable_result,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if 'history' not in session:
            session['history'] = []
            
        session['history'].insert(0, history_entry)
        session['history'] = session['history'][:50]
        session.modified = True 
    except Exception as e:
        print(f"History logging failed: {str(e)}")
