import streamlit as st
import json
import requests

st.title('Risk Buddy Data and Rules Generator')

# Get the OpenAI API key from the environment or Streamlit secrets
import os

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError('The OpenAI API key must be set in the environment variable OPENAI_API_KEY')

# Load schema.json
try:
    with open('schema.json', 'r') as f:
        schema = json.load(f)
except FileNotFoundError:
    st.error('schema.json not found')
    schema = {}

# Load rules.json
try:
    with open('rules.json', 'r') as f:
        rules = json.load(f)
except FileNotFoundError:
    st.error('rules.json not found')
    rules = {"rules": []}

# Function to call OpenAI API
def call_openai(prompt, temperature=0.1):
    api_key = os.getenv('OPENAI_API_KEY')

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

# Generate natural language description of the schema
st.header('Schema')
if schema:
    schema_description = call_openai(f"Provide a brief natural language description of the following JSON schema:\n{json.dumps(schema, indent=4)}")
    st.write(schema_description['choices'][0]['message']['content'])
else:
    st.error('No schema found')

# Display rules in a tabular format
st.header('Rules')
if rules and "rules" in rules:
    st.dataframe({
        "Description": [rule["message"] for rule in rules["rules"]],
        "Rule Script": [rule["condition"] for rule in rules["rules"]]
    })
else:
    st.write('No rules found')

# Adding a new rule
st.header('Add a New Rule')
natural_language_rule = st.text_input('Enter the natural language rule description')

if st.button('Add Rule'):
    if natural_language_rule:
        # Generate rule script from natural language description using OpenAI API
        rule_script = call_openai(f"Generate a Python rule script from the following natural language rule description:\n{natural_language_rule}")
        new_rule = {
            'condition': rule_script,
            'action': 'risky',
            'message': natural_language_rule
        }
        rules["rules"].append(new_rule)
        # Save the updated rules back to rules.json
        with open('rules.json', 'w') as f:
            json.dump(rules, f, indent=4)
        st.success('Rule added successfully!')
    else:
        st.error('Please enter a rule description')

st.write("Explore the schema by expanding it below:")
st.json(schema)
