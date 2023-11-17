import os
import sqlalchemy
from db import db
from flask import abort, request, session
import users
import posts

def create_topic(topic):
    try:
        sql = """
            INSERT INTO topics (name)
            VALUES (:topic)"""
        db.session.execute(sql, {"topic":topic})
        db.session.commit()
    except:
        return False

    return True

def get_topics():
    try:
        sql = """
            SELECT id, name
            FROM topics
            """
        result = db.session.execute(sql).fetchall()
        return result
        
    except:
        return False