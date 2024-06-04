from datetime import datetime, timedelta
import random
import requests

vectors = [
    {
        "offering": {
            "id": "offering-40510",
            "currencyPairs": [
                {
                    "pair": "USD/BANK_RANDOM",
                    "payin": {
                        "kind": "USD_LEDGER",
                        "amount": "45000.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_RANDOM",
                        "paymentDetails": {
                            "accountNumber": "0x3344556677",
                            "reason": "For services rendered"
                        }
                    },
                    "estimatedSettlementTime": 20
                }
            ]
        },
        "rfq": {
            "metadata": {
                "from": "did:example:user-10014",
                "to": "did:example:pfi-10014"
            },
            "data": {
                "offeringId": "offering-40510",
                "payin": {
                    "kind": "USD_LEDGER",
                    "amount": "45000.00",
                    "paymentDetails": {}
                },
                "payout": {
                    "kind": "BANK_RANDOM",
                    "paymentDetails": {
                        "accountNumber": "0x3344556677",
                        "reason": "Large unexpected transfer"
                    }
                },
                "claims": ["signed-credential"]
            }
        },
        "quote": {
            "metadata": {
                "from": "did:example:pfi-10014",
                "to": "did:example:user-10014",
                "exchangeId": "exchange-40510"
            },
            "data": {
                "expiresAt": "2024-06-04T14:00:00Z",
                "payin": {
                    "currencyCode": "USD",
                    "amount": "45000.00"
                },
                "payout": {
                    "currencyCode": "USD",
                    "amount": "44500.00"
                }
            }
        },
        "risk": {
            "expected-score": "high",
            "expected-justification": "5. High risk due to significant deviation from the customer's usual transaction pattern."
        },
        "history": [
            {
                "timestamp": "2023-06-10T14:22:11Z",
                "details": {
                    "amount": "150.00",
                    "reason": "Monthly subscription fee"
                }
            },
            {
                "timestamp": "2023-07-15T11:34:22Z",
                "details": {
                    "amount": "250.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2023-08-20T09:44:33Z",
                "details": {
                    "amount": "300.00",
                    "reason": "Donation to charity"
                }
            },
            {
                "timestamp": "2023-09-25T17:56:44Z",
                "details": {
                    "amount": "200.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2023-10-30T10:12:55Z",
                "details": {
                    "amount": "250.00",
                    "reason": "Monthly subscription fee"
                }
            },
            {
                "timestamp": "2024-05-30T12:34:56Z",
                "details": {
                    "amount": "45000.00",
                    "reason": "Large unexpected transfer"
                }
            }
        ]
    },
    {
        "offering": {
            "id": "offering-40511",
            "currencyPairs": [
                {
                    "pair": "USD/BANK_RANDOM",
                    "payin": {
                        "kind": "USD_LEDGER",
                        "amount": "200.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_RANDOM",
                        "paymentDetails": {
                            "accountNumber": "0x5566778899",
                            "reason": "Payment for services rendered"
                        }
                    },
                    "estimatedSettlementTime": 20
                }
            ]
        },
        "rfq": {
            "metadata": {
                "from": "did:example:user-10015",
                "to": "did:example:pfi-10015"
            },
            "data": {
                "offeringId": "offering-40511",
                "payin": {
                    "kind": "USD_LEDGER",
                    "amount": "200.00",
                    "paymentDetails": {}
                },
                "payout": {
                    "kind": "BANK_RANDOM",
                    "paymentDetails": {
                        "accountNumber": "0x5566778899",
                        "reason": "Payment for services rendered"
                    }
                },
                "claims": ["signed-credential"]
            }
        },
        "quote": {
            "metadata": {
                "from": "did:example:pfi-10015",
                "to": "did:example:user-10015",
                "exchangeId": "exchange-40511"
            },
            "data": {
                "expiresAt": "2024-06-04T14:00:00Z",
                "payin": {
                    "currencyCode": "USD",
                    "amount": "200.00"
                },
                "payout": {
                    "currencyCode": "USD",
                    "amount": "195.00"
                }
            }
        },
        "risk": {
            "expected-score": "low",
            "expected-justification": "6. Low risk due to consistent transaction pattern with usual behavior."
        },
        "history": [
            {
                "timestamp": "2023-06-10T14:22:11Z",
                "details": {
                    "amount": "150.00",
                    "reason": "Monthly subscription fee"
                }
            },
            {
                "timestamp": "2023-07-15T11:34:22Z",
                "details": {
                    "amount": "250.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2023-08-20T09:44:33Z",
                "details": {
                    "amount": "200.00",
                    "reason": "Donation to charity"
                }
            },
            {
                "timestamp": "2023-09-25T17:56:44Z",
                "details": {
                    "amount": "200.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2023-10-30T10:12:55Z",
                "details": {
                    "amount": "250.00",
                    "reason": "Monthly subscription fee"
                }
            },
            {
                "timestamp": "2023-11-30T10:12:55Z",
                "details": {
                    "amount": "150.00",
                    "reason": "Donation to charity"
                }
            }
        ]
    },
    {
        "offering": {
            "id": "offering-40512",
            "currencyPairs": [
                {
                    "pair": "USD/BANK_RANDOM",
                    "payin": {
                        "kind": "USD_LEDGER",
                        "amount": "150.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_RANDOM",
                        "paymentDetails": {
                            "accountNumber": "0x1122334455",
                            "reason": "Monthly subscription fee"
                        }
                    },
                    "estimatedSettlementTime": 20
                }
            ]
        },
        "rfq": {
            "metadata": {
                "from": "did:example:user-10016",
                "to": "did:example:pfi-10016"
            },
            "data": {
                "offeringId": "offering-40512",
                "payin": {
                    "kind": "USD_LEDGER",
                    "amount": "150.00",
                    "paymentDetails": {}
                },
                "payout": {
                    "kind": "BANK_RANDOM",
                    "paymentDetails": {
                        "accountNumber": "0x1122334455",
                        "reason": "Monthly subscription fee"
                    }
                },
                "claims": ["signed-credential"]
            }
        },
        "quote": {
            "metadata": {
                "from": "did:example:pfi-10016",
                "to": "did:example:user-10016",
                "exchangeId": "exchange-40512"
            },
            "data": {
                "expiresAt": "2024-06-04T14:00:00Z",
                "payin": {
                    "currencyCode": "USD",
                    "amount": "150.00"
                },
                "payout": {
                    "currencyCode": "USD",
                    "amount": "145.00"
                }
            }
        },
        "risk": {
            "expected-score": "low",
            "expected-justification": "7. Low risk due to consistent transaction pattern with usual behavior."
        },
        "history": [
            {
                "timestamp": "2023-06-10T14:22:11Z",
                "details": {
                    "amount": "150.00",
                    "reason": "Monthly subscription fee"
                }
            },
            {
                "timestamp": "2023-07-15T11:34:22Z",
                "details": {
                    "amount": "250.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2023-08-20T09:44:33Z",
                "details": {
                    "amount": "200.00",
                    "reason": "Donation to charity"
                }
            },
            {
                "timestamp": "2023-09-25T17:56:44Z",
                "details": {
                    "amount": "200.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2023-10-30T10:12:55Z",
                "details": {
                    "amount": "250.00",
                    "reason": "Monthly subscription fee"
                }
            },
            {
                "timestamp": "2023-11-30T10:12:55Z",
                "details": {
                    "amount": "150.00",
                    "reason": "Donation to charity"
                }
            }
        ]
    },
    {
        "offering": {
            "id": "offering-40513",
            "currencyPairs": [
                {
                    "pair": "USD/BANK_RANDOM",
                    "payin": {
                        "kind": "USD_LEDGER",
                        "amount": "200.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_RANDOM",
                        "paymentDetails": {
                            "accountNumber": "0x9988776655",
                            "reason": "Payment for services rendered"
                        }
                    },
                    "estimatedSettlementTime": 20
                }
            ]
        },
        "rfq": {
            "metadata": {
                "from": "did:example:user-10017",
                "to": "did:example:pfi-10017",
                "accountAgeMonths": 1
            },
            "data": {
                "offeringId": "offering-40513",
                "payin": {
                    "kind": "USD_LEDGER",
                    "amount": "200.00",
                    "paymentDetails": {}
                },
                "payout": {
                    "kind": "BANK_RANDOM",
                    "paymentDetails": {
                        "accountNumber": "0x9988776655",
                        "reason": "Payment for services rendered"
                    }
                },
                "claims": ["signed-credential"]
            }
        },
        "quote": {
            "metadata": {
                "from": "did:example:pfi-10017",
                "to": "did:example:user-10017",
                "exchangeId": "exchange-40513"
            },
            "data": {
                "expiresAt": "2024-06-04T14:00:00Z",
                "payin": {
                    "currencyCode": "USD",
                    "amount": "200.00"
                },
                "payout": {
                    "currencyCode": "USD",
                    "amount": "195.00"
                }
            }
        },
        "risk": {
            "expected-score": "high",
            "expected-justification": "8. High risk due to account being less than 3 months old with high transaction volume."
        },
        "history": [
            {
                "timestamp": "2024-04-01T14:22:11Z",
                "details": {
                    "amount": "150.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2024-04-05T11:34:22Z",
                "details": {
                    "amount": "200.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2024-04-10T09:44:33Z",
                "details": {
                    "amount": "250.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2024-04-15T17:56:44Z",
                "details": {
                    "amount": "300.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2024-04-20T10:12:55Z",
                "details": {
                    "amount": "150.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2024-04-25T12:34:56Z",
                "details": {
                    "amount": "200.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2024-04-30T14:56:22Z",
                "details": {
                    "amount": "250.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2024-05-05T16:44:33Z",
                "details": {
                    "amount": "300.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2024-05-10T18:56:44Z",
                "details": {
                    "amount": "150.00",
                    "reason": "Payment for services rendered"
                }
            },
            {
                "timestamp": "2024-05-15T20:12:55Z",
                "details": {
                    "amount": "200.00",
                    "reason": "Payment for services rendered"
                }
            }
        ]
    },
    {
        "offering": {
            "id": "offering-40514",
            "currencyPairs": [
                {
                    "pair": "USD/BANK_RANDOM",
                    "payin": {
                        "kind": "USD_LEDGER",
                        "amount": "50000.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_RANDOM",
                        "paymentDetails": {
                            "accountNumber": "0x4455667788",
                            "reason": "Office supplies"
                        }
                    },
                    "estimatedSettlementTime": 20
                }
            ]
        },
        "rfq": {
            "metadata": {
                "from": "did:example:user-10018",
                "to": "did:example:pfi-10018"
            },
            "data": {
                "offeringId": "offering-40514",
                "payin": {
                    "kind": "USD_LEDGER",
                    "amount": "50000.00",
                    "paymentDetails": {},
                    "reason": "for lunch"
                },
                "payout": {
                    "kind": "BANK_RANDOM",
                    "paymentDetails": {
                        "accountNumber": "0x4455667788",
                    }
                },
                "claims": ["signed-credential"]
            }
        },
        "quote": {
            "metadata": {
                "from": "did:example:pfi-10018",
                "to": "did:example:user-10018",
                "exchangeId": "exchange-40514"
            },
            "data": {
                "expiresAt": "2024-06-04T14:00:00Z",
                "payin": {
                    "currencyCode": "USD",
                    "amount": "50000.00"
                },
                "payout": {
                    "currencyCode": "USD",
                    "amount": "49500.00"
                }
            }
        },
        "risk": {
            "expected-score": "high",
            "expected-justification": "9. High risk due to mismatch between the transaction amount and the stated reason."
        }
    }
]

def run_tests():
    url = 'http://localhost:8080/api/score'
    results = []

    def is_partial_match(expected, actual):
        match_levels = {"low": 0, "medium": 1, "high": 2}
        if expected in match_levels and actual in match_levels:
            return abs(match_levels[expected] - match_levels[actual]) == 1
        return False

    total_tests = len(vectors)
    exact_matches = 0
    partial_matches = 0

    for i, vector in enumerate(vectors):
        expected_risk = vector.pop('risk', None)
        expected_score = expected_risk.get('expected-score')
        expected_justification = expected_risk.get('expected-justification')

        try:
            response = requests.post(url, json={'data': vector})
            if response.status_code == 200:
                result = response.json()
                actual_score = result.get('score', 'N/A')
                actual_justification = result.get('justification', 'N/A')
                if expected_score == actual_score:
                    match = "Exact"
                    exact_matches += 1
                elif is_partial_match(expected_score, actual_score):
                    match = "Partial"
                    partial_matches += 1
                else:
                    match = "Wrong"
            else:
                actual_score = "Error"
                actual_justification = response.text
                match = "Error"
        except Exception as e:
            actual_score = "Error"
            actual_justification = str(e)
            match = "Error"
        
        results.append({
            "Test Vector": i + 1,
            "Expected Score": expected_score,
            "Match": match,
            "Actual Score": actual_score,
            "Expected Justification": expected_justification,
            "Actual Justification": actual_justification
        })
        
        # Print each result as it's processed
        print(f"\nTest Vector {i + 1}")
        print(f"Expected Score: {expected_score}")
        print(f"Match: {match}")
        print(f"Actual Score: {actual_score}")
        print(f"Expected Justification: {expected_justification}")
        print(f"Actual Justification: {actual_justification}\n")
        
    # Summary
    correct_matches = exact_matches + partial_matches
    summary = f"Total Tests: {total_tests}, Exact Matches: {exact_matches}, Partial Matches: {partial_matches}, Correct Percentage: {correct_matches / total_tests * 100:.2f}%"
    print("\nSummary")
    print(summary)

if __name__ == '__main__':
    run_tests()