from flask import Flask, jsonify, request
import hashlib
import json
import time
import requests
from ecdsa import SigningKey, SECP256k1, VerifyingKey, BadSignatureError

app = Flask(__name__)

# --- CORE MAINNET STORAGE & CONFIGURATION (NO DATA DELETED, FULLY EXPANDED) ---
blockchain = []
difficulty = 4  # D4 dynamic proof standard prefix zeroes
balances = {"owner_address": 1000}  # Initialized core ledger registry
pending_transactions = []
peers = set()  # P2P Network Distributed Peer Nodes Registry

class Transaction:
    def __init__(self, sender, receiver, amount, signature=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature

    def to_dict(self):
        return {"sender": self.sender, "receiver": self.receiver, "amount": self.amount}

    def calculate_hash(self):
        tx_string = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def verify_signature(self):
        if self.sender == "MINING_REWARD":
            return True
        if not self.signature:
            return False
        try:
            pub_key = VerifyingKey.from_string(bytes.fromhex(self.sender), curve=SECP256k1)
            return pub_key.verify(bytes.fromhex(self.signature), self.calculate_hash().encode())
        except (ValueError, BadSignatureError):
            return False

def calculate_hash(index, previous_hash, timestamp, nonce, transactions_data):
    value = f"{index}{previous_hash}{timestamp}{nonce}{json.dumps(transactions_data, sort_keys=True)}"
    return hashlib.sha256(value.encode()).hexdigest()

def create_genesis_block():
    if len(blockchain) == 0:
        genesis_hash = calculate_hash(0, "0"*64, 1234567890, 0, [])
        block = {
            "index": 0,
            "previous_hash": "0"*64,
            "timestamp": 1234567890,
            "nonce": 0,
            "hash": genesis_hash,
            "transactions": [],
            "miner": "Genesis Network Engine",
            "reward_distribution": "25 Miner / 25 Owner standard locked split ready"
        }
        blockchain.append(block)

# Genesis initial configuration bootup
create_genesis_block()

# --- BULLETPROOF CHAIN VALIDATION ENGINE (ANTI-TAMPER LAYER) ---
def is_chain_valid(chain_to_validate):
    for i in range(1, len(chain_to_validate)):
        current = chain_to_validate[i]
        previous = chain_to_validate[i-1]
        
        # 1. Structure Hash Audit
        tx_data = current.get("transactions", [])
        if current["hash"] != calculate_hash(current["index"], current["previous_hash"], current["timestamp"], current["nonce"], tx_data):
            print("[CRITICAL] Block hash manipulation detected!")
            return False
            
        # 2. Blockchain Link Audit
        if current["previous_hash"] != previous["hash"]:
            print("[CRITICAL] Blockchain break tracking exception found!")
            return False
            
        # 3. Difficulty Proof Audit
        if not current["hash"].startswith("0" * difficulty):
            print("[CRITICAL] Illegal PoW calculation verification bypass failed!")
            return False
    return True

# --- AUTOMATED P2P SYNC PROTOCOL (CONSENSUS MECHANISM) ---
def consensus():
    global blockchain
    longest_chain = None
    max_length = len(blockchain)
    
    for peer in peers:
        try:
            response = requests.get(f"http://{peer}/chain", timeout=3)
            if response.status_code == 200:
                data = response.get_json()
                length = data["length"]
                chain = data["chain"]
                
                if length > max_length and is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        except Exception:
            continue
            
    if longest_chain:
        blockchain = longest_chain
        print("[P2P Sync] Blockchain updated dynamically to the longest valid chain across peers.")
        return True
    return False

# --- ORIGINAL CORE ENDPOINTS (PRESERVED & STABILIZED) ---
@app.route('/get_work', methods=['GET'])
def get_work():
    last_block = blockchain[-1]
    job_data = {
        "block_index": last_block["index"] + 1,
        "previous_hash": last_block["hash"],
        "difficulty": difficulty,
        "pending_transactions_count": len(pending_transactions)
    }
    return jsonify(job_data), 200

@app.route('/submit_work', methods=['POST'])
def submit_work():
    global pending_transactions
    miner_data = request.get_json() or {}
    index = miner_data.get('index', len(blockchain))
    previous_hash = miner_data.get('previous_hash', blockchain[-1]["hash"])
    nonce = miner_data.get('nonce')
    miner_address = miner_data.get('miner_address', 'anonymous_miner')
    timestamp = miner_data.get('timestamp', int(time.time()))
    
    current_tx_snapshot = list(pending_transactions)
    computed_hash = calculate_hash(index, previous_hash, timestamp, nonce, current_tx_snapshot)
    
    if computed_hash.startswith("0" * difficulty):
        # Bulletproof Reward Split Rule: 25 Miner / 25 Owner system triggered
        if miner_address not in balances:
            balances[miner_address] = 0
        balances[miner_address] += 25
        balances["owner_address"] += 25
        
        new_block = {
            "index": index,
            "previous_hash": previous_hash,
            "timestamp": timestamp,
            "nonce": nonce,
            "hash": computed_hash,
            "transactions": current_tx_snapshot,
            "miner": miner_address,
            "reward": "50/50 Block Split (25 to Miner, 25 to Owner) applied cleanly"
        }
        
        blockchain.append(new_block)
        pending_transactions = []  # Empty local mempool post confirmation
        
        # Broadcast block details to all connected decentralized nodes
        for peer in peers:
            try:
                requests.post(f"http://{peer}/receive_block", json={"block": new_block}, timeout=2)
            except Exception:
                continue
                
        return jsonify({"status": "success", "message": "Block confirmed on Bitcoin-DNA!", "hash": computed_hash}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid proof-of-work solution rejected."}), 400

@app.route('/chain', methods=['GET'])
def get_chain():
    consensus()  # Automatic P2P auto check before loading data
    return jsonify({
        "chain": blockchain,
        "length": len(blockchain),
        "balances": balances,
        "pending_transactions": pending_transactions
    }), 200

# --- NEW P2P ENDPOINTS FOR AUTO DECENTRALIZATION ---
@app.route('/register_node', methods=['POST'])
def register_node():
    node_data = request.get_json()
    node_address = node_data.get("node_address") # Format: "IP:PORT"
    if node_address:
        peers.add(node_address)
        return jsonify({"status": "success", "total_peers": list(peers)}), 200
    return jsonify({"status": "error", "message": "Invalid node format."}), 400

@app.route('/receive_block', methods=['POST'])
def receive_block():
    block_data = request.get_json().get("block")
    if block_data and block_data["previous_hash"] == blockchain[-1]["hash"]:
        if block_data["hash"].startswith("0" * difficulty):
            blockchain.append(block_data)
            return jsonify({"status": "accepted", "message": "Block synced smoothly via P2P"}), 200
    return jsonify({"status": "rejected", "message": "Stale or invalid block structure reference."}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

