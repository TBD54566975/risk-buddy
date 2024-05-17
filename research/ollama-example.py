from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Path to the directory containing the rule files
RULES_DIR = './rules'

# Default model
DEFAULT_MODEL = 'phi3'

# Load rules from disk
def load_rules():
    rules = []
    for filename in os.listdir(RULES_DIR):
        if filename.endswith('.txt'):
            with open(os.path.join(RULES_DIR, filename), 'r') as file:
                rules.append(file.read().strip())
    return rules

# Format the prompt for the Ollama API
def format_prompt(data, rules):
    rules_text = '\n'.join(rules)
    prompt = f"Rules:\n{rules_text}\n\nData:\n{data}\n\nEvaluate the data based on the rules and return a score (high, medium, low):"
    return prompt

# Call the Ollama API to score the data
def score_data(model, prompt):
    response = requests.post('http://localhost:11434/api/generate', json={
        'model': model,
        'prompt': prompt,
        'stream': False,
        'format': 'json'
    })
    response_data = response.json()
    return response_data['response'].strip()

@app.route('/api/score', methods=['POST'])
def score():
    try:
        data = request.json.get('data')
        model = request.json.get('model', DEFAULT_MODEL)
        
        # Load rules
        rules = load_rules()
        
        # Format the prompt
        prompt = format_prompt(data, rules)
        
        # Get the score from Ollama API
        score = score_data(model, prompt)
        
        return jsonify({'score': score})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8080)
