# Experimental risk scoring engine

Looking at using SLMs/LLMs combined with rules in natural language to score risk (potentialy part of an ensemble approach for risk scoring). 

![image](https://github.com/TBD54566975/risky-buddy/assets/14976/3d5cb56c-f94a-466c-babb-f0c2fb8924b3)


## Setup 

* Create rules in `rules/` in plain language
* `python main.py` (first time will take a while as it downloads a phi3 llamafile - should work on any platform)
* Pass in data (any format wrapped in json can work), see below for examples and get a score and justification back.


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


# Models

Currently have been looking at the `phi3` model from MSFT, which is ASF2 licensed, and quite good at reasoning yet small.
The 128k variant is favoured as it can comprehend a realistic set of rules and data in one hit. 

## Hosting models

For this to work an LLM model has to be hosted. Currently using llamafiles for developtime experience with models from huggingface. 

### Llama files
Llamafiles are a convenient way to run from Mozilla built on llama.cpp. [See this](https://github.com/Mozilla-Ocho/llamafile). 

Llamafile is a x-platform executable which can be a whole model or can run gguf weights (currently using the latter per model). For example https://huggingface.co/MoMonir/Phi-3-mini-128k-instruct-GGUF - this is a 128k model which can be run with the llamafile. 

### Other ways of hosting models

There are other ways to host models which are not out of the box or platform limited:

* TGI from huggingface is convenient: https://github.com/huggingface/text-generation-inference (docker based, but AMD64 only -  provent at scale server side hosting)
* https://github.com/vllm-project/vllm - linux specific ways to host LLMs.
* Ollama: this is technically more of a desktop platform, but is convenient (and written in golang). 

