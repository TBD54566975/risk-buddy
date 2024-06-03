from flask import Flask, request, jsonify
import os
import requests
import json
import subprocess
import signal
import time
import embedding
from tbdex import TBDEX_PROTOCOL_DESCRIPTION, TBDEX_JARGON

app = Flask(__name__)

# Constants
RULES_DIR = './rules'
LLAMAFILE_PORT = 9090
LLAMAFILE_NAME = "llamafile"
LLAMAFILE_MODEL = "phi-3-medium-128k-instruct-Q5_K_M.gguf"

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

def call_llm_for_evaluation(human_readable_data, rules):
    rules_text = '\n'.join([f"Rule {i+1}: {rule}" for i, rule in enumerate(rules)])
    system_prompt = (
        "Transcript of a never-ending dialog, where the User interacts with an Assistant reviewing remittance related data. "
        "The Assistant is a risk evaluating agent looking for risks according to the provided rules. "
        "The Assistant is helpful, honest, good at writing, and never fails to answer the User's requests immediately and with precision."
    )
    
    n_shot_examples = (
        "User: Here is a transaction with an amount of 0.0001 BTC.\n"
        "Assistant: low\n\n"
        "User: Here is a transaction with an amount of 10,000 USD to an unknown account.\n"
        "Assistant: high\n\n"
        "User: Here is a transaction with an amount of 500 USD from a well-known merchant.\n"
        "Assistant: low\n\n"
        "User: Here is a transaction with an amount of 50,000 USD with no stated reason.\n"
        "Assistant: high\n\n"
        "User: Here is a transaction with an amount of 200 USD from USD to MOMO.\n"
        "Assistant: low\n"
    )
    
    prompt = (
        f"{system_prompt}\n\n"
        f"User: Evaluate the following transactional data based on the provided rules and determine the risk level. "
        f"Return only the risk level as a single word: 'high' or 'low'.\n\n"
        f"tbDEX Protocol Description:\n{TBDEX_PROTOCOL_DESCRIPTION}\n\n"
        f"And some explanations of jargon:\n{TBDEX_JARGON}\n\n"
        f"Rules:\n{rules_text}\n\n"
        f"Example:\n"
        f"{n_shot_examples}\n"
        f"Transactional Data:\n{human_readable_data}\n\n"
        f"User: Based on the rules provided, evaluate the data and return the risk level as a single word: 'high' or 'low'.\n"
        f"Ensure your evaluation strictly adheres to the given rules without creating new ones.\n"
        f"Assistant:"
    )

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
    response_text = response_data['content'].strip().split('\n')[0].lower()
    print("risk level response:", response_text)
    if any(word in response_text for word in ["high", "low"]):
        # Extract the first instance of 'high' or 'low'
        risk_level = next((word for word in ["high", "low"] if word in response_text), "low")
        return risk_level
    return "low"  # Default to low if response is not clear

def call_llm_for_justification(human_readable_data, rules, risk_level):
    rules_text = '\n'.join([f"Rule {i+1}: {rule}" for i, rule in enumerate(rules)])
    
    # Adding more specific chain-of-thought guidance
    chain_of_thought = (
        "Let's analyze the data step-by-step to determine the justification:\n"
        "1. Identify which rules apply to this transaction.\n"
        "2. Check if the transaction data matches the conditions in those rules.\n"
        "3. Provide a justification based on the applicable rules and transaction data.\n"
        "4. Ensure the justification mentions the specific rules and why they apply without introducing any new rules."
    )
    
    prompt = (
        f"User: The following transaction has been flagged as '{risk_level}' risk. Provide a brief justification for this risk level based on the rules provided. "
        f"Ensure to include the word '{risk_level}' in your justification and only refer to the given rules without creating new ones. "
        f"Each rule you reference must be explicitly quoted as given in the list of rules.\n\n"
        f"tbDEX Protocol Description:\n{TBDEX_PROTOCOL_DESCRIPTION}\n\n"
        f"And some explanations of jargon:\n{TBDEX_JARGON}\n\n"
        f"Rules:\n{rules_text}\n\n"
        f"Transactional Data:\n{human_readable_data}\n\n"
        f"{chain_of_thought}\n\n"
        f"Assistant: Provide a brief explanation as to why the transaction is considered '{risk_level}' risk based on the rules and data."
    )

    response = requests.post(f'http://localhost:{LLAMAFILE_PORT}/completion', json={
        'prompt': prompt,
        'n_predict': 50,
        'temperature': 0.0,
        'top_p': 0.9,
        'min_p': 0.4,
        'top_k': 50,
        'stop': ["User:", "Assistant:"]
    })
    response_data = response.json()
    response_text = response_data['content'].strip().lower()
    print("justification response:", response_text)
    return response_text

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
        
        embedding.add_document(data_s)
        
        rules = load_rules()
        
        # Convert JSON data to human-readable format
        human_readable_data = json_to_human_readable(data)
        
        # Step 1: Determine the risk level
        risk_response = call_llm_for_evaluation(human_readable_data, rules).strip().lower()
        
        if risk_response == "high":
            # Step 2: Request justification for flagged transactions
            justification_response = call_llm_for_justification(human_readable_data, rules, risk_response).strip().lower()
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

if __name__:
    llamafile_process = run_llamafile()
    try:
        app.run(port=8080)
    finally:
        llamafile_process.send_signal(signal.SIGINT)
        llamafile_process.wait()
