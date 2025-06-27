from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///genetic_analysis.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid request"}), 400
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if username is None or email is None or password is None:
        return jsonify({"error": "Missing required fields"}), 400
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
