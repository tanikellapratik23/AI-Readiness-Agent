import os
from flask import Flask, render_template, request, jsonify
from framework import STAKEHOLDER_ROLES, QUESTIONS
from assessment import calculate_scores, summarize_recommendations
from agent import chatbot_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', roles=STAKEHOLDER_ROLES, questions=QUESTIONS)

@app.route('/assess', methods=['POST'])
def assess():
    role = request.form.get('role')
    answers = {}
    for q in QUESTIONS:
        key = f"q_{q['id']}"
        val = request.form.get(key)
        if val and val in q['choices']:
            answers[q['id']] = val
    scores = calculate_scores(answers)
    recommendations = summarize_recommendations(scores)
    return render_template('results.html', role=role, scores=scores, recommendations=recommendations)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '')
    role = data.get('role', '')
    scores = data.get('scores', {})
    response = chatbot_response(message, role, scores)
    return jsonify({'response': response})

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host=host, port=port, debug=debug)
