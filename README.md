# Experimental risk scoring engine

Create a transaction risk score engine (go/no go on risk) using an approach that is using SLMs/LLMs combined with rules in natural language and predicate logic (an ensemble approach for risk scoring).
Uses a local language model to evaluate rules against data and a local rule engine. This can be inserted at any stage of transaction processing, to help decide if a given transaction should be reviewed or rejected etc.
(No data leaves the server at runtime).

## Aims

<img src="https://github.com/TBD54566975/risky-buddy/assets/14976/3d5cb56c-f94a-466c-babb-f0c2fb8924b3" width="300">

### Cold start problem
The cold start problem with risk is that you need a lot of data to train models. This can be addressed by using inference type rules, and also LLMs which have "common sense" reasoning knowledge in concert

### Run with modest hardware
Expression style rules run fast and anywhere, and SLMs can now run on modest hardware. LLMs can be used at "rule authoring" time to provide assistance and data synthesis. 

### Deal with variable data formats
With a messaging protocol like tbdex the exact details of exchange of values may vary over time or per exchange, meaning it may not be clear at all times what fields will be available to validate against. 

### Allow expressiveness
Some things are hard to express as strict logic such as "if the stated reason for the transaction doesn't match up with the magnitude of purchase" but it would be nice to be able to use these as rules. 
This simple natural language expressiveness can capture learned human agent knowledge, and either ahead of time compile it to a predicate logic rule (via an LLM), or evaluate it at runtime via an SLM. 

### Use logic
If we can use simple predicate logic, we should. No need for deep models or LLMs when a nice if statement will do! 

### Building confidence in transactions
By combining knowledge in rules and models, confidence in transactions can increase. Hopefully rules can be shared, or fine tuned models can also be shared in future. 

### Data privacy
No data should leave the server. 

# Does it work? 

Yes quite well in some parts, other bits, sort of?

Here it is matching data against a rule in that uses "common sense" reasoning in plain language: 
![image](https://github.com/TBD54566975/risk-buddy/assets/14976/db03921c-558b-48f9-b1da-961c44633e08)

And here it is translating from natural language to a predicate rule: 
![Pasted Graphic 6](https://github.com/TBD54566975/risk-buddy/assets/14976/1aa8a263-f835-4fa6-8dd2-9b154065f798)

Read on!


## Getting started

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
just dev
```

3. Test:
```bash
just test
```

4. Editing rules:
```bash
just rules
```


## API

Simple text based access - really any format can work to start with, it will do its best to apply the rules: 

```sh
curl -X POST http://localhost:8080/api/score -H "Content-Type: application/json" -d '{
  "data": {
    "amount": 15000,
    "transaction_type": "transfer"
  }
}'
```

Try another more complex one: 
```sh
curl -X POST http://localhost:8080/api/score -H "Content-Type: application/json" -d '{
  "data": {
    "account_age_months": 1,
    "current_transaction": {
      "amount": 20000,
      "transaction_type": "transfer",
      "currency": "USD",
      "from_account": "0x1234567890",
      "to_account": "0x0987654321",
      "reason": "Investment",
      "frequency": "bi-weekly"
    },
    "transaction_history": [
      {"amount": 8000, "transaction_type": "transfer", "currency": "USD"},
      {"amount": 10000, "transaction_type": "purchase", "currency": "USD"},
      {"amount": 20000, "transaction_type": "transfer", "currency": "USD"}
    ]
  }
}'
```

Output:

```json
{"reason":"The current transaction amount of 20000 USD is significant but does not exceed the high-risk threshold of 100000. However, considering this account is only 1 month old and has a bi-weekly transfer frequency which deviates from typical behavior (especially since there are already two transactions in its history), it raises some concern. The transaction amount matches with the stated reason 'Investment', but without additional context or historical data on investments, this could be flagged as medium risk.","risk":"medium"}
```


### API details

There is a `rules.json` and `schema.json` that define the rules to apply and the data format (if any) expected to be passed in. The `schema.json` file is any valid json schema you like. 
The data passed to the score endpoint can be a list of items that match that schema. The *first* item in the list is deemed to be the transaction to be scored. Any additional items are deemed to be the history (which rules may take into account). 

Out of the box there is a schema.json which is an approximate one for tbdex.

The rules can then express conditions on which a transaction is risky, either via expression style predicate logic, this is an example rule: 

```json
        {
            "condition": "len([pair for pair in transaction['offering']['currencyPairs'] if float(pair['payin']['amount']) > 1000]) > 0 and (datetime.now(timezone.utc) - isoparse(transaction['accountCreated'])).days < 30",
            "action": "risky",
            "message": "Transaction over 1000 and account is less than one month old"
        }
```

This then uses the data structure in `schema.json` if it can to apply the condition as an expression. 
This format is fairly verbose, so use `just rules` to help you write it. 

What if the data doesn't match schema.json? what if the rule can't be expressed that way? 

This is why rules can be expressed in natural language and evaluated at runtime: 

```json
        {
            "condition": "if the stated reason for the transaction doesn't match up with the magnitude of purchase",
            "action": "risky",
            "message": "mismatching explanation and amount"
        }
```
(hard to describe this one with predicate logic, but you know it when you see it!)





# How it works

## Rules and SLM

* Rules are stored in `rules.json` with a plain text message of what the rule means if it activates and the "if" condition (which can be plain text or predicate logic expression). 
* You can edit rules by hand or with `just rules` human rule editor which takes plain language rules and translates it to an expression language ahead of time
* Rules are evaluated at runtime as expressions (basically logic and if statements) or an SLM depending on if they are in natural language or not (automatically detected)
* The `asteval` library is used to evaluate predicate logic style expressions (which have been hand written or written with `just rules` from natural language) providing isolation
* Predicate rules using expressions work as long as there is a `schema.json` which describes the expected data format. If the data doesn't match that format, then it will try to use the SLM to evaluate the rules as best it can.
* At runtime it will see if the data matches the schema, or if a rule condition works with schema and the data, and apply it accordingly (as an expression if it is one or a natural language rule - again, automatic).


## SLM and rule evaluation at runtime

A rule may read like this: 

```json
        {
            "condition": "if the stated reason for the transaction doesn't match up with the magnitude of purchase",
            "action": "risky",
            "message": "mismatching explanation and amount"
        }
```        


And can be matched with the data via an LLM: 

```shell
INFO:root:LLM response: yes, the transaction data violates the rule. the reason for the transaction, which is payment for a coffee, does not match the magnitude of the purchase, which is $250.00. this discrepancy indicates a potential violation of the rule.
```

The data (abbreciated) would be something like: 

```json
                    "pair": "USD/BANK_STABLE",
                    "payin": {
                        "kind": "USD_LEDGER",
                        "amount": "250.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_STABLE",
                        "paymentDetails": {
                            "accountNumber": "0x1122334455",
                            "reason": "Payment for a coffee"
                        }
                    },
                    "estimatedSettlementTime": 5
```

Which intuitively appears like too much for a coffee (even if you are in Davos Switzerland).


## Models

Currently have been looking at the `phi3` model family from MSFT, which is ASF2 licensed, and quite good at reasoning yet small and can run in many places.
The 128k variant is favoured as it can comprehend a realistic set of rules and data in one hit. Read more here: https://huggingface.co/microsoft/Phi-3-mini-128k-instruct
You can also use models like Meta-Llama-3-8B.Q8_0.gguf, however the prompt will need adjusting. One future enhancement is to use a consensus of 3 disparate models (once prompts are tuned for each).

## Hosting models

Currently using llamafiles for a simple experience with models from huggingface (gguf format). The required model will be downloaded by `just dev` the first time it is run. 
Llamafiles are a convenient way to run from Mozilla built on llama.cpp. [See this](https://github.com/Mozilla-Ocho/llamafile). 
Llamafile is a x-platform executable which can be a whole model or can run gguf weights (currently using the latter per model). For example https://huggingface.co/MoMonir/Phi-3-mini-128k-instruct-GGUF - this is a 128k model which can be run with the llamafile. 

# Ideas, Enhancements and next steps

* Get some more data to test from!
* Make some more rules (both logic rules and natural language to try)
* Create scoring test suite (so can try different rule approaches)
* Fine tuning of models for this type of scoring (perhaps using huggingface)
* Allow editing of rules in a "live" spreadsheet (google sheets or similar) so you can have data and rules side by side as a workbench
* Try calling SLM multiple times with high temperature to get best results
* Try multiple models for convergance on answers
* Just In Time (JIT) generation of rules from human form to an expression against detected shape of data as it comes in (as data schemas may be dynamical)
* Rules are currently evaluated by the SLM one at a time, perhaps in bulk could be more efficient (if there are 100s/1000s of rules)

