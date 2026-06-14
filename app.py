from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

USER = {"admin": "admin123"}

results = {}

class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Text)


@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("upload"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USER and USER[username] == password:
            session["user"] = username
            return redirect(url_for("upload"))
        return "Invalid login!"

    return render_template("login.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    global results

    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        file = request.files["file"]
        content = file.read().decode("utf-8")

        from mapreduce import run_mapreduce
        results = run_mapreduce(content)

        saved = AnalysisResult(result=str(results))
        db.session.add(saved)
        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template("upload.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", results=results)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
