from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "library_secret_key"

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="library_db"
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

    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM issued_books")
    total_issued = cursor.fetchone()[0]

    return render_template(
        "dashboard.html",
        total_books=total_books,
        total_issued=total_issued
    )


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
            "INSERT INTO books (title, author, category, quantity) VALUES (%s,%s,%s,%s)",
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

    cursor.execute("DELETE FROM books WHERE id=%s", (id,))
    db.commit()

    return redirect("/books")


# ---------------- ISSUE BOOK ----------------
@app.route("/issue", methods=["GET", "POST"])
def issue_book():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        student_name = request.form["student_name"]
        book_title = request.form["book_title"]
        issue_date = request.form["issue_date"]

        cursor.execute(
            "INSERT INTO issued_books (student_name, book_title, issue_date) VALUES (%s,%s,%s)",
            (student_name, book_title, issue_date)
        )

        db.commit()
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

if __name__ == "__main__":
    app.run(debug=True)
