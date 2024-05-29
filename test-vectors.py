vectors = [
    {
        "offering": {
            "id": "offering_01hyr80tpyfznvykzgw72apveh",
            "currencyPairs": [
                {
                    "pair": "BTC/MOMO",
                    "payin": {
                        "kind": "BTC_LEDGER",
                        "amount": "2",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "MOMO_MPESA",
                        "paymentDetails": {}
                    },
                    "estimatedSettlementTime": 15
                }
            ]
        },
        "rfq": {
            "metadata": {
                "kind": "rfq",
                "to": "did:dht:ho3axp5pgp4k8a7kqtb8knn5uaqwy9ghkm98wrytnh67bsn7ezry",
                "from": "did:dht:s3mow5af1a4ie715mbxxjeoyt4jn1ohgpz75mn5gizj7cuubu6ao",
                "id": "rfq_01hyr8v81hemcaeq10n3fm6qqz",
                "exchangeId": "rfq_01hyr8v81hemcaeq10n3fm6qqz",
                "createdAt": "2024-05-25T16:20:22.710212Z",
                "protocol": "1.0"
            },
            "data": {
                "offeringId": "offering_01hyr80tpyfznvykzgw72apveh",
                "payin": {
                    "amount": "2",
                    "kind": "BTC_LEDGER"
                },
                "payout": {
                    "kind": "MOMO_MPESA"
                },
                "claimsHash": "j_vWQ9-2AGf-ykDVQmjwFrXmRAVaDc748WVBkE-0-8Q"
            },
            "privateData": {
                "salt": "KVad9SnO2sufTDnpAKh4sg",
                "claims": []
            },
            "signature": "eyJhbGciOiJFZERTQSIsImtpZCI6ImRpZDpkaHQ6czNtb3c1YWYxYTRpZTcxNW1ieHhqZW95dDRqbjFvaGdwejc1bW41Z2l6ajdjdXVidTZhbyMwIn0..KVK75zu4gZpZav1BzAqtea4WSu_J_jRUs7ZJx_ZpTAr3mtIaVPB1PUB8f6xnUmRbWXtKXBxgNCZQDAnx3VjpDw"
        },
        "risk": {
            "expected-score": "low",
            "expected-justification": "No risk, is known legitimate."
        }
    },
    {
        "offering": {
            "id": "offering-40506",
            "currencyPairs": [
                {
                    "pair": "USD/BANK_ANZ",
                    "payin": {
                        "kind": "USD_LEDGER",
                        "amount": "80000.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_ANZ",
                        "paymentDetails": {
                            "accountNumber": "0x9988776655",
                            "reason": "Large unexplained transfer"
                        }
                    },
                    "estimatedSettlementTime": 20
                }
            ]
        },
        "rfq": {
            "metadata": {
                "from": "did:example:user-10010",
                "to": "did:example:pfi-10010"
            },
            "data": {
                "offeringId": "offering-40506",
                "payin": {
                    "kind": "USD_LEDGER",
                    "amount": "80000.00",
                    "paymentDetails": {}
                },
                "payout": {
                    "kind": "BANK_ANZ",
                    "paymentDetails": {
                        "accountNumber": "0x9988776655",
                        "reason": "N/A"
                    }
                },
                "claims": ["signed-credential"]
            }
        },
        "quote": {
            "metadata": {
                "from": "did:example:pfi-10010",
                "to": "did:example:user-10010",
                "exchangeId": "exchange-40506"
            },
            "data": {
                "expiresAt": "2024-06-01T14:00:00Z",
                "payin": {
                    "currencyCode": "USD",
                    "amount": "80000.00"
                },
                "payout": {
                    "currencyCode": "USD",
                    "amount": "79500.00"
                }
            }
        },
        "risk": {
            "expected-score": "high",
            "expected-justification": "High risk due to large unexplained transfer."
        }
    },
    {
        "offering": {
            "id": "offering-30405",
            "currencyPairs": [
                {
                    "pair": "USD/BANK_ANZ",
                    "payin": {
                        "kind": "USD_CASH",
                        "amount": "100.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_ANZ",
                        "paymentDetails": {
                            "accountNumber": "0x8899001122",
                            "reason": "Investment"
                        }
                    },
                    "estimatedSettlementTime": 15
                }
            ]
        },
        "rfq": {
            "metadata": {
                "from": "did:example:user-9009",
                "to": "did:example:pfi-9009"
            },
            "data": {
                "offeringId": "offering-30405",
                "payin": {
                    "kind": "USD_CASH",
                    "amount": "100.00",
                    "paymentDetails": {}
                },
                "payout": {
                    "kind": "BANK_ANZ",
                    "paymentDetails": {
                        "accountNumber": "0x8899001122",
                        "reason": "Investment"
                    }
                },
                "claims": ["signed-credential"]
            }
        },
        "quote": {
            "metadata": {
                "from": "did:example:pfi-9009",
                "to": "did:example:user-9009",
                "exchangeId": "exchange-30405"
            },
            "data": {
                "expiresAt": "2024-06-01T14:00:00Z",
                "payin": {
                    "currencyCode": "USD",
                    "amount": "100.00"
                },
                "payout": {
                    "currencyCode": "USD",
                    "amount": "99.00"
                }
            }
        },
        "risk": {
            "expected-score": "high",
            "expected-justification": "High risk due to withheld information."
        }
    },
    {
        "offering": {
            "id": "offering-20304",
            "currencyPairs": [
                {
                    "pair": "USD/BANK_ANZ",
                    "payin": {
                        "kind": "USD_LEDGER",
                        "amount": "150.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_ANZ",
                        "paymentDetails": {
                            "accountNumber": "0x6677889900",
                            "reason": "Personal expenses"
                        }
                    },
                    "estimatedSettlementTime": 20
                }
            ]
        },
        "rfq": {
            "metadata": {
                "from": "did:example:user-8008",
                "to": "did:example:pfi-8008"
            },
            "data": {
                "offeringId": "offering-20304",
                "payin": {
                    "kind": "USD_LEDGER",
                    "amount": "150.00",
                    "paymentDetails": {}
                },
                "payout": {
                    "kind": "BANK_ANZ",
                    "paymentDetails": {
                        "accountNumber": "0x6677889900",
                        "reason": "Personal expenses"
                    }
                },
                "claims": ["signed-credential"]
            }
        },
        "quote": {
            "metadata": {
                "from": "did:example:pfi-8008",
                "to": "did:example:user-8008",
                "exchangeId": "exchange-20304"
            },
            "data": {
                "expiresAt": "2024-06-01T14:00:00Z",
                "payin": {
                    "currencyCode": "USD",
                    "amount": "150.00"
                },
                "payout": {
                    "currencyCode": "USD",
                    "amount": "148.50"
                }
            }
        },
        "pastExchanges": [
            {
                "rfq": {
                    "metadata": {
                        "from": "did:example:user-8008",
                        "to": "did:example:pfi-8008"
                    },
                    "data": {
                        "offeringId": "offering-20304",
                        "payin": {
                            "kind": "USD_LEDGER",
                            "amount": "200.00",
                            "paymentDetails": {}
                        },
                        "payout": {
                            "kind": "BANK_ANZ",
                            "paymentDetails": {
                                "accountNumber": "0x6677889900",
                                "reason": "Personal expenses"
                            }
                        },
                        "claims": ["signed-credential"]
                    }
                },
                "quote": {
                    "metadata": {
                        "from": "did:example:pfi-8008",
                        "to": "did:example:user-8008",
                        "exchangeId": "exchange-20305"
                    },
                    "data": {
                        "expiresAt": "2024-05-01T14:00:00Z",
                        "payin": {
                            "currencyCode": "USD",
                            "amount": "200.00"
                        },
                        "payout": {
                            "currencyCode": "USD",
                            "amount": "198.00"
                        }
                    }
                },
                "orderStatus": [
                    {
                        "metadata": {
                            "from": "did:example:pfi-8008",
                            "to": "did:example:user-8008",
                            "exchangeId": "exchange-20305"
                        },
                        "data": {
                            "orderStatus": "PROCESSING"
                        }
                    },
                    {
                        "metadata": {
                            "from": "did:example:pfi-8008",
                            "to": "did:example:user-8008",
                            "exchangeId": "exchange-20305"
                        },
                        "data": {
                            "orderStatus": "COMPLETED"
                        }
                    }
                ],
                "close": {
                    "metadata": {
                        "from": "did:example:pfi-8008",
                        "to": "did:example:user-8008",
                        "exchangeId": "exchange-20305"
                    },
                    "data": {
                        "reason": "Order fulfilled",
                        "success": "true"
                    }
                }
            },
            {
                "rfq": {
                    "metadata": {
                        "from": "did:example:user-8008",
                        "to": "did:example:pfi-8008"
                    },
                    "data": {
                        "offeringId": "offering-20304",
                        "payin": {
                            "kind": "USD_LEDGER",
                            "amount": "300.00",
                            "paymentDetails": {}
                        },
                        "payout": {
                            "kind": "BANK_ANZ",
                            "paymentDetails": {
                                "accountNumber": "0x6677889900",
                                "reason": "Personal expenses"
                            }
                        },
                        "claims": ["signed-credential"]
                    }
                },
                "quote": {
                    "metadata": {
                        "from": "did:example:pfi-8008",
                        "to": "did:example:user-8008",
                        "exchangeId": "exchange-20306"
                    },
                    "data": {
                        "expiresAt": "2024-05-10T14:00:00Z",
                        "payin": {
                            "currencyCode": "USD",
                            "amount": "300.00"
                        },
                        "payout": {
                            "currencyCode": "USD",
                            "amount": "297.00"
                        }
                    }
                },
                "orderStatus": [
                    {
                        "metadata": {
                            "from": "did:example:pfi-8008",
                            "to": "did:example:user-8008",
                            "exchangeId": "exchange-20306"
                        },
                        "data": {
                            "orderStatus": "PROCESSING"
                        }
                    },
                    {
                        "metadata": {
                            "from": "did:example:pfi-8008",
                            "to": "did:example:user-8008",
                            "exchangeId": "exchange-20306"
                        },
                        "data": {
                            "orderStatus": "COMPLETED"
                        }
                    }
                ],
                "close": {
                    "metadata": {
                        "from": "did:example:pfi-8008",
                        "to": "did:example:user-8008",
                        "exchangeId": "exchange-20306"
                    },
                    "data": {
                        "reason": "Order fulfilled",
                        "success": "true"
                    }
                }
            }
        ],
        "risk": {
            "expected-score": "high",
            "expected-justification": "High risk due to high transaction volume in a short period."
        }
    },
    {
        "offering": {
            "id": "offering-10203",
            "currencyPairs": [
                {
                    "pair": "USD/BANK_ANZ",
                    "payin": {
                        "kind": "USD_LEDGER",
                        "amount": "3000.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_ANZ",
                    },
                    "estimatedSettlementTime": 30
                }
            ]
        },
        "rfq": {
            "metadata": {
                "from": "did:example:user-7007",
                "to": "did:example:pfi-7007"
            },
            "data": {
                "offeringId": "offering-10203",
                "payin": {
                    "kind": "USD_LEDGER",
                    "amount": "3000.00",
                    "paymentDetails": {}
                },
                "payout": {
                    "kind": "BANK_ANZ",
                    "paymentDetails": {
                        "accountNumber": "0x4455667788",
                        "reason": "Payment for major car servicing"
                    }
                },
                "claims": ["signed-credential"]
            }
        },
        "quote": {
            "metadata": {
                "from": "did:example:pfi-7007",
                "to": "did:example:user-7007",
                "exchangeId": "exchange-10203"
            },
            "data": {
                "expiresAt": "2024-06-01T14:00:00Z",
                "payin": {
                    "currencyCode": "USD",
                    "amount": "3000.00"
                },
                "payout": {
                    "currencyCode": "USD",
                    "amount": "2970.00"
                }
            }
        },
        "risk": {
            "expected-score": "low",
            "expected-justification": "low risk its a car service."
        }
    },
    {
        "offering": {
            "id": "offering-78901",
            "currencyPairs": [
                {
                    "pair": "USD/BANK_ANZ",
                    "payin": {
                        "kind": "USD_LEDGER",
                        "amount": "500.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_ANZ",
                        "paymentDetails": {
                            "accountNumber": "0x2233445566",
                            "reason": "Personal expenses"
                        }
                    },
                    "estimatedSettlementTime": 25
                }
            ]
        },
        "rfq": {
            "metadata": {
                "from": "did:example:user-6006",
                "to": "did:example:pfi-6006"
            },
            "data": {
                "offeringId": "offering-78901",
                "payin": {
                    "kind": "USD_LEDGER",
                    "amount": "500.00",
                    "paymentDetails": {}
                },
                "payout": {
                    "kind": "BANK_ANZ",
                    "paymentDetails": {
                        "accountNumber": "0x2233445566",
                        "reason": "Personal expenses"
                    }
                },
                "claims": ["signed-credential"]
            }
        },
        "quote": {
            "metadata": {
                "from": "did:example:pfi-6006",
                "to": "did:example:user-6006",
                "exchangeId": "exchange-78901"
            },
            "data": {
                "expiresAt": "2024-06-01T14:00:00Z",
                "payin": {
                    "currencyCode": "USD",
                    "amount": "500.00"
                },
                "payout": {
                    "currencyCode": "USD",
                    "amount": "495.00"
                }
            }
        },
        "risk": {
            "expected-score": "low",
            "expected-justification": "No risk detected."
        }
    },
    {
        "offering": {
            "id": "offering-46802",
            "currencyPairs": [
                {
                    "pair": "USD/BANK_ANZ",
                    "payin": {
                        "kind": "USD_LEDGER",
                        "amount": "300.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_ANZ",
                        "paymentDetails": {
                            "accountNumber": "0x6677889900",
                            "reason": "Business payment"
                        }
                    },
                    "estimatedSettlementTime": 20
                }
            ]
        },
        "rfq": {
            "metadata": {
                "from": "did:example:user-5005",
                "to": "did:example:pfi-5005"
            },
            "data": {
                "offeringId": "offering-46802",
                "payin": {
                    "kind": "USD_LEDGER",
                    "amount": "300.00",
                    "paymentDetails": {}
                },
                "payout": {
                    "kind": "BANK_ANZ",
                    "paymentDetails": {
                        "accountNumber": "0x6677889900",
                        "reason": "Business payment"
                    }
                },
                "claims": ["signed-credential"]
            }
        },
        "quote": {
            "metadata": {
                "from": "did:example:pfi-5005",
                "to": "did:example:user-5005",
                "exchangeId": "exchange-46802"
            },
            "data": {
                "expiresAt": "2024-06-01T14:00:00Z",
                "payin": {
                    "currencyCode": "USD",
                    "amount": "300.00"
                },
                "payout": {
                    "currencyCode": "USD",
                    "amount": "297.00"
                }
            }
        },
        "pastExchanges": [
            {
                "rfq": {
                    "metadata": {
                        "from": "did:example:user-5005",
                        "to": "did:example:pfi-5005"
                    },
                    "data": {
                        "offeringId": "offering-46802",
                        "payin": {
                            "kind": "USD_LEDGER",
                            "amount": "300.00",
                            "paymentDetails": {}
                        },
                        "payout": {
                            "kind": "BANK_ANZ",
                            "paymentDetails": {
                                "accountNumber": "0x6677889900",
                                "reason": "Business payment"
                            }
                        },
                        "claims": ["signed-credential"]
                    }
                },
                "quote": {
                    "metadata": {
                        "from": "did:example:pfi-5005",
                        "to": "did:example:user-5005",
                        "exchangeId": "exchange-46803"
                    },
                    "data": {
                        "expiresAt": "2024-05-01T14:00:00Z",
                        "payin": {
                            "currencyCode": "USD",
                            "amount": "300.00"
                        },
                        "payout": {
                            "currencyCode": "USD",
                            "amount": "297.00"
                        }
                    }
                },
                "orderStatus": [
                    {
                        "metadata": {
                            "from": "did:example:pfi-5005",
                            "to": "did:example:user-5005",
                            "exchangeId": "exchange-46803"
                        },
                        "data": {
                            "orderStatus": "PROCESSING"
                        }
                    },
                    {
                        "metadata": {
                            "from": "did:example:pfi-5005",
                            "to": "did:example:user-5005",
                            "exchangeId": "exchange-46803"
                        },
                        "data": {
                            "orderStatus": "COMPLETED"
                        }
                    }
                ],
                "close": {
                    "metadata": {
                        "from": "did:example:pfi-5005",
                        "to": "did:example:user-5005",
                        "exchangeId": "exchange-46803"
                    },
                    "data": {
                        "reason": "Order fulfilled",
                        "success": "true"
                    }
                }
            },
            {
                "rfq": {
                    "metadata": {
                        "from": "did:example:user-5005",
                        "to": "did:example:pfi-5005"
                    },
                    "data": {
                        "offeringId": "offering-46802",
                        "payin": {
                            "kind": "USD_LEDGER",
                            "amount": "300.00",
                            "paymentDetails": {}
                        },
                        "payout": {
                            "kind": "BANK_ANZ",
                            "paymentDetails": {
                                "accountNumber": "0x6677889900",
                                "reason": "Refund request"
                            }
                        },
                        "claims": ["signed-credential"]
                    }
                },
                "quote": {
                    "metadata": {
                        "from": "did:example:pfi-5005",
                        "to": "did:example:user-5005",
                        "exchangeId": "exchange-46804"
                    },
                    "data": {
                        "expiresAt": "2024-05-10T14:00:00Z",
                        "payin": {
                            "currencyCode": "USD",
                            "amount": "300.00"
                        },
                        "payout": {
                            "currencyCode": "USD",
                            "amount": "297.00"
                        }
                    }
                },
                "orderStatus": [
                    {
                        "metadata": {
                            "from": "did:example:pfi-5005",
                            "to": "did:example:user-5005",
                            "exchangeId": "exchange-46804"
                        },
                        "data": {
                            "orderStatus": "PROCESSING"
                        }
                    },
                    {
                        "metadata": {
                            "from": "did:example:pfi-5005",
                            "to": "did:example:user-5005",
                            "exchangeId": "exchange-46804"
                        },
                        "data": {
                            "orderStatus": "COMPLETED"
                        }
                    }
                ],
                "close": {
                    "metadata": {
                        "from": "did:example:pfi-5005",
                        "to": "did:example:user-5005",
                        "exchangeId": "exchange-46804"
                    },
                    "data": {
                        "reason": "Order fulfilled",
                        "success": "true"
                    }
                }
            }
        ],
        "risk": {
            "expected-score": "high",
            "expected-justification": "Risk due to frequent refund requests."
        }
    },
    {
        "offering": {
            "id": "offering-35791",
            "currencyPairs": [
                {
                    "pair": "USD/BANK_ANZ",
                    "payin": {
                        "kind": "USD_CASH",
                        "amount": "150.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_ANZ",
                        "paymentDetails": {
                            "accountNumber": "0x5544332211",
                            "reason": "Business payment"
                        }
                    },
                    "estimatedSettlementTime": 30
                }
            ]
        },
        "rfq": {
            "metadata": {
                "from": "did:example:user-4004",
                "to": "did:example:pfi-4004"
            },
            "data": {
                "offeringId": "offering-35791",
                "payin": {
                    "kind": "USD_CASH",
                    "amount": "150.00",
                    "paymentDetails": {}
                },
                "payout": {
                    "kind": "BANK_ANZ",
                    "paymentDetails": {
                        "accountNumber": "0x5544332211",
                        "reason": "Business payment"
                    }
                },
                "claims": ["signed-credential"]
            }
        },
        "quote": {
            "metadata": {
                "from": "did:example:pfi-4004",
                "to": "did:example:user-4004",
                "exchangeId": "exchange-35791"
            },
            "data": {
                "expiresAt": "2024-06-01T14:00:00Z",
                "payin": {
                    "currencyCode": "USD",
                    "amount": "150.00"
                },
                "payout": {
                    "currencyCode": "USD",
                    "amount": "148.50"
                }
            }
        },
        "pastExchanges": [
            {
                "rfq": {
                    "metadata": {
                        "from": "did:example:user-4004",
                        "to": "did:example:pfi-4004"
                    },
                    "data": {
                        "offeringId": "offering-35791",
                        "payin": {
                            "kind": "USD_CASH",
                            "amount": "200.00",
                            "paymentDetails": {}
                        },
                        "payout": {
                            "kind": "BANK_ANZ",
                            "paymentDetails": {
                                "accountNumber": "0x5544332211",
                                "reason": "Business payment"
                            }
                        },
                        "claims": ["signed-credential"]
                    }
                },
                "quote": {
                    "metadata": {
                        "from": "did:example:pfi-4004",
                        "to": "did:example:user-4004",
                        "exchangeId": "exchange-35792"
                    },
                    "data": {
                        "expiresAt": "2024-05-10T14:00:00Z",
                        "payin": {
                            "currencyCode": "USD",
                            "amount": "200.00"
                        },
                        "payout": {
                            "currencyCode": "USD",
                            "amount": "198.00"
                        }
                    }
                },
                "orderStatus": [
                    {
                        "metadata": {
                            "from": "did:example:pfi-4004",
                            "to": "did:example:user-4004",
                            "exchangeId": "exchange-35792"
                        },
                        "data": {
                            "orderStatus": "PROCESSING"
                        }
                    },
                    {
                        "metadata": {
                            "from": "did:example:pfi-4004",
                            "to": "did:example:user-4004",
                            "exchangeId": "exchange-35792"
                        },
                        "data": {
                            "orderStatus": "COMPLETED"
                        }
                    }
                ],
                "close": {
                    "metadata": {
                        "from": "did:example:pfi-4004",
                        "to": "did:example:user-4004",
                        "exchangeId": "exchange-35792"
                    },
                    "data": {
                        "reason": "Order fulfilled",
                        "success": "true"
                    }
                }
            },
            {
                "rfq": {
                    "metadata": {
                        "from": "did:example:user-4004",
                        "to": "did:example:pfi-4004"
                    },
                    "data": {
                        "offeringId": "offering-35791",
                        "payin": {
                            "kind": "USD_CASH",
                            "amount": "300.00",
                            "paymentDetails": {}
                        },
                        "payout": {
                            "kind": "BANK_ANZ",
                            "paymentDetails": {
                                "accountNumber": "0x5544332211",
                                "reason": "Business payment"
                            }
                        },
                        "claims": ["signed-credential"]
                    }
                },
                "quote": {
                    "metadata": {
                        "from": "did:example:pfi-4004",
                        "to": "did:example:user-4004",
                        "exchangeId": "exchange-35793"
                    },
                    "data": {
                        "expiresAt": "2024-05-20T14:00:00Z",
                        "payin": {
                            "currencyCode": "USD",
                            "amount": "300.00"
                        },
                        "payout": {
                            "currencyCode": "USD",
                            "amount": "297.00"
                        }
                    }
                },
                "orderStatus": [
                    {
                        "metadata": {
                            "from": "did:example:pfi-4004",
                            "to": "did:example:user-4004",
                            "exchangeId": "exchange-35793"
                        },
                        "data": {
                            "orderStatus": "PROCESSING"
                        }
                    },
                    {
                        "metadata": {
                            "from": "did:example:pfi-4004",
                            "to": "did:example:user-4004",
                            "exchangeId": "exchange-35793"
                        },
                        "data": {
                            "orderStatus": "COMPLETED"
                        }
                    }
                ],
                "close": {
                    "metadata": {
                        "from": "did:example:pfi-4004",
                        "to": "did:example:user-4004",
                        "exchangeId": "exchange-35793"
                    },
                    "data": {
                        "reason": "Order fulfilled",
                        "success": "true"
                    }
                }
            }
        ],
        "risk": {
            "expected-score": "high",
            "expected-justification": "High risk due to account age and high transaction volume."
        }
    },
    {
        "offering": {
            "id": "offering-67890",
            "currencyPairs": [
                {
                    "pair": "USD/BANK_ANZ",
                    "payin": {
                        "kind": "USD_LEDGER",
                        "amount": "5000.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_ANZ",
                        "paymentDetails": {
                            "accountNumber": "0x0987654321",
                            "reason": "Gift"
                        }
                    },
                    "estimatedSettlementTime": 15
                }
            ]
        },
        "rfq": {
            "metadata": {
                "from": "did:example:user-2002",
                "to": "did:example:pfi-2002"
            },
            "data": {
                "offeringId": "offering-67890",
                "payin": {
                    "kind": "USD_LEDGER",
                    "amount": "5000.00",
                    "paymentDetails": {}
                },
                "payout": {
                    "kind": "BANK_ANZ",
                    "paymentDetails": {
                        "accountNumber": "0x0987654321",
                        "reason": "Paying for lunch"
                    }
                },
                "claims": ["signed-credential"]
            }
        },
        "quote": {
            "metadata": {
                "from": "did:example:pfi-2002",
                "to": "did:example:user-2002",
                "exchangeId": "exchange-67890"
            },
            "data": {
                "expiresAt": "2024-06-01T14:00:00Z",
                "payin": {
                    "currencyCode": "USD",
                    "amount": "5000.00"
                },
                "payout": {
                    "currencyCode": "USD",
                    "amount": "4950.00"
                }
            }
        },
        "risk": {
            "expected-score": "high",
            "expected-justification": "high risk due to mismatch in amount and reason."
        }
    },
    {
        "offering": {
            "id": "offering-12345",
            "currencyPairs": [
                {
                    "pair": "USD/BANK_ANZ",
                    "payin": {
                        "kind": "USD_LEDGER",
                        "amount": "105000.00",
                        "paymentDetails": {}
                    },
                    "payout": {
                        "kind": "BANK_ANZ",
                        "paymentDetails": {
                            "accountNumber": "0x1234567890",
                            "reason": "Investment"
                        }
                    },
                    "estimatedSettlementTime": 20
                }
            ]
        },
        "rfq": {
            "metadata": {
                "from": "did:example:user-1001",
                "to": "did:example:pfi-1001"
            },
            "data": {
                "offeringId": "offering-12345",
                "payin": {
                    "kind": "USD_LEDGER",
                    "amount": "105000.00",
                    "paymentDetails": {}
                },
                "payout": {
                    "kind": "BANK_ANZ",
                    "paymentDetails": {
                        "accountNumber": "0x1234567890",
                        "reason": "Investment"
                    }
                },
                "claims": ["signed-credential"]
            }
        },
        "quote": {
            "metadata": {
                "from": "did:example:pfi-1001",
                "to": "did:example:user-1001",
                "exchangeId": "exchange-12345"
            },
            "data": {
                "expiresAt": "2024-06-01T14:00:00Z",
                "payin": {
                    "currencyCode": "USD",
                    "amount": "105000.00"
                },
                "payout": {
                    "currencyCode": "USD",
                    "amount": "104500.00"
                }
            }
        },
        "risk": {
            "expected-score": "high",
            "expected-justification": "High risk due to withheld information and large amount."
        }
    }
]

import requests
import pandas as pd
from tabulate import tabulate

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