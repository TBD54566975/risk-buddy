# Experimental risk scoring engine

This is an approach that is using SLMs/LLMs combined with rules in natural language and predicate logic to score risk (an ensemble approach for risk scoring).
Uses a local language model to evaluate rules against data and a local rule engine.
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

# Does it work? 

Yes quite well in some parts, other bits, sort of?

Here it is matching data against a rule in plain language: 
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

## Rules

* Rules are stored in `rules.json` with a plain text message of what the rule means if it activates and the "if" condition (which can be plain text or predicate logic expression).
* `python main.py` 
* You can edit rules by hand 


## API

Simple text based access - really any format can work. 

Then to access: 

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


## Example with transaction history: 

```sh
curl -X POST http://localhost:8080/api/score -H "Content-Type: application/json" -d '{
  "data": {
    "account_age_months": 2,
    "current_transaction": {
      "amount": 22000,
      "transaction_type": "investment",
      "currency": "USD",
      "from_account": "0x1234567890",
      "to_account": "0x0987654321",
      "reason": "Investment in unknown assets",
      "date": "2024-05-01",
      "frequency": "monthly"
    },
    "transaction_history": [
      {
        "amount": 8000,
        "transaction_type": "investment",
        "currency": "USD",
        "from_account": "0x1234567890",
        "to_account": "0x0987654321",
        "reason": "Investment in new venture",
        "date": "2024-04-01"
      },
      {
        "amount": 10000,
        "transaction_type": "investment",
        "currency": "USD",
        "from_account": "0x1234567890",
        "to_account": "0x0987654321",
        "reason": "Investment in stocks",
        "date": "2024-04-15"
      },
      {
        "amount": 22000,
        "transaction_type": "investment",
        "currency": "USD",
        "from_account": "0x1234567890",
        "to_account": "0x0987654321",
        "reason": "Investment in unknown assets",
        "date": "2024-04-25"
      }
    ]
  }
}'
```

# LLM and rule evaluation at runtime

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

The data (abbreciated) woudl be something like: 

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

Which intuitively (even if you are in Davos Switzerland) appears like too much for a coffee. 


# Models

Currently have been looking at the `phi3` model from MSFT, which is ASF2 licensed, and quite good at reasoning yet small.
The 128k variant is favoured as it can comprehend a realistic set of rules and data in one hit. Read more here: https://huggingface.co/microsoft/Phi-3-mini-128k-instruct
You can also use models like Meta-Llama-3-8B.Q8_0.gguf, however the prompt will need adjusting. One future enhancement is to use a consensus of 3 disparate models (once prompts are tuned for each).

Update: llama3 seems to work better reasoning over human readable data.

## Hosting models

For this to work an LLM model has to be hosted. Currently using llamafiles for developtime experience with models from huggingface. 

### Llama files
Llamafiles are a convenient way to run from Mozilla built on llama.cpp. [See this](https://github.com/Mozilla-Ocho/llamafile). 

Llamafile is a x-platform executable which can be a whole model or can run gguf weights (currently using the latter per model). For example https://huggingface.co/MoMonir/Phi-3-mini-128k-instruct-GGUF - this is a 128k model which can be run with the llamafile. 

### Other ways of hosting models

There are other ways to host models which are not out of the box or platform limited:

* TGI from huggingface is convenient: https://github.com/huggingface/text-generation-inference (docker based, but AMD64 only -  provent at scale server side hosting)
* https://github.com/vllm-project/vllm - linux specific ways to host LLMs.
* Ollama: this is technically more of a desktop platform, but is convenient (and written in golang). Downsides are that it has out of the box more limited set of models (but you can import them via modelfiles from gguf - so it is viable and convenient in some cases). It can also serve multiple models from one port whereas llamafiles is just one model per port.

