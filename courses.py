"""Course related functions
    """
from sqlalchemy.sql import text
from db import db
import users, tasks

# TODO lisää paremmat virheviestit routes:iin sen sijaan että palautetaan vain False

def get_list():
    """Returns all courses (if available)
    """
    sql = text("SELECT id, name, description FROM courses")
    result = db.session.execute(sql)
    return result.fetchall()

def create_new(name, description):
    """Create a new course
    """
    user_id = users.get_user_id()
    try:
        sql = text("SELECT name FROM courses WHERE name=:name")
        result = db.session.execute(sql, {"name": name})
        user = result.fetchone()
        if user:
            return False
        sql = text(
            "INSERT INTO courses(name, teacher_id, description) VALUES(:name,:teacher_id,:description)")
        db.session.execute(sql,
                            {"name": name,
                            "teacher_id": user_id,
                            "description": description})

        db.session.commit()
    except BaseException:
        return False
    return True

def join_course(course_id):
    """Join course
    """
    user_id = users.get_user_id()
    try:
        sql = text("SELECT id FROM students WHERE user_id=:user_id AND course_id=:course_id ")
        result = db.session.execute(sql, 
                                    {"user_id": user_id, 
                                    "course_id": course_id})
        user = result.fetchone()
        if user:
            return False
         
        sql = text("INSERT INTO students(user_id, course_id) VALUES(:user_id, :course_id)")
        db.session.execute(sql,
                           {"user_id": user_id,
                            "course_id": course_id})
        db.session.commit()
    except BaseException:
        return False
    return True


def check_course_teacher(teacher_id, course_id):
    """Checks that the given user_id matches the course teacher_id
    """
    sql = text("SELECT teacher_id FROM courses WHERE id=:id AND teacher_id=:teacher_id")
    result = db.session.execute(sql, 
                                {"id": course_id,
                                "teacher_id": teacher_id})
    if result.fetchone() is None:
        return False
    return True


def check_course_student(user_id, course_id):
    """Checks that the given user_id matches a student in the course
    """
    sql = text("SELECT user_id FROM students WHERE user_id=:user_id AND course_id=:course_id ")
    result = db.session.execute(sql, {
                                "user_id":user_id,
                                "course_id": course_id})
    if result.fetchone() is None:
        return False
    return True


def delete_course(course_id):
    """Deletes course and all course related info
    """
    try:
        course_tasks = tasks.get_tasks(course_id)
        for task in course_tasks:
            tasks.delete_task(task[0])

        sql = text("DELETE FROM materials WHERE course_id=:course_id")
        db.session.execute(sql, 
                            {"course_id": course_id})
        db.session.commit()

        sql = text("DELETE FROM students WHERE course_id=:course_id")
        db.session.execute(sql, 
                            {"course_id": course_id})
        db.session.commit()

        sql = text("DELETE FROM courses WHERE id=:id")
        db.session.execute(sql, 
                            {"id": course_id})
        db.session.commit()

    except BaseException:
        return False
    return True

def get_course_info(id):
    """Returns course id, name, teacher_id and description
    """
    sql = text("SELECT id, name, teacher_id, description FROM courses WHERE id=:id ")
    result = db.session.execute(sql, 
                                {"id": id})
    return result.fetchone()


def change_course(course_id, name, description):
    """Changes course info"""
    try:
        sql = text("UPDATE courses SET name=:name, description=:description WHERE id=:course_id")
        db.session.execute(sql, {"course_id": course_id,
                                 "name": name,
                                 "description":description})
        db.session.commit()

    except BaseException:
        return False
    return True


def get_own_courses(user_id):
    """Returns list of courses that the given user_id has joined
    """
    sql = text("SELECT course_id FROM students WHERE user_id=:user_id ")
    result = db.session.execute(sql, 
                                {"user_id": user_id})
    return result.fetchall()


def get_teacher_courses(teacher_id):
    """Returns list of courses that given teacher_id has created
    """
    sql = text("SELECT id FROM courses WHERE teacher_id=:teacher_id ")
    result = db.session.execute(sql,
                                {"teacher_id": teacher_id})
    return result.fetchall()


def get_course_students(course_id):
    """Returns list of students joined in the given course_id
    """
    sql = text("SELECT user_id FROM students WHERE course_id=:course_id")
    result = db.session.execute(sql,
                                {"course_id": course_id})
    return result.fetchall()