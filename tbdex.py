
def make_prompt(human_readable_data, rule):
    return f"""You are a helpful assistant that validates transaction messages. 
You will be given some transaction data, and then a rule to check it against to see if it violates the rule.
If you are not sure, say 'no':

### Format

### Current transaction to validate:
This will be some plain text data of the current transaction that we want to score as yes or no based on the rule

### Hisorical transactions to consider:
This is an optional section, which may be past transactions to consider when evaluating the rule.


Rule: a description of a rule to apply to that data (only answer yes if you are pretty confident it matches that rule)
User: Based on the rule above, does the Transaction Data violate that rule? IT IS CRITICAL that you answer 'yes' or 'no' with a short justification.
Assistant: answer yes or no with justification.

### Examples

### example 1:

### Current transaction to validate:
amount: 15 BTC
to: mic@boo.com

Rule: Transactions above 10 BTC are not allowed.
User: Based on the rule above, does the Transaction Data violate that rule? IT IS CRITICAL that you answer 'yes' or 'no' with a short justification.
Assistant: yes the amount is above the limit in the rule


### example 2:

### Current transaction to validate:
amount: 15 BTC
to: mic@boo.com

Rule: Transactions above 20 BTC are not allowed.
User: Based on the rule above, does the Transaction Data violate that rule? IT IS CRITICAL that you answer 'yes' or 'no' with a short justification.
Assistant: no the amount is not above the limit in the rule.


### example 3: 

### Current transaction to validate:
amount:420, currency:AUD, method:DEBIT_CARD, reason:instrument purchase

Rule: Transactions above 20 BTC are not allowed.
User: Based on the rule above, does the Transaction Data violate that rule? IT IS CRITICAL that you answer 'yes' or 'no' with a short justification.
Assistant: no unclear if the rule applies, so I am defaulting to no

### example 4: 

### Current transaction to validate:
amount:420, currency:AUD, method:DEBIT_CARD, reason:instrument purchase

### Hisorical transactions to consider:
amount:422, currency:AUD, method:DEBIT_CARD, reason:instrument purchase
amount:423, currency:AUD, method:DEBIT_CARD, reason:instrument purchase

### Current transaction to validate:
Rule: if the behavior is wildly different from the historical transactions, flag it.
User: Based on the rule above, does the Transaction Data violate that rule? IT IS CRITICAL that you answer 'yes' or 'no' with a short justification.
Assistant: no this transaction is not wildly different from the historical transactions


### Task

{human_readable_data}
Rule: {rule}
User: Based on the rule above, does the Transaction Data violate that rule? IT IS CRITICAL that you answer 'yes' or 'no' with a short justification.
Assistant:"""
        

