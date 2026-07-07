from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db

app = Flask(__name__)
app.secret_key = "school_management_secret_key"


# Home
@app.route("/")
def home():
    return redirect(url_for("login"))


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))

        return "<h2>Invalid Username or Password</h2>"

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

        <style>
            body {
                background: linear-gradient(120deg, #4e73df, #224abe);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: Arial;
            }

            .card {
                width: 380px;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0px 10px 20px rgba(0,0,0,0.2);
            }

            .logo {
                width: 80px;
                margin-bottom: 10px;
            }
        </style>

    </head>

    <body>

        <div class="card text-center">

            <img src="/static/school_logo.png" class="logo">

            <h4>Isadaw Management System</h4>

            <form method="POST">

                <div class="mb-3 text-start">
                    <label>Username</label>
                    <input type="text" name="username" class="form-control" required>
                </div>

                <div class="mb-3 text-start">
                    <label>Password</label>
                    <input type="password" name="password" class="form-control" required>
                </div>

                <button class="btn btn-primary w-100">Login</button>

            </form>

        </div>

    </body>
    </html>
    """


# Dashboard
@app.route("/dashboard")
def dashboard():

    if "logged_in" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_users=total_users
    )


# Register Student
@app.route("/register", methods=["GET", "POST"])
def register():

    if "logged_in" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        reg_no = request.form["reg_no"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        student_class = request.form["class"]
        phone = request.form["phone"]
        address = request.form["address"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO students
        (reg_no, firstname, lastname, gender, dob, class, phone, address)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            reg_no,
            firstname,
            lastname,
            gender,
            dob,
            student_class,
            phone,
            address
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("students"))

    return render_template("register_student.html")


# View Students
@app.route("/students")
def students():

    if "logged_in" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search")

    conn = get_db()
    cursor = conn.cursor()

    if search:

        cursor.execute("""
        SELECT * FROM students
        WHERE reg_no LIKE %s
        OR firstname LIKE %s
        OR lastname LIKE %s
        """,
        (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        ))

    else:

        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "students.html",
        students=students
    )


# Edit Student
@app.route("/edit_student/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    if "logged_in" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":

        reg_no = request.form["reg_no"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        student_class = request.form["class"]
        phone = request.form["phone"]
        address = request.form["address"]

        cursor.execute("""
        UPDATE students
        SET reg_no=%s,
            firstname=%s,
            lastname=%s,
            gender=%s,
            dob=%s,
            class=%s,
            phone=%s,
            address=%s
        WHERE student_id=%s
        """,
        (
            reg_no,
            firstname,
            lastname,
            gender,
            dob,
            student_class,
            phone,
            address,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("students"))

    cursor.execute(
        "SELECT * FROM students WHERE student_id=%s",
        (id,)
    )

    student = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "edit_student.html",
        student=student
    )


# Delete Student
@app.route("/delete_student/<int:id>")
def delete_student(id):

    if "logged_in" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE student_id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("students"))


# Logout
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
