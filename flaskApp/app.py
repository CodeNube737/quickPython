# app.py
# description: Flask profile app for Lab 5

from flask import Flask, session, redirect, render_template, request, jsonify

app = Flask(__name__)
app.secret_key = "dev"

profiles = {}

# -----------------------------
# Helper functions
# -----------------------------

def get_current_user():
    return session.get("username")

def validate_profile_data(first_name, last_name, student_id):
    if not first_name or not last_name or not student_id:
        return "All fields are required."
    if not student_id.isnumeric():
        return "Student ID must be numeric."
    return None

def normalize_profile_data(first_name, last_name, student_id):
    return {
        "first_name": first_name.strip(),
        "last_name": last_name.strip(),
        "student_id": str(student_id).strip()
    }

# -----------------------------
# TEMP LOGIN ROUTE (for testing)
# -----------------------------
@app.route("/login")
def login():
    session["username"] = "student"   # fake login
    return redirect("/profile")

# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    username = get_current_user()
    if not username:
        return redirect("/")

    if request.method == "GET":
        user_profile = profiles.get(username)
        return render_template("profile.html", profile=user_profile)

    # POST
    first = request.form.get("first_name")
    last = request.form.get("last_name")
    sid = request.form.get("student_id")

    error = validate_profile_data(first, last, sid)
    if error:
        return render_template(
            "profile.html",
            error=error,
            profile={"first_name": first, "last_name": last, "student_id": sid}
        )

    cleaned = normalize_profile_data(first, last, sid)
    profiles[username] = cleaned

    return redirect("/")

# -----------------------------
# Run the app
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
