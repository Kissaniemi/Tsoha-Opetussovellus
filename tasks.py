"""Task related functions
    """
from sqlalchemy.sql import text
from db import db

def get_tasks(course_id):
    """Get all course tasks (related to the given course)
    """
    sql = text("SELECT id, question FROM tasks WHERE course_id=:course_id ")
    result = db.session.execute(sql, 
                                {"course_id": course_id})
    return result.fetchall()


def add_task_choices(question, course_id, choices, answers):
    """Add a multiple choice task to the course
    """
    try:
        sql = text("INSERT INTO tasks (question, course_id) VALUES(:question,:course_id) RETURNING id")
        result = db.session.execute(sql,
                                {
                                "question": question,
                                "course_id": course_id})
        task_id = result.fetchone()[0]

        for i in range(0, len(choices)):
            if choices[i] != "":
                sql = text("INSERT INTO choices (task_id, choice, answer) VALUES (:task_id, :choice, :answer)")
                if str(i) in answers:
                    db.session.execute(sql, {"task_id":task_id, "choice":choices[i], "answer": True})
                else:
                    db.session.execute(sql, {"task_id":task_id, "choice":choices[i], "answer": False})
        db.session.commit()

    except BaseException:
        return False
    return True


def get_task_info(task_id):
    """Returns task with the given id
    """
    sql = text("SELECT id, question, course_id FROM tasks WHERE id=:id")
    result = db.session.execute(sql, {"id": task_id})
    return result.fetchone()


def get_task_choices(task_id):
    """Returns task related choices and whether the choices truth value
    """
    sql = text("SELECT choice, answer FROM choices WHERE task_id=:task_id")
    result = db.session.execute(sql, {"task_id": task_id})
    return result.fetchall()


def check_answers(answers, choices):
    """ Checks if the answers to the task were correct"""
    for i in answers:
        if choices[int(i)][1] == False:
            return False
    return True


def add_result(student_id, task_id, correct):
    """ Adds the students task result to the answers table
    """
    try:
        if check_result(student_id, task_id):
            sql = text("INSERT INTO answers (student_id, task_id, correct) VALUES (:student_id, :task_id, :correct)")
        else:
            sql = text("UPDATE answers SET correct=:correct WHERE student_id=:student_id AND task_id=:task_id")
        db.session.execute(sql,
                            {
                            "student_id": student_id,
                            "task_id": task_id,
                            "correct": correct})
        db.session.commit()
        
    except BaseException:
        return False
    return True


def check_result(student_id, task_id):
    """Check if students result already exists
    """
    sql = text("SELECT id FROM answers WHERE student_id=:student_id AND task_id=:task_id")
    result = db.session.execute(sql, {"student_id": student_id,
                                      "task_id": task_id})
    user = result.fetchone()
    if not user:
        return True
    return False


def get_answers(student_id, task_id):
    """Returns given students_id and answer to given task, if student has not done task, returns Not done yet if not 
    """
    sql = text("SELECT student_id, correct FROM answers WHERE student_id=:student_id AND task_id=:task_id")

    result = db.session.execute(sql, { "student_id":student_id,
                                     "task_id": task_id})
    answer = result.fetchone()
    if not answer:
        return (student_id, "Not done yet")
    return answer