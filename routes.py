from flask import redirect, render_template, request
from app import app
import courses, users
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
    return render_template("courses.html", count=len(list), courses=list) 


@app.route("/create_course", methods=["GET", "POST"])
def create_course():
    if request.method == "GET":
            user_type = users.get_user_type()
            if user_type == False:
                return render_template(
                "error.html", message="Only teachers can make courses")
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
        if courses.create_new(coursename, description):
            return redirect("/courses")
        return render_template(
            "error.html", message="Course creation failed")


@app.route("/join_course", methods=["POST"])
def join():
    if request.method == "POST":
        course_id = request.form["course_id"]
        user_id = users.get_user_id()
        if courses.check_course_teacher(user_id, course_id):
            return render_template(
                "error.html", message="Can't join own course")

        if courses.join_course(course_id):
            return redirect("/courses")    # TODO parempi ilmoitus kurssille lisäyksen onnistumisesta
        return render_template(
            "error.html", message="Joining course failed")


@app.route("/delete_course", methods=["POST"])
def delete_course():
    if request.method == "POST":
        course_id = request.form["course_id"]
        teacher_id = users.get_user_id()
        if courses.check_course_teacher(teacher_id, course_id):
            if courses.delete_course(course_id):
                return redirect("/courses")
        return render_template(
                "error.html", message="Only the course teacher can delete the course")

@app.route("/course_page/<int:id>", methods=["GET", "POST"])
def course_page(id):
    info = courses.get_course_info(id)
    return render_template("course_page.html", info=info)


@app.route("/change_course/<int:id>", methods=["GET", "POST"])
def change_course(id):
    if request.method == "GET":
        if not id:
            return render_template(
                "error.html", message="course id not found")
        info = courses.get_course_info(id)
        return render_template("change_course.html", info=info)

    if request.method == "POST":
        course_id = request.form["course_id"]
        coursename = request.form["coursename"]
        description = request.form["description"]
        teacher_id = users.get_user_id()
        if len(coursename) > 100:
            return render_template("error.html", error="Course name too long")
        if len(description) > 1000:
            return render_template("error.html", error="Course description too long")
        if session["csrf_token"] != request.form["csrf_token"]:
                return render_template("error.html", error="403")
        if courses.check_course_teacher(teacher_id, course_id):
            if courses.change_course(course_id, coursename, description):
                return redirect("/courses")
        return render_template(
                "error.html", message="Only the course teacher can change the course")