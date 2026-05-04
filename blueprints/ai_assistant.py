from flask import Blueprint, request, jsonify, render_template
import json
from stats_logic.ai_consultant import AIConsultant
from functools import lru_cache

ai_assistant_views = Blueprint("ai_assistant", __name__)
consultant = AIConsultant()

@lru_cache(maxsize=100)
def cached_recommendation(goal, data_type, groups):
    return consultant.get_test_recommendation(goal, data_type, groups)

@lru_cache(maxsize=200)
def cached_interpretation(test_name, data_summary, results_json):
    # results_json is used as a hashable key
    results = json.loads(results_json)
    return consultant.interpret_results(test_name, data_summary, results)

@ai_assistant_views.route('/wizard', methods=['GET', 'POST'])
def wizard():
    if request.method == 'POST':
        # Handle both Form and JSON for flexibility
        if request.is_json:
            data = request.json
            goal = data.get('goal')
            data_type = data.get('data_type')
            groups = data.get('groups')
        else:
            goal = request.form.get('goal')
            data_type = request.form.get('data_type')
            groups = request.form.get('groups')
        
        # Check if AI is actually available
        if not consultant.is_available():
            recommendation = "Notice: The AI reasoning engine is currently offline. Please ensure Ollama is running with the correct model."
        else:
            recommendation = cached_recommendation(goal, data_type, groups)
        
        if request.is_json:
            return jsonify({"recommendation": recommendation})
            
        return render_template('wizard.html', recommendation=recommendation, submitted=True)
    
    return render_template('wizard.html')

@ai_assistant_views.route('/interpret', methods=['POST'])
def interpret():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    test_name = data.get('test_name')
    data_summary = data.get('data_summary')
    results = data.get('results')
    
    if not consultant.is_available():
        # Fallback to rule-based directly if possible, or return a neutral message
        interpretation = consultant.rule_based_fallback(test_name, results)
    else:
        # Use JSON string for results to make it hashable for lru_cache
        results_json = json.dumps(results, sort_keys=True)
        interpretation = cached_interpretation(test_name, data_summary, results_json)
        
    return jsonify({"interpretation": interpretation})
