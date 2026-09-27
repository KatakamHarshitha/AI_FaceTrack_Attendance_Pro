from flask import Flask, render_template, request, jsonify
from database import db,User

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///attendance.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    user = User(name=name, email=email)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "id": user.id,
        "name": user.name,
        "email": user.email
    }), 201

@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()

    return jsonify([
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in users
    ])

if __name__ == "__main__":
    app.run(debug=True)