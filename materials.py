"""Material related functions
    """

from sqlalchemy.sql import text
from db import db


def add_material(course_id, name, material):
    """Add material to the course
    """
    try:
        sql = text("INSERT INTO materials(name, material, course_id) VALUES(:name,:material,:course_id)")
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


def get_material_info(id):
    sql = text("SELECT id, name, material, course_id FROM materials WHERE id=:id ")
    result = db.session.execute(sql, 
                                {"id": id})
    return result.fetchone()
