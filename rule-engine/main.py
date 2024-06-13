import json
import jsonschema
from jsonschema import validate
from asteval import Interpreter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import isoparse
import requests

LLAMAFILE_PORT = 5000  # Example port number for LLM API

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def call_llm(prompt):
    """Call the LLM to evaluate a fuzzy condition."""
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
    return response_text == "true"

def is_valid_expression(condition, aeval):
    """Check if the condition is a valid expression."""
    try:
        aeval(condition)
        return True
    except Exception:
        return False

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

    for rule in rules:
        condition = rule['condition']
        
        if is_valid_expression(condition, aeval):
            # The whole condition is valid, evaluate directly
            if aeval(condition):
                results.append({"action": rule['action'], "message": rule['message']})
        else:
            # Split the condition and evaluate parts
            parts = condition.split(' and ')
            part1_valid = is_valid_expression(parts[0], aeval)
            part2_valid = len(parts) > 1 and is_valid_expression(parts[1], aeval)
            
            if part1_valid and part2_valid:
                if aeval(parts[0]) and aeval(parts[1]):
                    results.append({"action": rule['action'], "message": rule['message']})
            elif part1_valid:
                if aeval(parts[0]) and call_llm(f"Evaluate: {parts[1].strip()}"):
                    results.append({"action": rule['action'], "message": rule['message']})
            elif part2_valid:
                if aeval(parts[1]) and call_llm(f"Evaluate: {parts[0].strip()}"):
                    results.append({"action": rule['action'], "message": rule['message']})
            else:
                # Both parts are fuzzy
                if call_llm(f"Evaluate: {condition.strip()}"):
                    results.append({"action": rule['action'], "message": rule['message']})

    return results

def main():
    """Main function to load schema, rules, and data, validate data, and evaluate rules."""
    # Load schema, rules, and data from respective JSON files
    schema = load_json('schema.json')
    rules = load_json('rules.json')['rules']
    history = load_json('data.json')

    # Ensure history is always a list (handles single instance scenario)
    if isinstance(history, dict):
        history = [history]

    # Take the first item as the current transaction
    transaction = history[0]

    # Validate each item in history against the schema
    try:
        for item in history:
            validate(instance=item, schema=schema)
        print("Data is valid.")
    except jsonschema.exceptions.ValidationError as err:
        print(f"Data is invalid: {err.message}")
        return

    # Evaluate rules against the transaction and history
    results = evaluate_rules(transaction, history, rules)
    print("Evaluation Results:", json.dumps(results, indent=4))

if __name__ == "__main__":
    main()
