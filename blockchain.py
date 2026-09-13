import hashlib
import time
from wallet import Wallet


class Block:

    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()

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

    def mine_block(self, difficulty):

        target = "0" * difficulty

        print(f"Mining Block #{self.index}...")

        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

        print("Block mined!")
        print("Hash:", self.hash)
        print("Nonce:", self.nonce)


class Blockchain:

    MINING_REWARD = 50

    def __init__(self):
        self.chain = []
        self.difficulty = 4

        genesis_block = Block(
            0,
            ["Genesis Block"],
            "0"
        )

        genesis_block.mine_block(self.difficulty)

        self.chain.append(genesis_block)

    def add_block(self, transactions, miner_address, owner_address):

        if not self.validate_transactions(transactions):
            print("Invalid transaction. Block rejected.")
        return False

        previous_block = self.chain[-1]

        miner_reward_tx = {
        "sender": "SYSTEM",
        "receiver": miner_address,
        "amount": self.MINING_REWARD // 2
        }

        owner_reward_tx = {
        "sender": "SYSTEM",
        "receiver": owner_address,
        "amount": self.MINING_REWARD // 2
        }

        block_transactions = transactions + [
        miner_reward_tx,
        owner_reward_tx
        ]


        new_block = Block(
        len(self.chain),
        block_transactions,
        previous_block.hash
        )

        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

        return True

    def validate_transactions(self, transactions):
        wallet = Wallet()

        for tx in transactions:
            if not isinstance(tx, dict):
                return False

            if "signature" not in tx or "public_key" not in tx:
                return False

            signature = tx["signature"]
            public_key = tx["public_key"]

            original_tx = {
            key: value
            for key, value in tx.items()
            if key not in ("signature", "public_key")
            }

            if not wallet.verify_signature(
                original_tx,
                signature,
                public_key
            ):
                return False

        return True

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

            if not current_block.hash.startswith("0" * self.difficulty):
                return False

            reward_transactions = [
                tx for tx in current_block.transactions
                if isinstance(tx, dict)
                and tx.get("sender") == "SYSTEM"
            ]

            if len(reward_transactions) != 2:
                return False

                total_reward = 0

            for reward_tx in reward_transactions:

            if reward_tx.get("receiver") is None:
                return False

            if reward_tx.get("amount") is None:
                return False

            if reward_tx.get("amount") != self.MINING_REWARD // 2:
                return False

                total_reward += reward_tx.get("amount")

if total_reward != self.MINING_REWARD:
    return False

    def get_balance(self, address):
        balance = 0

        for block in self.chain:
            for tx in block.transactions:
                if not isinstance(tx, dict):
                    continue

                if tx.get("receiver") == address:
                    balance += tx.get("amount", 0)

                if tx.get("sender") == address:
                    balance -= tx.get("amount", 0)

        return balance

