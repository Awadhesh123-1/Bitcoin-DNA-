from wallet import Wallet
from blockchain import Blockchain


# Create wallet
wallet = Wallet()
owner_wallet = Wallet()
# Create blockchain
blockchain = Blockchain()


# Create transaction
transaction = {
    "from": wallet.address,
    "to": "TEST_ADDRESS",
    "amount": 10
}


# Sign transaction
signature = wallet.sign_transaction(transaction)


# Attach signature and public key
signed_transaction = {
    **transaction,
    "public_key": wallet.public_key,
    "signature": signature
}
# Verify signature
is_valid_signature = wallet.verify_signature(
    transaction,
    signature,
    wallet.public_key
)

print("Signature Valid :", is_valid_signature)

if not is_valid_signature:
    print("ERROR: Invalid transaction signature")
    exit()

print("\n===== TRANSACTION =====")
print("From      :", wallet.address)
print("To        :", transaction["to"])
print("Amount    :", transaction["amount"])
print("Signed    :", bool(signature))


# Add signed transaction to blockchain
block_added = blockchain.add_block(
    [signed_transaction],
    wallet.public_key,
    owner_wallet.address
)

print("Block Added :", block_added)

print("\n===== REWARD TRANSACTIONS =====")

latest_block = blockchain.chain[-1]

for tx in latest_block.transactions:
    if not isinstance(tx, dict):
        continue

    if tx.get("sender") == "SYSTEM":
        print("Sender :", tx.get("sender"))
        print("Receiver :", tx.get("receiver"))
        print("Amount :", tx.get("amount"))
        print("----------------")

print("\n===== BLOCKCHAIN =====")
print("Blocks    :", len(blockchain.chain))
print("Valid     :", blockchain.is_chain_valid())
