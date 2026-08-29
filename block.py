import hashlib
import time


class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = (
            str(self.index)
            + str(self.timestamp)
            + str(self.transactions)
            + str(self.previous_hash)
            + str(self.nonce)
        )

        return hashlib.sha256(data.encode()).hexdigest()


# Test block
if __name__ == "__main__":
    genesis_block = Block(
        0,
        ["Genesis Transaction"],
        "0"
    )

    print("Block Hash:", genesis_block.hash)