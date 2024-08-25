"""User related functions
    """
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db
import secrets


def login(username, password):
    """Login function
    """
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False

    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["csrf_token"] = secrets.token_hex(16)
        return True
    return False


def logout():
    """Logout function
    """
    del session["user_id"]


def register(username, password, user_type):
    """Register new user profile
    """
    hash_value = generate_password_hash(password)
    try:
        if user_type == "teacher":
            sql = text(
                "INSERT INTO users(username,password,teacher) VALUES(:username,:password,:teacher)")
            db.session.execute(sql,
                               {"username": username,
                                "password": hash_value,
                                "teacher": True})
        else:
            sql = text(
                "INSERT INTO users(username,password,teacher) VALUES(:username,:password,:teacher)")
            db.session.execute(sql,
                               {"username": username,
                                "password": hash_value,
                                "teacher": False})
        db.session.commit()
    except BaseException:
        return False
    return True


def get_user_type(user_id):
    """Returns user type (teacher or not)
    """
    sql = text("SELECT teacher FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id": user_id})
    return result.fetchone()


def get_user_name(user_id):
    """Returns username
    """
    sql = text("SELECT username FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id": user_id})
    result_one = result.fetchone()
    if result_one is None:
        return False
    return result_one[0]

