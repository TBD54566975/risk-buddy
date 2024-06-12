import json
import jsonschema
from jsonschema import validate
from asteval import Interpreter
from datetime import datetime
from dateutil.relativedelta import relativedelta

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def evaluate_rules(transaction, history, rules):
    """
    Evaluate rules against the provided transaction and history.
    
    Uses asteval to safely evaluate expressions in the rules.
    Makes use of datetime and relativedelta for date-related conditions.
    """
    aeval = Interpreter()
    aeval.symtable['transaction'] = transaction
    aeval.symtable['history'] = history
    aeval.symtable['datetime'] = datetime
    aeval.symtable['relativedelta'] = relativedelta
    results = []

    for rule in rules:
        condition = rule['condition']
        if aeval(condition):
            results.append({"action": rule['action'], "message": rule['message']})
    
    return results

def process_rules(history):
    """Main function to load schema, rules, and data, validate data, and evaluate rules."""
    # Load schema, rules, and data from respective JSON files
    schema = load_json('schema.json')
    rules = load_json('rules.json')['rules']
    

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
    history = load_json('data.json')
    process_rules(history)
    history = load_json('data_ok.json')
    process_rules(history)
