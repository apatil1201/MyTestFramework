from flask import Flask, request, jsonify
from flask_cors import CORS
import re
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)  # allow all origins for local dev

# In-memory DB
users = {}
transactions = {}
user_counter = 1
transaction_counter = 1

VALID_TOKEN = "Bearer testtoken"

# -----------------------
# Auth check
# -----------------------


@app.before_request
def require_auth():
    if request.path.startswith("/api/"):
        if request.method == "OPTIONS":
            return None  # CORS preflight handled automatically
        auth = request.headers.get("Authorization")
        if auth != VALID_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401

# -----------------------
# USERS
# -----------------------


@app.route("/api/users", methods=["POST", "OPTIONS"])
def create_user():
    if request.method == "OPTIONS":
        # Respond to preflight
        return '', 200
    global user_counter
    data = request.json
    if not data.get("name") or not data.get("email") or not data.get("accountType"):
        return jsonify({"error": "Invalid user data"}), 400
    if not re.match(r'(^[\w\.-]+)@([\w\.-]+\.\w{2,4}$)', data.get("email")):
        return jsonify({'error': "Invalid email format"}), 400
    if not re.match(r'(premium|basic)', data.get("accountType")):
        return jsonify({'error': "Invalid account Type"}), 400
    user_id = str(user_counter)
    user_counter += 1
    users[user_id] = {**data, "id": user_id}
    return jsonify(users[user_id]), 201


@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users[user_id]), 200


@app.route("/api/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    users[user_id].update(data)  # merge changes
    return jsonify(users[user_id]), 200


@app.route("/api/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    deleted = users.pop(user_id)
    return jsonify({"message": "User deleted", "user": deleted}), 200

# -----------------------
# TRANSACTIONS
# -----------------------


@app.route("/api/transactions", methods=["POST"])
def create_transaction():
    global transaction_counter
    data = request.json
    if not data.get("userId") or not data.get("amount") or not data.get("type"):
        return jsonify({"error": "Invalid transaction data"}), 400
    if float(data.get("amount")) < 0:
        return jsonify({"error": "Invalid Amount - cannot be negative"}), 400

    txn_id = str(transaction_counter)
    transaction_counter += 1
    transactions[txn_id] = {**data, "id": txn_id}
    return jsonify(transactions[txn_id]), 201


@app.route("/api/transactions/<user_id>", methods=["GET"])
def get_transactions(user_id, txn_id=None):
    user_txns = [txn for txn in transactions.values() if txn["userId"] == user_id]
    if not user_txns:
        return jsonify({"error": "Transaction not found for user"}), 404
    return jsonify(user_txns), 200


@app.route("/api/transactions/<txn_id>", methods=["PUT"])
def update_transaction(txn_id):
    if txn_id not in transactions:
        return jsonify({"error": "Transaction not found"}), 404
    data = request.json
    if float(data.get("amount")) < 0:
        return jsonify({"error": "Invalid Amount - Cannot be negative"}), 400
    transactions[txn_id].update(data)
    return jsonify(transactions[txn_id]), 200


@app.route("/api/transactions/<txn_id>", methods=["DELETE"])
def delete_transaction(txn_id):
    if txn_id not in transactions:
        return jsonify({"error": "Transaction not found"}), 404

    deleted = transactions.pop(txn_id)
    return jsonify({"message": "Transaction deleted", "transaction": deleted}), 200

if __name__ == "__main__":
    app.run(port=5000)