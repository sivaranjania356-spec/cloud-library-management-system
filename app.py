from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "library_secret_key"

# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="library_db"
# )
# cursor = db.cursor()

Railway MySQL Connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )

        admin = cursor.fetchone()

        if admin:
            session["user"] = username
            return redirect("/dashboard")

        return "Invalid Login ❌"

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return render_template("dashboard.html", total_books=0, total_issued=0)


# ---------------- BOOK LIST ----------------
@app.route("/books")
def books():
    if "user" not in session:
        return redirect("/")

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    return render_template("books.html", books=books)


# ---------------- ADD BOOK ----------------
@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        quantity = request.form["quantity"]

        cursor.execute(
            "INSERT INTO books(title, author, category, quantity) VALUES (%s,%s,%s,%s)",
            (title, author, category, quantity)
        )

        db.commit()
        return redirect("/books")

    return render_template("add_book.html")


# ---------------- DELETE BOOK ----------------
@app.route("/delete/<int:id>")
def delete_book(id):
    if "user" not in session:
        return redirect("/")

    return redirect("/books")


# ---------------- ISSUE BOOK ----------------
@app.route("/issue", methods=["GET", "POST"])
def issue_book():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        return redirect("/dashboard")

    return render_template("issue_book.html")


# ---------------- RETURN BOOK ----------------
@app.route("/return_book")
def return_book():
    if "user" not in session:
        return redirect("/")

    return render_template("return_book.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


print("STARTING LIBRARY PROJECT")

# if __name__ == "__main__":
#     app.run(debug=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)