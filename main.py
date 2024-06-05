from flask import Flask, request, jsonify
import os
import requests
import json
import subprocess
import signal
import time
import logging
import re

from tbdex import TBDEX_PROTOCOL_DESCRIPTION, TBDEX_JARGON

app = Flask(__name__)

# Constants
RULES_DIR = './rules'
LLAMAFILE_PORT = 9090
LLAMAFILE_NAME = "llamafile"
LLAMAFILE_MODEL = "phi-3-mini-128k-instruct.Q8_0.gguf"

# Configure logging
logging.basicConfig(level=logging.INFO)

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

def call_llm_for_rule_evaluation(human_readable_data, rule, rule_name):
    prompt = (
        f"{TBDEX_PROTOCOL_DESCRIPTION}\n\n"
        f"{TBDEX_JARGON}\n\n"
        f"Examples:\n"
        f"User: \nTransaction Data: Here is a transaction with an amount of 0.0001 BTC.\nRule: Transactions above 10 BTC.\nAssistant: \nno\n"
        f"User: \nTransaction Data: Here is a transaction with an amount of 15 BTC.\nRule: Transactions above 10 BTC.\nAssistant: \nyes\n"
        f"User: \nTransaction Data: Here is a transaction to an unknown account.\nRule: Transactions to unknown accounts.\nAssistant: \nyes\n"
        f"User: \nTransaction Data: Here is a transaction to a known account.\nRule: Transactions to unknown accounts.\nAssistant: \nno\n\n"
        f"These are examples of how to reply.\n\n"
        f"User: \nEvaluate the following transactional data against the rule and answer strictly with 'yes' or 'no'.\n\n"
        f"Transaction Data:\n{human_readable_data}\n\n"
        f"Rule: {rule}\n\n"
        f"User: \Based on the rule above, does the Transaction Data violate that rule? Answer 'yes' or 'no'.\nAssistant: "
    )

    logging.info(f"Testing rule: {rule_name}")
    logging.info(f"Calling LLM with prompt: {prompt}")

    response = requests.post(f'http://localhost:{LLAMAFILE_PORT}/completion', json={
        'prompt': prompt,
        'n_predict': 10,
        'temperature': 0.0,
        'top_p': 0.9,
        'min_p': 0.4,
        'top_k': 50,
        'stop': ["User:", "Assistant:"]
    })
    response_data = response.json()
    response_text = response_data['content'].strip().lower()

    logging.info(f"LLM response: {response_text}")

    # Check for simple 'yes' or 'no' in the response
    match = re.search(r'\b(yes|no)\b', response_text)
    if match:
        return match.group(1) == 'yes'
    else: 
        return False     

def clean_json(json_string):
    try:
        cleaned_data = json.loads(json_string)
        return json.dumps(cleaned_data, indent=2)
    except json.JSONDecodeError as e:
        logging.error(f"JSON Decode Error: {e}")
        return json_string

def run_llamafile():
    if not os.path.exists(LLAMAFILE_NAME):
        raise FileNotFoundError(f'{LLAMAFILE_NAME} does not exist.')

    command = f'./{LLAMAFILE_NAME} -m {LLAMAFILE_MODEL} --port {LLAMAFILE_PORT}'
    logging.info(f'Running {command}...')
    
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
        
        rules = load_rules()
        
        # Convert JSON data to human-readable format
        human_readable_data = json_to_human_readable(data)
        
        # Evaluate each rule
        high_risk_flagged = False
        for i, rule in enumerate(rules):
            rule_name = f"Rule {i+1}"
            applies = call_llm_for_rule_evaluation(human_readable_data, rule, rule_name)
            if applies:
                high_risk_flagged = True
                break
        
        if high_risk_flagged:
            result = {
                "score": "high",
                "justification": f"The transaction was flagged as high risk due to rule: {rule}"
            }
        else:
            result = {
                "score": "low",
                "justification": "None of the rules applied to this transaction."
            }
        
        return jsonify(result)
        
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error: {error_message}")
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    llamafile_process = run_llamafile()
    try:
        app.run(port=8080)
    finally:
        llamafile_process.send_signal(signal.SIGINT)
        llamafile_process.wait()
