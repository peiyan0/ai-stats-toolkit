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

@ai_assistant_views.route('/tutor/chat', methods=['POST'])
def tutor_chat():
    data = request.json or {}
    message = data.get('message')
    test_name = data.get('test_name')
    results = data.get('results')
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
        
    response = consultant.chat_tutor(message, test_name, results)
    return jsonify({"response": response})

@ai_assistant_views.route('/apa_report', methods=['POST'])
def apa_report():
    data = request.json or {}
    test_name = data.get('test_name')
    data_summary = data.get('data_summary')
    results = data.get('results')
    
    if not test_name:
        return jsonify({"error": "Test name is required"}), 400
        
    report = consultant.get_apa_report(test_name, data_summary, results)
    return jsonify({"report": report})

@ai_assistant_views.route('/profile_dataset', methods=['POST'])
def profile_dataset():
    data = request.json or {}
    dataset_name = data.get('dataset_name', 'General Array')
    values = data.get('values')
    
    if not values or not isinstance(values, list):
        return jsonify({"error": "Dataset values are required and must be a list"}), 400
        
    profile = consultant.profile_dataset(dataset_name, values)
    return jsonify({"profile": profile})
