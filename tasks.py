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
