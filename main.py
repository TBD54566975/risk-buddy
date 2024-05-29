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
LLAMAFILE_MODEL = "Meta-Llama-3-8B.Q4_0.gguf"

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

def format_evaluation_prompt(human_readable_data, rules, similar_transactions=None):
    rules_text = '\n'.join(rules)
    prompt = (
        f"Take the rules and transactional data described below and evaluate if any of the rules apply to the transaction, returning only JSON as instructed.\n"
        f"### Rules:\n"
        f"{rules_text}\n\n"
        f"### Transactional Data:\n"
        f"{human_readable_data}\n\n"
    )

    if similar_transactions:
        prompt += "### Possibly Related Transactions:\n\n"
        for trans, score in similar_transactions:
            prompt += f"{trans}\n\n"

    prompt += (
        f"\n### Evaluation Notes (for internal use):\n"
        f"- Ensure that each rule is considered, but understand that not all rules may apply.\n"
        f"- Highlight any transactions that meet the criteria of the rules.\n"
        f"- Provide a clear justification that references the specific rules that apply.\n"                    
        f"- If any related transactions are present, consider them in evaluating rules that may apply.\n"                    
        f"### Task:\n"
        f"Based on the rules provided, evaluate the data and return the best judgement in JSON format. Not all rules may apply to the data, so only consider relevant rules. Detailed reasoning and processing isn't needed, but do consider each rule if it may apply:\n"
        f"{{\n"
        f"  \"score\": \"one of 'high', 'medium', or 'low'\",\n"
        f"  \"justification\": \"a brief explanation based on the rules and data as to why the score is this\"\n"
        f"}}\nResults:"
    )
    return prompt

def call_llm(prompt):

    print("\n\n\n\n\n\n\nPROMPT\n\n\n\n" + prompt + "\n\n\n\n\n\n\nEND PROMPT\n\n\n\n\n")

    response = requests.post(f'http://localhost:{LLAMAFILE_PORT}/completion', json={
        'prompt': prompt,
        'n_predict': 150,
        'temperature': 0.0,

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
        
        # Format the evaluation prompt
        evaluation_prompt = format_evaluation_prompt(human_readable_data, rules, similar_transactions)
        score_response = call_llm(evaluation_prompt)
        
        json_score = extract_json_from_response(score_response)
        try:
            cleaned_json_score = clean_json(json_score)
            return jsonify(json.loads(cleaned_json_score))
        except Exception as e:
            print("Error processing JSON response:", score_response)
            return jsonify({'error': str(e), 'response': score_response}), 500

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
