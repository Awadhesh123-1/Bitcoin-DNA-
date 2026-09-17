from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Jingle Miner ko Mining Job dene ka Endpoint
@app.route('/get_work', methods=['GET'])
def get_work():
    # Hardcoded/Fallback Job details aapke custom coin ke liye
    job_data = {
        "block_index": 1,
        "previous_hash": "00000000000000000000000000000000",
        "difficulty": 4
    }
    return jsonify(job_data), 200

# Hardware jab Nonce solve kar lega toh data yahan bhejega
@app.route('/submit_work', methods=['POST'])
def submit_work():
    miner_data = request.get_json()
    nonce = miner_data.get('nonce')
    print(f"[!] Jingle Miner found a block! Nonce received: {nonce}")
    return jsonify({"status": "success", "message": "Block confirmed on Bitcoin-DNA!"}), 200

if __name__ == '__main__':
    # Server ko Hotspot network par live karna (Port 8080)
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

