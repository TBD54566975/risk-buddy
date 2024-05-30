from flask import Flask, request, jsonify
import os
import requests
import json
import subprocess
import signal
import time
import embedding

app = Flask(__name__)

# Constants
RULES_DIR = './rules'
LLAMAFILE_PORT = 9090
LLAMAFILE_NAME = "llamafile"
#LLAMAFILE_MODEL = "Meta-Llama-3-8B.Q8_0.gguf"
LLAMAFILE_MODEL = "Phi-3-medium-128k-instruct-Q5_K_M.gguf"

# Utility functions
def load_rules():
    rules = []
    for filename in os.listdir(RULES_DIR):
        if filename.endswith('.txt'):
            with open(os.path.join(RULES_DIR, filename), 'r') as file:
                rules.append(file.read().strip())
    return rules

def json_to_human_readable(data, indent=0):
    human_readable = []
    indent_str = '  ' * indent
    if isinstance(data, dict):
        for key, value in data.items():
            if "id" in key.lower() or "hash" in key.lower():
                continue
            if isinstance(value, (dict, list)):
                human_readable.append(f"{indent_str}{key}:")
                human_readable.append(json_to_human_readable(value, indent + 1))
            else:
                human_readable.append(f"{indent_str}{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            human_readable.append(json_to_human_readable(item, indent))
    else:
        human_readable.append(f"{indent_str}{data}")
    return '\n'.join(human_readable)

def format_evaluation_prompt(human_readable_data, rules):
    rules_text = '\n'.join(rules)
    prompt = (
        f"Evaluate the following transactional data based on the provided rules and determine the risk level (high, medium, or low). Do not provide a justification at this stage.\n\n"
        f"### Rules:\n{rules_text}\n\n"
        f"### Transactional Data:\n{human_readable_data}\n\n"
        f"### Task:\nBased on the rules provided, evaluate the data and return the risk level as a single string: 'high', 'medium', or 'low'."
    )
    return prompt

def format_justification_prompt(human_readable_data, rules, risk_level):
    rules_text = '\n'.join(rules)
    prompt = (
        f"The following transaction has been flagged as '{risk_level}' risk. Please provide a justification for this risk level based on the rules provided.\n\n"
        f"### Rules:\n{rules_text}\n\n"
        f"### Transactional Data:\n{human_readable_data}\n\n"
        f"### Task:\nProvide a brief explanation as to why the transaction is considered '{risk_level}' risk based on the rules and data."
    )
    return prompt

def call_llm(prompt):
    print("\n\n\n\n\n\n\nPROMPT\n\n\n\n" + prompt + "\n\n\n\n\n\n\nEND PROMPT\n\n\n\n\n")

    response = requests.post(f'http://localhost:{LLAMAFILE_PORT}/completion', json={
        'prompt': prompt,
        'n_predict': 100,
        'temperature': 0.0,
        'top_p': 0.9,
        'min_p': 0.4,
        'top_k': 50,
    })
    response_data = response.json()
    response_text = response_data['content'].strip()
    print("LLM Response:", response_text)
    return response_text

def extract_json_from_response(response_text):
    start = response_text.find('{')
    end = response_text.rfind('}') + 1
    if start != -1 and end != -1:
        json_response = response_text[start:end]
    else:
        json_response = '{}'
    return json_response

def clean_json(json_string):
    try:
        cleaned_data = json.loads(json_string)
        return json.dumps(cleaned_data, indent=2)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        return json_string

def run_llamafile():
    if not os.path.exists(LLAMAFILE_NAME):
        raise FileNotFoundError(f'{LLAMAFILE_NAME} does not exist.')

    command = f'./{LLAMAFILE_NAME} -m {LLAMAFILE_MODEL} --port {LLAMAFILE_PORT}'
    print(f'Running {command}...')
    
    llamafile_process = subprocess.Popen(command, 
                                         shell=True, 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE)
    time.sleep(5)  # Wait for a few seconds to let the server start
    return llamafile_process

@app.route('/api/score', methods=['POST'])
def score():
    try:
        data = request.json.get('data')
        data_s = json.dumps(data)
        
        similar_transactions = embedding.search(data_s, n_results=3, min_score=0.95)
        if similar_transactions:
            print("Nearby transaction(s) found.")            
        
        embedding.add_document(data_s)
        
        rules = load_rules()
        
        # Convert JSON data to human-readable format
        human_readable_data = json_to_human_readable(data)
        print("Human-readable Data:\n", human_readable_data)
        
        # Step 1: Determine the risk level
        evaluation_prompt = format_evaluation_prompt(human_readable_data, rules)
        risk_response = call_llm(evaluation_prompt).strip()
        
        if risk_response in ["high", "medium"]:
            # Step 2: Request justification for flagged transactions
            justification_prompt = format_justification_prompt(human_readable_data, rules, risk_response)
            justification_response = call_llm(justification_prompt).strip()
            result = {
                "score": risk_response,
                "justification": justification_response
            }
        else:
            result = {
                "score": "low",
                "justification": "None needed for low risk transactions."
            }
        
        return jsonify(result)
        
    except Exception as e:
        error_message = str(e)
        print("Error:", error_message)
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    llamafile_process = run_llamafile()
    try:
        app.run(port=8080)
    finally:
        llamafile_process.send_signal(signal.SIGINT)
        llamafile_process.wait()
