from blockchain import Blockchain


def main():

    # Create a new blockchain
    blockchain = Blockchain()

    # Add the first block
    blockchain.add_block(
        [
            "Alice sends 50 BTC to Bob"
        ]
    )

    # Add the second block
    blockchain.add_block(
        [
            "Bob sends 25 BTC to Charlie"
        ]
    )

    # Print the blockchain
    print("\n===== BITCOIN-DNA BLOCKCHAIN =====\n")

    for block in blockchain.chain:
        print(f"Block #{block.index}")
        print("Transactions:", block.transactions)
        print("Previous Hash:", block.previous_hash)
        print("Hash:", block.hash)
        print("-" * 50)


if __name__ == "__main__":
    main()