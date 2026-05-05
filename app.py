from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from dotenv import load_dotenv
import os
import sqlite3 
import json

from blueprints.anova import anova_views
from blueprints.confidence import confidence_views
from blueprints.descriptive import descriptive_views
from blueprints.linear import linear_views
from blueprints.ai_assistant import ai_assistant_views
from blueprints.probability import probability_views
from blueprints.t_test import t_test_views
from blueprints.predictive import predictive_views
from blueprints.export import export_views

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

app.register_blueprint(anova_views, url_prefix='/calculations')
app.register_blueprint(confidence_views, url_prefix='/calculations')
app.register_blueprint(descriptive_views, url_prefix='/calculations')
app.register_blueprint(linear_views, url_prefix='/calculations')
app.register_blueprint(probability_views, url_prefix='/calculations')
app.register_blueprint(t_test_views, url_prefix='/calculations')
app.register_blueprint(predictive_views, url_prefix='/calculations')
app.register_blueprint(export_views, url_prefix='/ai')
app.register_blueprint(ai_assistant_views, url_prefix='/ai')

# initialize history
@app.before_request
def before_request(): 
    if 'history' not in session:
        session['history'] = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calculations')
def calculations():
    return render_template('calculations.html')

@app.route('/datasets')
def datasets():
    conn = sqlite3.connect('dataset/dataset.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dataset")
    datasets = cursor.fetchall()
    cursor.execute("SELECT * FROM two_pops")
    two_pops = cursor.fetchall()
    conn.close()
    return render_template('datasets.html',
        datasets=datasets,
        two_pops=two_pops
    )           

@app.route('/how_to_use')
def how_to_use():
    return render_template('how_to_use.html')

@app.route('/history')
def history():
    return render_template('history.html', history=session.get('history',[]))

if __name__ == '__main__':
    app.run(debug=True)