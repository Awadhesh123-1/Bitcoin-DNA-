import os
import json
import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1

WALLET_FILE = "wallet.json"


class Wallet:

    def __init__(self):
        self.balance = 0

        if os.path.exists(WALLET_FILE):
            self.load_wallet()
        else:
            self.create_wallet()

    def create_wallet(self):
        # Private Key
        private_key = SigningKey.generate(curve=SECP256k1)
        self.private_key = private_key.to_string().hex()

        # Public Key
        public_key = private_key.get_verifying_key()
        self.public_key = public_key.to_string().hex()

        # BTC-DNA Address
        public_key_hash = hashlib.sha256(
            bytes.fromhex(self.public_key)
        ).hexdigest()

        self.address = "BDNA" + public_key_hash[:40]

        self.save_wallet()

    def save_wallet(self):
        data = {
            "private_key": self.private_key,
            "public_key": self.public_key,
            "address": self.address,
            "balance": self.balance
        }

        with open(WALLET_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def load_wallet(self):
        with open(WALLET_FILE, "r") as file:
            data = json.load(file)

        self.private_key = data["private_key"]
        self.public_key = data["public_key"]
        self.address = data["address"]
        self.balance = data.get("balance", 0)

    def show_wallet(self):
        print("\n===== BTC-DNA WALLET =====")
        print("Address    :", self.address)
        print("Balance    :", self.balance, "BTC-DNA")
        print("Public Key :", self.public_key)
        print("Private Key: [SECRET]")
        print("==========================")

    def deposit(self, amount):
        if amount <= 0:
            return False

        self.balance += amount
        self.save_wallet()
        return True

    def spend(self, amount):
        if amount <= 0 or amount > self.balance:
            return False

        self.balance -= amount
        self.save_wallet()
        return True

    def sign_transaction(self,
   transaction):
        if isinstance(transaction, dict):
            transaction_data = json.dumps(
                transaction,
                sort_keys=True,
                separators=(",", ":")
            )
        else:
            transaction_data = str(transaction)

        private_key = SigningKey.from_string(
            bytes.fromhex(self.private_key),
            curve=SECP256k1
        )

        signature = private_key.sign_deterministic(
            transaction_data.encode(),
            hashfunc=hashlib.sha256
        )
        return signature.hex()

    def verify_signature(self, transaction, signature, public_key):
        if not isinstance(transaction, dict):
            return False

        if not isinstance(signature, str):
            return False

        if not isinstance(public_key, str):
            return False

        try:
            transaction_data = json.dumps(
                transaction,
                sort_keys=True,
                separators=(",", ":")
            )

            verifying_key = VerifyingKey.from_string(
                bytes.fromhex(public_key),
                curve=SECP256k1
            )

            return verifying_key.verify(
                bytes.fromhex(signature),
                transaction_data.encode(),
                hashfunc=hashlib.sha256
            )

        except Exception:
            return False
        return False
