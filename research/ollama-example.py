from flask import Flask, request, jsonify
import os
import requests
import json

app = Flask(__name__)

# Path to the directory containing the rule files
RULES_DIR = './rules'

# Default model - use the Modelfile with content: `FROM ./phi-3-mini-128k-instruct.Q8_0.gguf`
DEFAULT_MODEL = 'phi3-128k-instruct'

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
    prompt = (
        f"Rules:\n"
        f"{rules_text}\n\n"
        f"Data:\n"
        f"{json.dumps(data, indent=2)}\n\n"
        f"Instructions:\n"
        f"Based on the rules provided, evaluate the data against the rules and return:\n"
        f"a score: one of 'high', 'medium', or 'low'\n"
        f"a justification: a short explanation of why it was scored that way.\n\n"
    )
    return prompt

# Call the Ollama API to score the data
def score_data(model, prompt):
    print(prompt)
    response = requests.post('http://localhost:11434/api/generate', json={
        'model': model,
        'prompt': prompt,
        'stream': False, 
        'temperature': 0.0,
    })
    response_data = response.json()
    print(response_data)
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
        
        return jsonify(score)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8080)
