from flask import Flask, request, jsonify
import os
import requests
import json
import subprocess
import shlex
import signal
import time

app = Flask(__name__)

# Path to the directory containing the rule files
RULES_DIR = './rules'
LLAMAFILE_PORT = 9090


# Load rules from disk
def load_rules():
    rules = []
    for filename in os.listdir(RULES_DIR):
        if filename.endswith('.txt'):
            with open(os.path.join(RULES_DIR, filename), 'r') as file:
                rules.append(file.read().strip())
    return rules

def format_prompt(data, rules):
    rules_text = '\n'.join(rules)
    prompt = (
        f"### Rules:\n"
        f"{rules_text}\n\n"
        f"### Transactional Data:\n"
        f"{json.dumps(data, indent=2)}\n\n"
        f"### Task:\n"
        f"Based on the rules provided, evaluate the data and return the best judgement in JSON format. Not all rules may apply to the data, so only consider relevant rules. Detailed reasoning and processing isn't needed, but do consider each rule if it may apply:\n"
        f"{{\n"
        f"  \"score\": \"one of 'high', 'medium', or 'low'\",\n"
        f"  \"justification\": \"a brief explanation based on the rules and data as to why the score is this\"\n"
        f"}}\n"
        f"\n### Evaluation Notes (for internal use):\n"
        f"- Ensure that each rule is considered, but understand that not all rules may apply.\n"
        f"- Highlight any transactions that meet the criteria of the rules.\n"
        f"- Provide a clear justification that references the specific rules that apply.\n"
    )
    return prompt

# Call the LLaMAfile API to score the data
def score_data(prompt):

    print("prompt", prompt)
    response = requests.post(f'http://localhost:{LLAMAFILE_PORT}/completion', json={
        'prompt': prompt,
        'n_predict': 150,  # Limit the response length
        'temperature': 0.0,  # Adjust the randomness of the generated text
    })
    response_data = response.json()
    # Extract the JSON content from the response
    response_text = response_data['content'].strip()
    print(response_text)

    print("JSON", response_text)


    start = response_text.find('{')
    end = response_text.rfind('}') + 1
    if start != -1 and end != -1:
        json_response = response_text[start:end]
    else:
        json_response = '{}'
    return json_response

LLAMAFILE_NAME = "llamafile"
LLAMAFILE_MODEL = "phi-3-mini-128k-instruct.Q8_0.gguf"
LLAMAFILE_PORT = 9090

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

        # Load rules
        rules = load_rules()
        
        # Format the prompt
        prompt = format_prompt(data, rules)
        
        # Get the score from LLaMAfile API
        score = score_data(prompt)
        
        # Print the score and any potential error
        print("Score:", score)
        
        return jsonify(json.loads(score))
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