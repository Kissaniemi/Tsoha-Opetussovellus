"""Material related functions
    """

from sqlalchemy.sql import text
from db import db


def add_material(course_id, name, material):
    """Add material to the course
    """
    try:
        sql = text("INSERT INTO materials(name, material, course_id)\
                    VALUES(:name,:material,:course_id)")
        db.session.execute(sql,
                                {"name": name,
                                "material": material,
                                "course_id": course_id})

        db.session.commit()
    except BaseException:
        return False
    return True


def get_materials(course_id):
    """Get all course materials (related to the given course)
    """

    sql = text("SELECT id, name, material, course_id FROM materials WHERE course_id=:course_id ")
    result = db.session.execute(sql,
                                {"course_id": course_id})
    return result.fetchall()


def delete_material(material_id):
    """Deletes material with given id
    """
    try:
        sql = text("DELETE FROM materials WHERE id=:id")
        db.session.execute(sql,
                            {"id": material_id})
        db.session.commit()

    except BaseException:
        return False
    return True


def change_material(material_id, name, material):
    """Changes course info"""
    try:
        sql = text("UPDATE materials SET name=:name, material=:material WHERE id=:id")
        db.session.execute(sql, {"id": material_id,
                                 "name": name,
                                 "material": material})
        db.session.commit()

    except BaseException:
        return False
    return True


def get_material_info(material_id):
    """Returs all info of the material
    """
    sql = text("SELECT id, name, material, course_id FROM materials WHERE id=:id")
    result = db.session.execute(sql,
                                {"id": material_id})
    task = result.fetchone()
    if not task:
        return False
    return task


def get_max_id(course_id):
    """Returns the highest/(last) material_id of given course
    """
    sql = text("SELECT MAX(id) FROM materials WHERE course_id=:course_id")
    result = db.session.execute(sql,
                                {"course_id": course_id})
    return result.fetchone()[0]


def get_min_id(course_id):
    """Returns the smallest/(first) material_id of given course
    """
    sql = text("SELECT MIN(id) FROM materials WHERE course_id=:course_id")
    result = db.session.execute(sql,
                                {"course_id": course_id})
    return result.fetchone()[0]
