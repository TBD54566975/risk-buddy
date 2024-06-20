import requests
import json
import os
from colorama import Fore, Style, Back
import colorama

def load_schema(file_path):
    with open(file_path) as f:
        return json.load(f)

def call_llm(prompt, api_key, temperature=0.1):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    return response.json()


def generate_rule_from_description(description, schema, api_key):
    prompt = f"""
You are an assistant in financial risk assessment. 
You need to convert natural language descriptions of rules into executable expressions based on the data given. 

The data will take the form of transaction json objects, which conform to the following schema: 

The schema for transactions and history is as follows:
{json.dumps(schema, indent=4)}

history is a list of past transactions.

The rules are evaluated using the following logic in Python code:

from asteval import Interpreter
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from dateutil.parser import isoparse

def evaluate_rules(transaction, history, rules):
    \"""
    Evaluate rules against the provided transaction and history.
    
    Uses asteval to safely evaluate deterministic expressions in the rules.
    Calls LLM to evaluate fuzzy expressions.
    \"""
    aeval = Interpreter()
    aeval.symtable['transaction'] = transaction
    aeval.symtable['history'] = history
    aeval.symtable['datetime'] = datetime
    aeval.symtable['relativedelta'] = relativedelta
    aeval.symtable['isoparse'] = isoparse
    aeval.symtable['timezone'] = timezone    

history = request.json.get('data') 
# data can be singular or a list of transactions with current one first. 
# Ensure history is always a list (handles single instance scenario)
if isinstance(history, dict):
    history = [history]
transaction = history[0]
history = history[1:]

.. 
and evaluated with aeval(rule string).

For example: 
rule description: Payin amount from USD_LEDGER is too high
expression: len([pair for pair in transaction['offering']['currencyPairs'] if pair['payin']['kind'] == 'USD_LEDGER' and float(pair['payin']['amount']) > 30000]) > 0




Now, based on the above information, convert the following natural language description into an executable rule:
\"\"\"
{description}
\"\"\"

The rule should be a Python expression that evaluates to True or False based on the data provided, not assigned to a variable. 
Return just the rule as text, not markdown, just a single line of text please, no extra quotes. Please avoid using generator expressions and instead use list comprehensions or other supported constructs.
"""
    
    
    response_data = call_llm(prompt, api_key)
    raw_rule = response_data['choices'][0]['message']['content']
    return raw_rule, prompt


def correct_rule(rule, error_msg, synth_data, previous_prompt, api_key):
    prompt = f"""
        {previous_prompt}

        {rule}

        Error: {error_msg}

        Please correct the rule expression.
    """

    response_data = call_llm(prompt, api_key, temperature=0.9)
    return response_data['choices'][0]['message']['content'], prompt



def synthesize_data_from_schema(schema, api_key):
    prompt = f"""
        Syntheize some data based on the schema provided: 
        {schema}

        It is CRITICAL that you return only valid json. 

        json:
    """
    response_data = call_llm(prompt, api_key)
    raw = response_data['choices'][0]['message']['content']

    ## now get result from between ```json .... ```
    synth =  raw.split('```json')[1].split('```')[0].strip()
    return json.loads(synth)
    

def validate_rule_with_synthetic_data(rule, data):

    from asteval import Interpreter
    from datetime import datetime, timezone
    from dateutil.relativedelta import relativedelta
    from dateutil.parser import isoparse
    transaction = data
    history = [data, data]

    aeval = Interpreter()
    aeval.symtable['transaction'] = transaction
    aeval.symtable['history'] = history
    aeval.symtable['datetime'] = datetime
    aeval.symtable['relativedelta'] = relativedelta
    aeval.symtable['isoparse'] = isoparse
    aeval.symtable['timezone'] = timezone    

    aeval(rule)
    if aeval.error:
        return aeval.error_msg
    else:
        return None


def main():
    colorama.init(autoreset=True)

    schema = load_schema('schema.json')
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print(Fore.RED + "API key not found. Make sure OPENAI_API_KEY environment variable is set.")
        return    

    print(Fore.CYAN + Style.BRIGHT + "Welcome to the Rule Generator!")
    description = input(Fore.YELLOW + "Enter the natural language rule description: ")
    
    print(Fore.MAGENTA + "Generating rule from description...")
    rule, prompt = generate_rule_from_description(description, schema, api_key)
    print(Fore.GREEN + "The rule generated:\n" + Fore.WHITE + Back.GREEN + "    " + rule)
    
    print(Fore.MAGENTA + "Will validate the rule now. Generating synthetic data to test with ...")
    synth_data = synthesize_data_from_schema(schema, api_key)
    
    max_attempts = 5
    for attempt in range(max_attempts):
        print(Fore.MAGENTA + f"Now testing with synthetic data (Attempt {attempt + 1}/{max_attempts}) ...")
        err = validate_rule_with_synthetic_data(rule, synth_data)
        if not err:
            print(Fore.GREEN + "Rule validation successful!")
            break
        else:
            print(Fore.RED + f"Rule validation failed with synthetic data (Attempt {attempt + 1}/{max_attempts}). Will try to correct it...")
            rule, prompt = correct_rule(rule=rule, error_msg=err, synth_data=synth_data, previous_prompt=prompt, api_key=api_key)
            print(Fore.GREEN + "The corrected rule generated:\n" + Fore.WHITE + Back.GREEN + "    " + rule)
    else:
        print(Fore.RED + "Failed to validate the rule after 5 attempts.")

    user_response = input(Fore.CYAN + Style.BRIGHT + "Process completed. Do you want to add the rule to rules.json? (yes/no): ").strip().lower()
    if user_response == 'yes':
        rules_file_path = 'rules.json'
        if os.path.exists(rules_file_path):
            with open(rules_file_path, 'r') as f:
                rules_data = json.load(f)
        else:
            rules_data = {"rules": []}
        
        new_rule = {
            "condition": rule,
            "action": "risky",
            "message": description
        }
        rules_data["rules"].append(new_rule)
        
        with open(rules_file_path, 'w') as f:
            json.dump(rules_data, f, indent=4)
        
        print(Fore.GREEN + "Rule added to rules.json successfully.")
    else:
        print(Fore.CYAN + "Rule was not added to rules.json.")




if __name__ == "__main__":
    main()
