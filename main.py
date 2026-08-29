from blockchain import Blockchain
from transaction import Transaction


blockchain = Blockchain()

transaction1 = Transaction(
    "Alice",
    "Bob",
    50
)

transaction2 = Transaction(
    "Bob",
    "Charlie",
    25
)

blockchain.add_block([
    transaction1,
    transaction2
])

print("Blockchain valid:", blockchain.is_chain_valid())

print("\nNumber of blocks:")
print(len(blockchain.chain))

for block in blockchain.chain:
    print("\n-------------------")
    print(block)