"""Login related functions
    """
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db
import secrets


def login(username, password):
    """Login function

    Args:
        username: profile username
        password: profile password

    Returns:
        Boolean: True if username and password ok, False if not
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

    Args:
        username: profile username
        password: profile password
        type_user (Boolean): check to see if user has teacher rights

    Returns:
        : returns False if registering failed, calls login function if not
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
    return login(username, password)


def get_user_id():
    """Returns user id
    """
    return session.get("user_id", 0)


def get_user_type():
    """Returns user type (teacher or not)

    Returns:
        Boolean: False if user type is not teacher, True if is
    """
    id_user = session.get("user_id", 0)
    sql = text("SELECT teacher FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id": id_user})
    return result.fetchone()


def get_user_name(id_user):
    """Returns username
    """
    sql = text("SELECT username FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id": id_user})
    result_one = result.fetchone()
    if result_one is None:
        return False
    return result_one[0]

