
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "mysecretkey"
#----- Create database + table ------
def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (name, username, password, role) VALUES (?, ?, ?, ?)",
            (name, username, password, role)
        )

        conn.commit()
        conn.close()

        return "Registered Successfully"

    return render_template("register.html")
    


   
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = user[2]      # username column
            session["name"] = user[1]      # name column
            session["role"] = user[4]      # role column

            return redirect("/dashboard")

            # SAFE ROLE HANDLING
            if len(user) >= 5:
                session["role"] = user[4]
            else:
                session["role"] = "User"

            return redirect("/dashboard")

        return "Invalid Login ❌"

    return render_template("login.html")



@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    role = session.get("role", "User")  # SAFE ACCESS

    return render_template(
        "dashboard.html",
        user=session["user"],
        role=role
    )
        
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))




@app.route("/profile")
def profile():

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT name, username, role FROM users WHERE username=?",
        (session["user"],)
    )

    user = cur.fetchone()

    conn.close()

    return render_template(
        "profile.html",
        name=user[0],
        username=user[1],
        role=user[2]
    )

#-----run---------------
if __name__ == "__main__":
    app.run(debug=True)
