"""Course related functions
    """
from sqlalchemy.sql import text
from db import db
import users


def get_list():
    """Returns all courses (if available)
    """
    sql = text("SELECT id, name FROM courses")
    result = db.session.execute(sql)
    return result.fetchall()

def create_new(name, description):
    """Create a new course
    """
    user_id = users.get_user_id()
    try:
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
