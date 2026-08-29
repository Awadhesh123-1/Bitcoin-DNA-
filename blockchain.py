from block import Block


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(
            0,
            ["Genesis Block"],
            "0"
        )

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        previous_block = self.get_latest_block()

        new_block = Block(
            len(self.chain),
            transactions,
            previous_block.hash
        )

        self.chain.append(new_block)


if __name__ == "__main__":
    blockchain = Blockchain()

    blockchain.add_block(
        ["Alice sends 10 BTC to Bob"]
    )

    for block in blockchain.chain:
        print("Block:", block.index)
        print("Hash:", block.hash)
        print("Previous Hash:", block.previous_hash)
        print()