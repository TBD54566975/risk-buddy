import streamlit as st
import json

st.title('Risk Buddy Data and Rules Generator')

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
    rules = {}

st.header('Schema')
st.json(schema)

st.header('Rules')
st.json(rules)

# Adding a new rule
st.header('Add a New Rule')
condition = st.text_area('Condition')
action = st.text_input('Action')
message = st.text_input('Message')

if st.button('Add Rule'):
    if condition and action and message:
        new_rule = {
            'condition': condition,
            'action': action,
            'message': message
        }
        rules['rules'].append(new_rule)
        # Save the updated rules back to rules.json
        with open('rules.json', 'w') as f:
            json.dump(rules, f, indent=4)
        st.success('Rule added successfully!')
    else:
        st.error('Please fill in all fields')
