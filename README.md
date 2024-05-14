To try: 

* get https://ollama.com/ and run it
* Create rules in `rules/` in plain language
* `python main.py`
* Access it and pass in data (any format wrapped in json can work), see below


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

Will result in something like: 
```txt
{"score":"{\n    \"score\": \"medium\",\n    \"reason\": \"The current transaction amount of 20000 is not high risk as it does not exceed 100000. However, considering this account is only 1 month old and has a high transaction volume (with two transactions over 10000 in the same currency), there is potential for medium risk due to unusual activity patterns.\"\n}"}
```