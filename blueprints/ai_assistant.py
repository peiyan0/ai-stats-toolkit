from flask import Blueprint, request, jsonify, render_template
import json
from stats_logic.ai_consultant import AIConsultant

ai_assistant_views = Blueprint("ai_assistant", __name__)
consultant = AIConsultant()

@ai_assistant_views.route('/wizard', methods=['GET'])
def wizard():
    return render_template('wizard.html')

@ai_assistant_views.route('/interpret', methods=['POST'])
def interpret():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    test_name = data.get('test_name')
    data_summary = data.get('data_summary')
    results = data.get('results')
    
    # Instantly interpret using robust rule-based logic
    interpretation = consultant.interpret_results(test_name, data_summary, results)
        
    return jsonify({"interpretation": interpretation})
