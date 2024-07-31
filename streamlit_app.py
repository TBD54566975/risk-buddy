import streamlit as st
import json
import os
from rule_assistant import call_llm

st.title('Risk Buddy Data and Rules Generator')

# Get the OpenAI API key from the environment or Streamlit secrets
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

# Generate natural language description of the schema
st.header('Schema')
if schema:
    schema_description = call_llm(f"Provide a brief natural language description of the following JSON schema in no more than 2-3 sentences:\n{json.dumps(schema, indent=4)}", OPENAI_API_KEY)
    st.write(schema_description['choices'][0]['message']['content'])
    st.json(schema)
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
