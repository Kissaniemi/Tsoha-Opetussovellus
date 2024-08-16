from flask import redirect, render_template, request, url_for
from app import app
import courses, users, materials, tasks
from flask import session


@app.route("/")
def index():
    id_user = session.get("user_id", 0)
    name = users.get_user_name(id_user)
    return render_template("index.html", name=name)


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
        if len(username) > 40:
            return render_template("error.html", error="username too long (maximum 40 characters)")
        if len(password1) > 1000:
            return render_template("error.html", error="password too long (maximum 1000 characters)")
        if len(username) < 4:
            return render_template("error.html", error="username too short (minimum 4 characters)")
        if len(password1) < 4:
            return render_template("error.html", error="password too short (minimum 4 characters)")
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
        if len(username) > 40:
            return render_template("error.html", error="username too long (maximum 40 characters)")
        if len(password1) > 1000:
            return render_template("error.html", error="password too long (maximum 1000 characters)")
        if len(username) < 4:
            return render_template("error.html", error="username too short (minimum 4 characters)")
        if len(password1) < 4:
            return render_template("error.html", error="password too short (minimum 4 characters)")
        if password1 != password2:
            return render_template(
                "error.html", message="Passwords do not match")
        if users.register(username, password1, "teacher"):
            return redirect("/")
        return render_template(
            "error.html", message="User creation failed")


"""Course related routes"""

@app.route("/courses", methods=["GET", "POST"])
def get_course():
    id = users.get_user_id()
    if id == 0:
        return render_template(
            "error.html", message="You need to log in first")
    list = courses.get_list()
    return render_template("courses.html", count=len(list), courses=list) 


@app.route("/create_course", methods=["GET", "POST"])
def create_course():
    if request.method == "GET":
            user_type = users.get_user_type()
            if user_type[0] == False:
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
        if not courses.join_course(course_id):
            return render_template(
            "error.html", message="Already joined course")
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
        teacher_id = users.get_user_id()
        if not courses.check_course_teacher(teacher_id, id):
            return render_template(
                "error.html", message="Only the course teacher can change the course")
        info = courses.get_course_info(id)
        return render_template("change_course.html", info=info)
    
    if request.method == "POST":
        teacher_id = users.get_user_id()
        coursename = request.form["coursename"]
        description = request.form["description"]
        if len(coursename) > 100:
            return render_template("error.html", error="Course name too long")
        if len(description) > 1000:
            return render_template("error.html", error="Course description too long")
        if session["csrf_token"] != request.form["csrf_token"]:
                return render_template("error.html", error="403")
        if courses.check_course_teacher(teacher_id, id):
            if courses.change_course(id, coursename, description):
                return redirect("/courses")
        return render_template(
                "error.html", message="Course change failed")


@app.route("/own_courses", methods=["GET"])
def own_courses():
    if request.method == "GET":
        id = users.get_user_id()
        if id == 0:
            return render_template(
                "error.html", message="You need to log in first")

        user_type = users.get_user_type()
        if user_type[0] == False:
            own = courses.get_own_courses(id)
            course_info = []
            for course in own:
                course_info.append(courses.get_course_info(course[0]))    
            return render_template("own_courses.html", course_info=course_info)
        else:
            own = courses.get_teacher_courses(id)
            course_info = []
            for course in own:
                course_info.append(courses.get_course_info(course[0]))    
            return render_template("own_courses.html", course_info=course_info)


@app.route("/course_statistics/<int:course_id>", methods=["GET"])
def course_statistics(course_id):
    if request.method == "GET":
        id = users.get_user_id()
        user_type = users.get_user_type()
        if user_type[0] == False:
            course_info = courses.get_course_info(course_id)
            teacher = users.get_user_name(course_info[2])
            course_tasks = tasks.get_tasks(course_id)
            answers = []
            for task in course_tasks:
                    answers.append((tasks.get_answers(id, task[0])))
            return render_template("student_statistics.html", course_info=course_info, teacher=teacher, course_tasks=course_tasks, answers=answers, length=len(answers))
        
        else:
            course_info = courses.get_course_info(course_id)
            student_info = courses.get_course_students(course_id)
            course_tasks = tasks.get_tasks(course_id)
            students = []
            student_results = []
            for student in student_info:
                students.append(users.get_user_name(student[0]))     
                for task in course_tasks:
                    student_results.append((users.get_user_name(student[0]),task, tasks.get_answers(student[0], task[0])))

            return render_template("teacher_statistics.html", course_info=course_info, tasks=course_tasks, student_info=students, student_results=student_results)


""" Material related routes """

@app.route("/add_material/<int:id>", methods=["GET", "POST"])
def add_material(id):
    if request.method == "GET":
        teacher_id = users.get_user_id()
        if not courses.check_course_teacher(teacher_id, id):
            return render_template(
                "error.html", message="Only the course teacher can add material to this course")
        return render_template("new_material.html", id=id)
    if request.method == "POST":
        name = request.form["materialname"]
        material = request.form["materialtext"]
        if materials.add_material(id, name, material):
            return redirect(url_for("course_page", id=id))
        else:
            return render_template("error.html", message="Creating course material failed")


@app.route("/course_material/<int:id>", methods=["GET", "POST"])
def get_material(id):
    user_id = users.get_user_id()
    if not courses.check_course_teacher(user_id, id):
        if not courses.check_course_student(user_id, id):
            return render_template(
                "error.html", message="Only students of this course can see the course material")
    material = materials.get_materials(id)
    return render_template("materials.html", id=id, material=material)


@app.route("/delete_material/<int:mat_id>", methods =["POST"])
def delete_material(mat_id):
    if request.method == "POST":
        teacher_id = users.get_user_id()
        mat_info = materials.get_material_info(mat_id)[3]
        course_id = courses.get_course_info(mat_info)[0]
        if courses.check_course_teacher(teacher_id, course_id):
            if materials.delete_material(mat_id):
                return redirect(f"/course_material/{course_id}")
        return render_template(
                "error.html", message="Only the teacher of this course can delete the material")


@app.route("/change_material/<int:id>", methods=["GET", "POST"])
def change_material(id):
    if request.method == "GET":
        if not id:
            return render_template(
                "error.html", message="material id not found")
        teacher_id = users.get_user_id()
        info = materials.get_material_info(id)
        course_id = info[3]
        if not courses.check_course_teacher(teacher_id, course_id):
            return render_template(
                "error.html", message="Only the course teacher can change the material")   
        return render_template("change_material.html", info=info)
    
    if request.method == "POST":
        materialname = request.form["materialname"]
        materialtext = request.form["materialtext"]
        if len(materialname) > 100:
            return render_template("error.html", error="Material name too long")
        if len(materialtext) > 1000:
            return render_template("error.html", error="Material text too long")
        if session["csrf_token"] != request.form["csrf_token"]:
                return render_template("error.html", error="403")
        if materials.change_material(id, materialname, materialtext):
            info = materials.get_material_info(id)
            course_id = info[3]
            return redirect(f"/course_material/{course_id}")
        return render_template(
                "error.html", message="Material change failed")

"""Task related routes"""

@app.route("/course_tasks/<int:id>")
def get_tasks(id):
    user_id = users.get_user_id()
    if not courses.check_course_teacher(user_id, id):
        if not courses.check_course_student(user_id, id):
            return render_template(
                "error.html", message="Only students of this course can see the course tasks")
    task_info = tasks.get_tasks(id)
    return render_template("tasks.html", task_id=id, task_info=task_info, length=(len(task_info)))


@app.route("/add_tasks/<int:course_id>", methods=["GET", "POST"])
def create_task(course_id):
    if request.method == "GET":
        teacher_id = users.get_user_id()
        if not courses.check_course_teacher(teacher_id, course_id):
            return render_template(
                "error.html", message="Only the course teacher can add material to this course")
        return render_template("new_task.html", course_id=course_id)
    
    if request.method == "POST":
        question = request.form["question"]
        choices = request.form.getlist("choice")
        answers = request.form.getlist("answer")
        if tasks.add_task_choices(question, course_id, choices, answers):
                    return redirect(f"/course_tasks/{course_id}")
        return render_template(
            "error.html", message="Task creation failed")


@app.route("/task_page/<int:task_id>", methods=["GET", "POST"])
def do_task(task_id):
    if request.method == "GET":
        task_info = tasks.get_task_info(task_id)
        task_choices = tasks.get_task_choices(task_id)
        return render_template("task_page.html", task_info=task_info, task_choices=task_choices, length= len(task_choices))
    
    if request.method == "POST":
        answers = request.form.getlist("answer")
        choices = tasks.get_task_choices(task_id)
        user_id = users.get_user_id()
        if answers != []:
            if tasks.check_answers(answers, choices):
                tasks.add_result(user_id, task_id, True)
                return render_template(
                "task_result.html", message= "correct", task_id=task_id)
        
        tasks.add_result(user_id, task_id, False)
        return render_template(
            "task_result.html", message= "incorrect", task_id=task_id)
