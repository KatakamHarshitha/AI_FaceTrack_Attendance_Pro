from flask import Flask, render_template, request, jsonify
from datetime import datetime
from database import db, User, Attendance

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
@app.route("/api/attendance/<int:user_id>", methods=["POST"])
def mark_attendance(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    now = datetime.now()

    attendance = Attendance(
        user_id=user.id,
        date=now.strftime("%Y-%m-%d"),
        time=now.strftime("%H:%M:%S")
    )

    db.session.add(attendance)
    db.session.commit()

    return jsonify({
        "message": "Attendance marked successfully",
        "user_id": user.id,
        "name": user.name,
        "date": attendance.date,
        "time": attendance.time
    }), 201
@app.route("/api/attendance", methods=["GET"])
def get_attendance():
    records = Attendance.query.all()

    return jsonify([
        {
            "id": record.id,
            "user_id": record.user_id,
            "date": record.date,
            "time": record.time
        }
        for record in records
    ])

if __name__ == "__main__":
    app.run(debug=True)