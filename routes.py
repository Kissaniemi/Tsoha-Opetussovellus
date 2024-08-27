from flask import redirect, render_template, request, url_for
from flask import session
from app import app
import courses, users, materials, tasks

@app.route("/")
def index():
    user_id = session.get("user_id", 0)
    name = users.get_user_name(user_id)
    return render_template(
        "index.html", name=name)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template(
            "login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        message = "Wrong username or password"
        return render_template(
            "login.html", message=message)


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/create_users", methods=["GET"])
def create_users():
    if request.method == "GET":
        return render_template(
            "choose.html")


@app.route("/create_student", methods=["GET", "POST"])
def create_student():
    if request.method == "GET":
        return render_template(
            "register_student.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        errors = []
        if len(username) > 40:
            errors.append("Username too long (maximum 40 characters)")
        if len(password1) > 1000:
            errors.append("Password too long (maximum 1000 characters)")
        if len(username) < 4:
            errors.append("Username too short (minimum 4 characters)")
        if len(password1) < 4:
            errors.append("Password too short (minimum 4 characters)")
        if password1 != password2:
            errors.append("Passwords do not match")
        if session["csrf_token"] != request.form["csrf_token"]:
            errors.append("403")
        if errors:
            return render_template(
                "register_student.html", message=errors)
        if users.register(username, password1, "student"):
            users.login(username, password1)
            return redirect("/")
        return render_template(
            "register_student.html", error="User creation failed")


@app.route("/create_teacher", methods=["GET", "POST"])
def create_teacher():
    if request.method == "GET":
        return render_template(
            "register_teacher.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        errors = []
        if len(username) > 40:
            errors.append("Username too long (maximum 40 characters)")
        if len(password1) > 1000:
            errors.append("Password too long (maximum 1000 characters)")
        if len(username) < 4:
            errors.append("Username too short (minimum 4 characters)")
        if len(password1) < 4:
            errors.append("Password too short (minimum 4 characters)")
        if password1 != password2:
            errors.append("Passwords do not match")
        if session["csrf_token"] != request.form["csrf_token"]:
            errors.append("403")
        if errors:
            return render_template(
                "register_teacher.html", message=errors)
        if users.register(username, password1, "teacher"):
            users.login(username, password1)
            return redirect("/")
        return render_template(
            "register_teacher.html", error="User creation failed")


"""Course related routes"""

@app.route("/courses", methods=["GET", "POST"])
def get_course():
    user_id = session.get("user_id", 0)
    if user_id == 0:
        return render_template(
            "index.html", error="You need to log in first")
    course_list = courses.get_list()
    teacher = users.get_user_type(user_id)
    return render_template(
        "courses.html", count=len(course_list), courses=course_list, teacher=teacher[0])


@app.route("/create_course", methods=["GET", "POST"])
def create_course():
    if request.method == "GET":
        user_id = session.get("user_id", 0)
        if user_id == 0:
            return render_template(
                "index.html", error="You need to log in first")
        user_type = users.get_user_type(user_id)
        if user_type[0] is False:
            return render_template(
                "new_course.html", error="Only teachers can make courses")
        return render_template(
            "new_course.html")

    if request.method == "POST":
        coursename = request.form["coursename"]
        description = request.form["description"]
        errors = []
        if len(coursename) > 100:
            errors.append("Course name too long")
        if len(description) > 1000:
            errors.append("Course description too long")
        if len(coursename) < 5:
            errors.append("Course name too short (minimum 5 characters)")
        if len(description) < 5:
            errors.append("Course description too short (minimum 5 characters)")
        if session["csrf_token"] != request.form["csrf_token"]:
            errors.append("403")
        if errors:
            return render_template(
                "new_course.html", message=errors)
        user_id = session.get("user_id", 0)
        if courses.create_new(coursename, description, user_id):
            return redirect("/courses")
        return render_template(
            "new_course.html", message="Course creation failed")


@app.route("/join_course", methods=["POST"])
def join():
    if request.method == "POST":
        course_id = request.form["course_id"]
        user_id = session.get("user_id", 0)
        info = courses.get_course_info(course_id)
        teacher = users.get_user_type(user_id)
        if courses.check_course_teacher(user_id, course_id):
            return render_template(
                "course_page.html", info=info,
                teacher=teacher[0], message="Can't join own course")
        if courses.join_course(course_id, user_id):
            return render_template(
                "course_page.html", info=info,
                teacher=teacher[0], success="Joined course")
        if not courses.join_course(course_id, user_id):
            return render_template(
                "course_page.html", info=info,
                teacher=teacher[0], message="Already joined course")
        return render_template(
            "course_page.html", info=info,
            teacher=teacher[0], message="Joining course failed")


@app.route("/delete_course", methods=["POST"])
def delete_course():
    if request.method == "POST":
        course_id = request.form["course_id"]
        teacher_id = session.get("user_id", 0)
        info = courses.get_course_info(course_id)
        if courses.check_course_teacher(teacher_id, int(course_id)):
            if courses.delete_course(course_id):
                return redirect("/courses")
        return render_template(
            "course_page.html", info=info, teacher=teacher_id, 
            error="Only the course teacher can delete the course")


@app.route("/course_page/<int:course_id>", methods=["GET", "POST"])
def course_page(course_id):
    user_id = session.get("user_id", 0)
    if user_id == 0:
        return render_template(
            "index.html", error="You need to log in first")
    info = courses.get_course_info(course_id)
    user_id = session.get("user_id", 0)
    teacher = users.get_user_type(user_id)
    return render_template(
        "course_page.html", info=info, teacher=teacher[0])


@app.route("/change_course/<int:course_id>", methods=["GET", "POST"])
def change_course(course_id):
    if request.method == "GET":
        user_id = session.get("user_id", 0)
        if user_id == 0:
            return render_template(
                "index.html", error="You need to log in first")
        teacher_id = session.get("user_id", 0)
        if not courses.check_course_teacher(teacher_id, course_id):
            return render_template(
                "courses.html", error="Only the course teacher can change the course")
        info = courses.get_course_info(course_id)
        return render_template(
                "change_course.html", info=info)

    if request.method == "POST":
        teacher_id = session.get("user_id", 0)
        coursename = request.form["coursename"]
        description = request.form["description"]
        errors = []
        if len(coursename) > 100:
            errors.append("Course name too long")
        if len(description) > 1000:
            errors.append("Course description too long")
        if len(coursename) < 5:
            errors.append("Course name too short (minimum 5 characters)")
        if len(description) < 5:
            errors.append("Course description too short (minimum 5 characters)")
        if session["csrf_token"] != request.form["csrf_token"]:
            errors.append("403")
        if errors:
            return render_template(
                "change_course.html", info=info, message=errors)
        if courses.check_course_teacher(teacher_id, course_id):
            if courses.change_course(course_id, coursename, description):
                return redirect("/courses")
        return render_template(
                "change_course.html", info=info, error="Course change failed")


@app.route("/own_courses", methods=["GET"])
def own_courses():
    if request.method == "GET":
        user_id = session.get("user_id", 0)
        if user_id == 0:
            return render_template(
                "index.html", error="You need to log in first")
        user_type = users.get_user_type(user_id)
        if user_type[0] is False:
            own = courses.get_own_courses(user_id)
            course_info = []
            for course in own:
                course_info.append(courses.get_course_info(course[0]))
            return render_template(
                "own_courses.html", course_info=course_info, count= len(own))

        own = courses.get_teacher_courses(user_id)
        course_info = []
        for course in own:
            course_info.append(courses.get_course_info(course[0]))
        return render_template(
            "own_courses.html", course_info=course_info, count= len(own))


@app.route("/course_statistics/<int:course_id>", methods=["GET"])
def course_statistics(course_id):
    if request.method == "GET":
        user_id = session.get("user_id", 0)
        if user_id == 0:
            return render_template(
                   "index.html", error="You need to log in first")
        info = courses.get_course_info(course_id)
        teacher = users.get_user_type(user_id)
        user_type = users.get_user_type(user_id)
        if not courses.check_course_teacher(user_id, course_id):
            if not courses.check_course_student(user_id, course_id):
                return render_template(
                    "course_page.html", info=info, teacher=teacher[0],
                        message="Only students of this course can see the course statistics")
        if user_type[0] is False:
            course_info = courses.get_course_info(course_id)
            teacher = users.get_user_name(course_info[2])
            course_tasks = tasks.get_tasks(course_id)
            answers = []
            for task in course_tasks:
                answers.append((tasks.get_answers(user_id, task[0])))
            return render_template(
                "student_statistics.html", course_info=course_info,
                teacher=teacher, course_tasks=course_tasks,
                answers=answers, length=len(answers))

        course_info = courses.get_course_info(course_id)
        student_info = courses.get_course_students(course_id)
        course_tasks = tasks.get_tasks(course_id)
        students = []
        student_results = []
        for student in student_info:
            students.append(users.get_user_name(student[0]))
            for task in course_tasks:
                student_results.append((users.get_user_name(student[0]), \
                                        task, tasks.get_answers(student[0], task[0])))
        return render_template(
            "teacher_statistics.html", course_info=course_info,
            tasks=course_tasks, student_info=students,
            student_results=student_results, student_amount=len(student_info),
            task_amount=len(course_tasks))


""" Material related routes """

@app.route("/add_material/<int:course_id>", methods=["GET", "POST"])
def add_material(course_id):
    if request.method == "GET":
        user_id = session.get("user_id", 0)
        if user_id == 0:
            return render_template(
                "index.html", error="You need to log in first")
        teacher_id = session.get("user_id", 0)
        info = courses.get_course_info(course_id)
        if not courses.check_course_teacher(teacher_id, course_id):
            return render_template(
                "course_page.html", info=info, teacher=teacher_id,
                error="Only the course teacher can add material to this course")
        return render_template(
            "new_material.html", course_id=course_id)

    if request.method == "POST":
        name = request.form["materialname"]
        material = request.form["materialtext"]
        errors = []
        if len(name) > 30:
            errors.append("Material name too long")
        if len(material) > 500:
            errors.append("Material text too long")
        if len(name) < 5:
            errors.append("Material name too short (minimum 5 characters)")
        if len(material) < 5:
            errors.append("Material text too short (minimum 5 characters)")
        if session["csrf_token"] != request.form["csrf_token"]:
            errors.append("403")
        if errors:
            return render_template(
                "new_material.html", message=errors, course_id=course_id)
        if materials.add_material(course_id, name, material):
            return redirect(url_for("course_page", course_id=course_id))
        teacher_id = session.get("user_id", 0)
        info = courses.get_course_info(course_id)
        return render_template(
            "course_page.html", info=info, teacher=teacher_id,
            message="Creating course material failed")


@app.route("/course_material/<int:course_id>", methods=["GET", "POST"])
def get_material(course_id):
    user_id = session.get("user_id", 0)
    if user_id == 0:
        return render_template(
            "index.html", message="You need to log in first")
    info = courses.get_course_info(course_id)
    teacher = users.get_user_type(user_id)
    if not courses.check_course_teacher(user_id, course_id):
        if not courses.check_course_student(user_id, course_id):
            return render_template(
                "course_page.html", 
                info=info, teacher=teacher[0],
                message="Only students \
                of this course can see the course material")
    material = materials.get_materials(course_id)
    teacher = users.get_user_type(user_id)
    return render_template(
        "materials.html", course_id=course_id,
        material=material, teacher=teacher[0])


@app.route("/material_page/<int:course_id>/<int:material_id>")
def material_page(course_id, material_id):
    user_id = session.get("user_id", 0)
    if user_id == 0:
        return render_template("courses.html", message="You need to log in first")
    if not courses.check_course_teacher(user_id, course_id):
        if not courses.check_course_student(user_id, course_id):
            return render_template(
                "courses.html", message="Only students \
                of this course can see the course material")
    material = materials.get_material_info(material_id)
    max_count = materials.get_max_id(course_id)
    min_count = materials.get_min_id(course_id)
    previous_material = None
    next_material = None
    for i in range(material_id+1, max_count+1):
        if materials.get_material_info(i):
            next_material = i
            break
    for i in range(material_id, min_count, -1):
        if materials.get_material_info(i-1):
            previous_material = i-1
            break
    return render_template(
        "material_page.html", course_id=course_id,
        material=material, next_material=next_material, previous_material=previous_material)


@app.route("/delete_material/<int:mat_id>", methods =["POST"])
def delete_material(mat_id):
    if request.method == "POST":
        teacher_id = session.get("user_id", 0)
        mat_info = materials.get_material_info(mat_id)[3]
        course_id = courses.get_course_info(mat_info)[0]
        if courses.check_course_teacher(teacher_id, course_id):
            if materials.delete_material(mat_id):
                return redirect(f"/course_material/{course_id}")
        return render_template(
            "course_material.html", error="Only the teacher \
            of this course can delete the material")


@app.route("/change_material/<int:material_id>", methods=["GET", "POST"])
def change_material(material_id):
    if request.method == "GET":
        user_id = session.get("user_id", 0)
        if user_id == 0:
            return render_template(
                "index.html", error="You need to log in first")
        teacher_id = session.get("user_id", 0)
        info = materials.get_material_info(material_id)
        course_id = info[3]
        if not courses.check_course_teacher(teacher_id, course_id):
            return render_template(
                "materials.html", error="Only the \
                course teacher can change the material")
        return render_template(
            "change_material.html", info=info)

    if request.method == "POST":
        name = request.form["materialname"]
        material = request.form["materialtext"]
        errors = []
        if len(name) > 30:
            errors.append("Material name too long")
        if len(material) > 500:
            errors.append("Material text too long")
        if len(name) < 5:
            errors.append("Material name too short (minimum 5 characters)")
        if len(material) < 5:
            errors.append("Material text too short (minimum 5 characters)")
        if session["csrf_token"] != request.form["csrf_token"]:
            errors.append("403")
        if errors:
            return render_template(
                "change_material.html", message=errors)
        if materials.change_material(material_id, name, material):
            info = materials.get_material_info(material_id)
            course_id = info[3]
            return redirect(f"/course_material/{course_id}")
        return render_template(
            "change_material.html", message="Material change failed")

"""Task related routes"""

@app.route("/course_tasks/<int:course_id>")
def get_tasks(course_id):
    user_id = session.get("user_id", 0)
    if user_id == 0:
        return render_template(
            "index.html", error="You need to log in first")
    user_id = session.get("user_id", 0)
    task_info = tasks.get_tasks(course_id)
    teacher = users.get_user_type(user_id)
    info = courses.get_course_info(course_id)
    if not courses.check_course_teacher(user_id, course_id):
        if not courses.check_course_student(user_id, course_id):
            return render_template(
                "course_page.html",  info=info,
                teacher=teacher[0],
                message="Only students of this course can see the course tasks")
    return render_template(
        "tasks.html", course_id=course_id, task_info=task_info,
        length=(len(task_info)), teacher=teacher[0])


@app.route("/add_multiple_choice/<int:course_id>", methods=["GET", "POST"])
def add_multiple_choice(course_id):
    if request.method == "GET":
        user_id = session.get("user_id", 0)
        if user_id == 0:
            return render_template(
                "index.html", error="You need to log in first")
        if not courses.check_course_teacher(user_id, course_id):
            return render_template(
                "courses.html", error="Only the course teacher \
                can add tasks to this course")
        return render_template(
            "new_multiple_choice_task.html", course_id=course_id)

    if request.method == "POST":
        question = request.form["question"]
        choices = request.form.getlist("choice")
        answers = request.form.getlist("answer")
        errors = []
        if len(question) > 100:
            errors.append("Question too long (maximum 100 characters)")
        if len(question) < 5:
            errors.append("Question too short (minimum 5 characters)")
        for choice in choices:
            if len(choice) > 100:
                errors.append("Answer too long (maximum 100 characters)")
            if len(choice) < 1:
                errors.append("Answer too short (minimum 1 characters)")
        if len(choices) == 10:
            errors.append("Too many choices (maximum 10 choices)")
        if session["csrf_token"] != request.form["csrf_token"]:
            errors.append("403")
        if errors:
            return render_template(
                "new_multiple_choice_task.html", message=errors)
        task_id = tasks.add_task(question, course_id, "multiple choice")
        if tasks.add_task_choices(task_id, choices, answers):
            return redirect(f"/course_tasks/{course_id}")
        return render_template(
            "new_multiple_choice_task.html", message="Task creation failed")


@app.route("/add_fill_in/<int:course_id>", methods=["GET", "POST"])
def add_fill_in(course_id):
    if request.method == "GET":
        user_id = session.get("user_id", 0)
        if user_id == 0:
            return render_template(
                "index.html", error="You need to log in first")
        if not courses.check_course_teacher(user_id, course_id):
            return render_template(
                "courses.html", error="Only the course teacher \
                can add tasks to this course")
        return render_template(
            "new_fill_in_task.html", course_id=course_id)

    if request.method == "POST":
        question = request.form["question"]
        answer = request.form["answer"]
        errors = []
        if len(question) > 100:
            errors.append("Question too long (maximum 100 characters)")
        if len(answer) > 30:
            errors.append("Answer too long (maximum 30 characters)")
        if len(question) < 5:
            errors.append("Question too short (minimum 5 characters)")
        if len(answer) < 1:
            errors.append("Answer too short (minimum 1 characters)")
        if session["csrf_token"] != request.form["csrf_token"]:
            errors.append("403")
        if errors:
            return render_template(
                "new_fill_in_task.html", message=errors)
        task_id = tasks.add_task(question, course_id, "fill in")
        if tasks.add_task_choice(task_id, answer):
            return redirect(f"/course_tasks/{course_id}")
        return render_template(
            "new_fill_in_task.html", message="Task creation failed")


@app.route("/task_page/<int:course_id>/<int:task_id>", methods=["GET", "POST"])
def do_task(course_id, task_id):
    if request.method == "GET":
        user_id = session.get("user_id", 0)
        all_tasks = tasks.get_tasks(course_id)
        teacher = users.get_user_type(user_id)
        if user_id == 0:
            return render_template(
                "index.html", error="You need to log in first")
        if not courses.check_course_student(user_id, course_id):
            return render_template(
                "tasks.html", course_id=course_id, task_info=all_tasks,
                length=(len(all_tasks)), teacher=teacher[0],
                message="Only students can try the course tasks")

        task_choices = tasks.get_task_choices(task_id)
        task_info = tasks.get_task_info(task_id)
        max_count = tasks.get_max_id(course_id)
        min_count = tasks.get_min_id(course_id)
        next_task = None
        previous_task = None

        for i in range(task_id+1, max_count+1):
            if tasks.get_task_info(i):
                next_task = i
                break

        for i in range(task_id, min_count, -1):
            if tasks.get_task_info(i-1):
                previous_task = i-1
                break

        if task_info[3] == "multiple choice":
            return render_template(
                "task_page_multiple_choice.html",
                task_info=task_info, task_choices=task_choices,
                length= len(task_choices), course_id=course_id,
                next_task=next_task, previous_task=previous_task)

        if task_info[3] == "fill in":
            return render_template(
                "task_page_fill_in.html",
                task_info=task_info, course_id=course_id,
                next_task=next_task, previous_task=previous_task)

    if request.method == "POST":
        user_id = session.get("user_id", 0)
        task_info = tasks.get_task_info(task_id)
        teacher = users.get_user_type(user_id)
        max_count = tasks.get_max_id(course_id)
        min_count = tasks.get_min_id(course_id)
        next_task = None
        previous_task = None

        for i in range(task_id+1, max_count+1):
            if tasks.get_task_info(i):
                next_task = i
                break
        for i in range(task_id, min_count, -1):
            if tasks.get_task_info(i-1):
                previous_task = i-1
                break

        msg = "incorrect"
        if task_info[3] == "multiple choice":
            task_choices = tasks.get_task_choices(task_id)
            answers = request.form.getlist("answer")
            choices = tasks.get_task_choices(task_id)
            user_id = session.get("user_id", 0)
            if answers != []:
                if tasks.check_answers(answers, choices):
                    tasks.add_result(user_id, task_id, True)
                    msg = "correct"
            else:
                tasks.add_result(user_id, task_id, False)
            return render_template(
                "task_result.html", message=msg, task_id=task_id,
                course_id=course_id, next_task=next_task,
                previous_task=previous_task)

        if session["csrf_token"] != request.form["csrf_token"]:
            return render_template(
                "tasks.html", course_id=course_id, task_info=all_tasks,
                length=(len(all_tasks)), teacher=teacher[0],
                message="403")

        answer = request.form["answer"]
        user_id = session.get("user_id", 0)
        if tasks.check_match(task_id, answer):
            tasks.add_result(user_id, task_id, True)
            msg = "correct"
        else:
            tasks.add_result(user_id, task_id, False)
        return render_template(
            "task_result.html", message= msg, task_id=task_id,
            course_id=course_id, next_task=next_task,
            previous_task=previous_task)


@app.route("/choose_task/<int:course_id>", methods=["GET"])
def choose_task(course_id):
    if request.method == "GET":
        user_id = session.get("user_id", 0)
        if user_id == 0:
            return render_template(
                "index.html", error="You need to log in first")
        if not courses.check_course_teacher(user_id, course_id):
            return render_template(
                "courses.html", error="Only the \
                course teacher can add tasks to this course")
        info = courses.get_course_info(course_id)
        return render_template(
            "choose_task.html", info=info, course_id=course_id)


@app.route("/delete_task/<int:task_id>", methods =["POST"])
def delete_task(task_id):
    if request.method == "POST":
        user_id = session.get("user_id", 0)
        if user_id == 0:
            return render_template(
                "index.html", error="You need to log in first")
        task_info = tasks.get_task_info(task_id)
        if courses.check_course_teacher(user_id, task_info[2]):
            if tasks.delete_task(task_id):
                return redirect(f"/course_tasks/{task_info[2]}")
        return render_template(
            "courses.html", error="Only the teacher \
            of this course can delete tasks")
