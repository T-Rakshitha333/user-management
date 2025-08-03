from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

# Database connection (single thread-safe connection for demo purposes)
database_path = 'users.db'
connection = sqlite3.connect(database_path, check_same_thread=False)
db = connection.cursor()

# Helper to hash passwords
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def health_check():
    return jsonify({"message": "User Management System is running"}), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        db.execute("SELECT id, name, email FROM users")
        all_users = db.fetchall()
        return jsonify({"users": all_users}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    db.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    user = db.fetchone()
    if user:
        return jsonify({"user": user}), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_new_user():
    user_data = request.get_json()
    name = user_data.get('name')
    email = user_data.get('email')
    password = user_data.get('password')

    if not all([name, email, password]):
        return jsonify({"error": "Name, email, and password are required"}), 400

    try:
        hashed_password = hash_password(password)
        db.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_password)
        )
        connection.commit()
        return jsonify({"message": f"User '{name}' created successfully"}), 201
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    user_data = request.get_json()
    name = user_data.get('name')
    email = user_data.get('email')

    if not all([name, email]):
        return jsonify({"error": "Name and email are required for update"}), 400

    db.execute(
        "UPDATE users SET name = ?, email = ? WHERE id = ?",
        (name, email, user_id)
    )
    connection.commit()

    if db.rowcount == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User updated successfully"}), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    connection.commit()

    if db.rowcount == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": f"User with ID {user_id} deleted"}), 200

@app.route('/search', methods=['GET'])
def search_users_by_name():
    search_name = request.args.get('name')
    if not search_name:
        return jsonify({"error": "Please provide a name to search"}), 400

    db.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{search_name}%",))
    matched_users = db.fetchall()
    return jsonify({"results": matched_users}), 200

@app.route('/login', methods=['POST'])
def user_login():
    login_data = request.get_json()
    email = login_data.get('email')
    password = login_data.get('password')

    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400

    hashed_password = hash_password(password)

    db.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, hashed_password))
    user = db.fetchone()

    if user:
        return jsonify({"status": "success", "user_id": user[0]}), 200
    return jsonify({"status": "failed", "error": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
