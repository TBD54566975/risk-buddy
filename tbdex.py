TBDEX_PROTOCOL_DESCRIPTION = """
tbDEX Protocol

Introduction:
tbDEX is a protocol for discovering liquidity and exchanging assets such as fiat money, real-world goods, stablecoins, or bitcoin. 
It uses Decentralized Identifiers (DIDs) and Verifiable Credentials (VCs) to establish the provenance of identity in the real world. 
The protocol does not enforce anonymity but allows counterparties to negotiate the minimum information required for an exchange. 
This specification defines the message and resource formats of the tbDEX messaging protocol, composed of Resources and Messages.



Fields:

metadata: An object containing fields about the resource.
data: The actual resource content (e.g., an offering).
signature: Signature that verifies the authenticity and integrity of the resource.

metadata:
from: The author's DID.
kind: The type of data property (e.g., offering).
id: The resource's ID.
createdAt: ISO 8601 timestamp.
updatedAt: ISO 8601 timestamp.
protocol: Version of the protocol in use (x.x format). Protocol versions must remain consistent across messages in an exchange.

data: The actual resource content, always a JSON object. The content for each resource type is specified in the Resource Kinds section.

signature: See the Signatures section for more details.

Resource Kinds:

Offering:
description: Brief description of the offering.
payoutUnitsPerPayinUnit: Number of payout units received for 1 payin unit.
payin: Details and options for the payin currency.
payout: Details and options for the payout currency.
requiredClaims: Claims required when submitting an RFQ for this offering.

PayinDetails:
currencyCode: ISO 4217 currency code.
min: Minimum amount for the offer.
max: Maximum amount for the offer.
methods: List of payment methods.

PayoutDetails:
currencyCode: ISO 4217 currency code.
min: Minimum amount for the offer.
max: Maximum amount for the offer.
methods: List of payment methods.

PayinMethod:
kind: Unique identifier for the payment method (e.g., DEBIT_CARD, BITCOIN_ADDRESS).
name: Payment method name.
description: Information about the payment method.
group: Category of the payment method.
requiredPaymentDetails: JSON Schema for fields needed to use this payment method.
fee: Fee for using this payment method.
min: Minimum amount for using this payment method.
max: Maximum amount for using this payment method.

Important Notes:
kind should be unique.
min or max in a payment method takes precedence over min or max defined at the PaymentDetails level.
If requiredPaymentDetails is omitted, RFQs must also omit paymentDetails.

PayoutMethod:
kind: Unique identifier for the payment method (e.g., DEBIT_CARD, BITCOIN_ADDRESS).
estimatedSettlementTime: Estimated time to settle an order, in seconds.
name: Payment method name.
description: Information about the payment method.
group: Category of the payment method.
requiredPaymentDetails: JSON Schema for fields needed to use this payment method.
fee: Fee for using this payment method.
min: Minimum amount for using this payment method.
max: Maximum amount for using this payment method.

Important Notes:
estimatedSettlementTime provides an estimate of the latency between receiving a payin and the payout landing.

Reserved PaymentMethod Kinds:
Some payment methods should be consistent across PFIs and have reserved kind values. PFIs may provide stored balances, custodying assets or funds on behalf of their customers.

Example Offering: A JSON example of an offering is provided.

Balance:
currencyCode: ISO 4217 currency code.
available: Amount available to be transacted with.

Example Balance: A JSON example of a balance is provided.

Reputation: A set of Verifiable Credentials issued to the PFI to assess its reputability. (TODO: Fill out)

Messages:
Messages form exchanges between Alice and a PFI.

Fields:
All tbDEX messages are JSON objects with the following properties:

metadata: An object containing fields about the message.
data: The actual message content.
signature: Signature that verifies the authenticity and integrity of the message.
private: Ephemeral JSON object for sensitive data (e.g., PII).

metadata:
from: The sender's DID.
to: The recipient's DID.
kind: The type of data property (e.g., rfq, quote).
id: The message's ID.
exchangeId: ID for an exchange of messages between Alice and PFI.
externalId: Arbitrary ID for the caller to associate with the message.
createdAt: ISO 8601 timestamp.
protocol: Version of the protocol in use (x.x format). Protocol versions must remain consistent across messages in an exchange.

data: The actual message content, always a JSON object. The content for each message type is specified in the Message Kinds section.

privateData:
salt: Randomly generated salt.
claims: Array of claims.
payin: Container for unhashed payin payment details.
payout: Container for unhashed payout payment details.

PrivatePaymentDetails:
paymentDetails: Object containing properties defined in an Offering's requiredPaymentDetails schema.

RFQ example: A JSON example of an RFQ message is provided.

Close:
reason: Explanation for closing the exchange.
success: Indicates whether the exchange was successful.

Example Close: A JSON example of a Close message is provided.

Quote:
expiresAt: When the quote expires.
payin: Amount of payin currency received by the PFI.
payout: Amount of payout currency received by Alice.

QuoteDetails:
currencyCode: ISO 4217 currency code.
amount: Amount of currency excluding fees.
fee: Amount paid in fees.
paymentInstruction: Instructions for paying the PFI and getting paid by the PFI.

PaymentInstruction:
link: Link to allow Alice to pay PFI, or be paid by the PFI.
instruction: Instruction on how Alice can pay PFI, or how Alice can be paid by the PFI.
"""

TBDEX_JARGON = """
Some jargon:

Term->Definition
PFI	Partipating Financial Institution: typically this is some kind of company that allows you to obtain a specified currency in exchange for another (e.g. BTC -> KES)
KYC	Know Your Customer: requirements that financial institutions know who their customer is for legal and compliance reasons.
payin	a method/technology used by the sender to transmit funds to the PFI.
payout	a method/technology used by the PFI to transmit funds to the recipient. e.g. Mobile Money
payout currency	currency that the PFI is paying out to Alice. Alice will receive the payout currency from the PFI.
payin currency	currency the PFI will accept in exchange for the payin currency. The PFI will receive the payin currency from Alice.
"""
