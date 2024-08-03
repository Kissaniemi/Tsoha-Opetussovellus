from flask import redirect, render_template, request
from app import app
import courses
import users
from flask import session


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        return render_template(
            "error.html", message="Wrong username or password")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/create_users", methods=["GET"])
def create_users():
    if request.method == "GET":
        return render_template("choose.html")


@app.route("/create_student", methods=["GET", "POST"])
def create_student():
    if request.method == "GET":
        return render_template("register_student.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template(
                "error.html", message="Passwords do not match")
        if users.register(username, password1, "student"):
            return redirect("/")
        return render_template(
            "error.html", message="User creation failed")


@app.route("/create_teacher", methods=["GET", "POST"])
def create_teacher():
    if request.method == "GET":
        return render_template("register_teacher.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template(
                "error.html", message="Passwords do not match")
        if users.register(username, password1, "teacher"):
            return redirect("/")
        return render_template(
            "error.html", message="User creation failed")


@app.route("/courses", methods=["GET", "POST"])
def get_course():
    list = courses.get_list()
    return render_template("courses.html", count=len(list), courses=list) # TODO check että kurssit vain opettajien tehtävissä

@app.route("/create_course", methods=["GET", "POST"])
def create_course():
    if request.method == "GET":
        return render_template("new_course.html")
    if request.method == "POST":
        coursename = request.form["coursename"]
        description = request.form["description"]
        if len(coursename) > 100:
            return render_template("error.html", error="Course name too long")
        if len(description) > 1000:
            return render_template("error.html", error="Course description too long")
        if session["csrf_token"] != request.form["csrf_token"]:
             return render_template("error.html", error="403")
        # TODO chekkaa että kurssinimi ei ole jo viety
        if courses.create_new(coursename, description):
            return redirect("/courses")
        return render_template(
            "error.html", message="Course creation failed")

