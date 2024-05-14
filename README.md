To use: 


* Run ollama
* Create rules in `rules/` in plain language
* `python main.py`


Then to access: 

```sh
curl -X POST http://localhost:8080/api/score -H "Content-Type: application/json" -d '{
  "data": {
    "amount": 15000,
    "transaction_type": "transfer"
  }
}'
```