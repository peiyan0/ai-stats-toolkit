from flask import Blueprint, session, Response
import io
import csv
import json

export_views = Blueprint("export", __name__)

@export_views.route('/export/history', methods=['GET'])
def export_history():
    """Exports the session history as a CSV file."""
    history = session.get('history', [])
    
    if not history:
        return "No history found to export", 404
        
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Timestamp', 'Calculation Type', 'Input Data', 'Results'])
    
    for entry in history:
        writer.writerow([
            entry.get('timestamp'),
            entry.get('type'),
            json.dumps(entry.get('input_data')),
            json.dumps(entry.get('result_data'))
        ])
        
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=stat_toolkit_history.csv"}
    )
