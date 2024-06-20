import requests
import json
import os


def load_schema(file_path):
    with open(file_path) as f:
        return json.load(f)

def call_llm(prompt, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
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

history is a list of past transactions (as a dict).

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

.. 
and evaluated with aeval(rule string).

Now, based on the above information, convert the following natural language description into an executable rule:
\"\"\"
{description}
\"\"\"

The rule should be a Python expression that evaluates to True or False based on the data provided, not assigned to a variable. 
Return just the rule as text, not markdown, just a single line of text please.
"""
    
    
    response_data = call_llm(prompt, api_key)
    raw_rule = response_data['choices'][0]['message']['content']
    return raw_rule, prompt


def correct_rule(rule, error_msg, synth_data, previous_prompt, api_key):
    prompt = f"""
        {previous_prompt}

        {rule}

        Error: {error_msg}

        Please correct the rule expression to be valid Python code that evaluates to True or False based on the data provided.
        The rule should be a Python expression that evaluates to True or False based on the data provided, not assigned to a variable. 
        Return just the rule as text, not markdown, just a single line of text please.
    """

    response_data = call_llm(prompt, api_key)
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
    return raw.split('```json')[1].split('```')[0].strip()
    

def validate_rule_with_synthetic_data(rule, data):

    from asteval import Interpreter
    from datetime import datetime, timezone
    from dateutil.relativedelta import relativedelta
    from dateutil.parser import isoparse
    transaction = data
    history = [data]

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
    schema = load_schema('schema.json')
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("API key not found. Make sure OPENAI_API_KEY environment variable is set.")
        return    

    description = input("Enter the natural language rule description: ")
    rule, prompt = generate_rule_from_description(description, schema, api_key)
    print("The rule generated:", rule)
    print("Will validate the rule now. Generating synthetic data to test with ... ")

    synth_data = synthesize_data_from_schema(schema, api_key)
    print("Now testing with synthetic data ... ")
    err = validate_rule_with_synthetic_data(rule, synth_data)
    if err:
        print("Rule validation failed with synthetic data. will try to correct it...")
        corrected_rule, prompt = correct_rule(rule=rule, error_msg=err, synth_data=synth_data, previous_prompt=prompt, api_key=api_key)
        print("The rule generated:", corrected_rule)




if __name__ == "__main__":
    main()
