from flask import Flask,render_template,redirect,url_for,request,session,flash
import sqlite3
from datetime import datetime

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
            session["user_id"] = user[0] 
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

@app.route("/dashboard",methods=['GET'])
def dashboard():
    if "user" not in session:
        return redirect("/login")
    role = session.get("role", "User")  # SAFE ACCESS
    
    user_id = session["user_id"]

    conn = sqlite3.connect("resources.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT id,resource_name, category, quantity, expiry_date
        FROM resources
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))
    donations = cur.fetchall()

    cur.execute("""
        SELECT id,resource_name, category, quantity, expiry_date
        FROM resources
        WHERE expiry_date >= DATE('now')
            OR expiry_date = ''
            OR expiry_date IS NULL
                """)
    allresources = cur.fetchall()
    conn.close()
    search_query = request.args.get('search', '').strip()
    # Filter resources if a search query exists
    if search_query:
        resources = [
            r for r in allresources 
            if search_query.lower() in r[1].lower() or search_query.lower() in r[2].lower()
        ]
    else:
        resources = allresources

    return render_template(
        "dashboard.html",
        user=session["user"],
        role=role,
        donations=donations,
        resources=resources,
        search_query=search_query
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


#table for adding resources
conn = sqlite3.connect('resources.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS resources (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             user_id INTEGER,
             resource_name TEXT,
             category TEXT,
             quantity INTEGER,
             expiry_date TEXT,
             FOREIGN KEY(user_id) REFERENCES users(id)
             )
'''
)
conn.close()

@app.route('/add_resource')
def add_resource():
    return render_template("add_resource.html")

#saving resources
@app.route("/submit_resource", methods=["POST"])
def submit_resource():
    if 'user_id' not in session:
        return redirect('/login') 
    user_id = session["user_id"]
    resource_name = request.form["resource_name"]
    category = request.form["category"]
    quantity = request.form["quantity"]
    expiry_date = request.form["expiry_date"]

    conn = sqlite3.connect("resources.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO resources
        (user_id, resource_name, category, quantity, expiry_date)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, resource_name, category, quantity, expiry_date))

    conn.commit()
    conn.close()

    flash("Thank you for your donation!Your contribution is now available to help someone in need.")

    return redirect('/dashboard')

@app.route('/delete_resource/<int:resource_id>', methods=['POST'])
def delete_resource(resource_id):
    conn = sqlite3.connect("resources.db")
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM resources WHERE id = ? AND user_id = ?", (resource_id, session['user_id']))
        conn.commit()
    except Exception as e:
        print(f"Error deleting resource: {e}")
        conn.rollback()
    finally:
        conn.close()
        
    return redirect('/dashboard') 

if __name__ == "__main__":
    app.run(debug=True)