from flask import Flask, request, jsonify
import os
import requests
import json
import subprocess
import signal
import time
import logging
import re
import jsonschema
from jsonschema import validate
from asteval import Interpreter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import isoparse

from tbdex import TBDEX_PROTOCOL_DESCRIPTION, TBDEX_JARGON

app = Flask(__name__)

# Constants
RULES_DIR = './rules'
LLAMAFILE_PORT = 9090
LLAMAFILE_NAME = "llamafile"
LLAMAFILE_MODEL = "phi-3-mini-128k-instruct.Q8_0.gguf"

# Configure logging
logging.basicConfig(level=logging.INFO)


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

def call_llm_for_rule_evaluation(human_readable_data, rule):
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

def score_with_llm(data, rules):
    data = request.json.get('data')    
    
    # Convert JSON data to human-readable format
    human_readable_data = json_to_human_readable(data)
    
    # Evaluate each rule
    high_risk_flagged = False
    rules_matched = []
    rules_checked = []
    for i, rule in enumerate(rules):
        rules_checked.append(rule['message'])
        applies = call_llm_for_rule_evaluation(human_readable_data, rule['condition'])
        if applies:
            print("RULE APPLIES", rule)
            rules_matched.append(rule['condition'])
            high_risk_flagged = True
    
    if high_risk_flagged:
        result = {
            "score": "high",
            "justification": f"The transaction was flagged as high risk due to rule: {rules_matched} with rules checked: {rules_checked}."
        }
    else:
        result = {
            "score": "low",
            "justification": "None of the rules applied to this transaction."
        }
    
    return jsonify(result)    

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)





def is_valid_expression(condition, aeval):
    """Check if the condition is a valid expression."""
    aeval(condition)
    if aeval.error:
        aeval.error = []
        print("condition is not valid", condition)
        return False
    return True

def evaluate_rules(transaction, history, rules):
    """
    Evaluate rules against the provided transaction and history.
    
    Uses asteval to safely evaluate deterministic expressions in the rules.
    Calls LLM to evaluate fuzzy expressions.
    """
    aeval = Interpreter()
    aeval.symtable['transaction'] = transaction
    aeval.symtable['history'] = history
    aeval.symtable['datetime'] = datetime
    aeval.symtable['relativedelta'] = relativedelta
    aeval.symtable['isoparse'] = isoparse
    results = []

    def call_llm(transaction, history, rule):
        if history:
            return call_llm_for_rule_evaluation("Current transaction to example\n" +json_to_human_readable(transaction)+
                                                "\nHisorical transactions:\n" +json_to_human_readable(transaction), rule)
        else:
            return call_llm_for_rule_evaluation(json_to_human_readable(transaction), rule)

    for rule in rules:
        condition = rule['condition']
        print("!!!!!   -----> CONDITION:", condition)
        
        if is_valid_expression(condition, aeval):
            
            # The whole condition is valid, evaluate directly
            print("!!!!!   -----> VALID")
            if aeval(condition):
                results.append(rule['message'])
        else:
            print("here")
            # Split the condition and evaluate parts
            parts = condition.split(' and ')
            part1_valid = is_valid_expression(parts[0], aeval)
            part2_valid = len(parts) > 1 and is_valid_expression(parts[1], aeval)
            print("here2")

            if part1_valid and part2_valid:
                if aeval(parts[0]) and aeval(parts[1]):
                    results.append(rule['message'])
            elif part1_valid:
                if aeval(parts[0]) and call_llm(transaction, history, parts[1].strip()):
                    results.append(rule['message'])
            elif part2_valid:
                if aeval(parts[1]) and call_llm(transaction, history, parts[0].strip()):
                    results.append(rule['message'])
            else:
                # Both parts are fuzzy
                if call_llm(transaction, history, condition.strip()):
                    results.append(rule['message'])

    if len(results) > 0:
        result = {
            "score": "high",
            "justification": f"The transaction was flagged as high risk due to the following rules: {results}."
        }
    else:
        result = {
            "score": "low",
            "justification": "None of the rules applied to this transaction."
        }     
    return jsonify(result)       


schema = load_json('schema.json')
rules = load_json('rules.json')['rules']

@app.route('/api/score', methods=['POST'])
def score():
    try:
                
        history = request.json.get('data') 
        # data can be singular or a list of transactions with current one first. 
        # Ensure history is always a list (handles single instance scenario)
        if isinstance(history, dict):
            history = [history]

        # now lets check if we can evaluate these with rules, or fall back to score with llm alone
        # validate each item in history against the schema
        try:
            for item in history:
                validate(instance=item, schema=schema)
            

        except jsonschema.exceptions.ValidationError as err:
            print(f"Data is not according to schema, will use LLM only: {err.message}")
            return score_with_llm(request.json.get('data'), rules)
            
        # Evaluate rules against the transaction and history
        # get the head and then tail as history 
        print("Data is valid against schema.")                        
        transaction = history[0]
        history = history[1:]
        return evaluate_rules(transaction, history, rules)

        
        
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

