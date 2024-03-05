import os
from unittest import result
from db import db
from flask import abort, request, session
import users
import posts

def create_comment(comment, title_id, username, visibility):
    try:
        sql = """INSERT INTO comments (comment, title_id, commentor, visibility)
                VALUES (:comment, :title_id, :commentor, :visibility)"""
        db.session.execute(sql, {"comment":comment, "title_id":title_id,
                            "commentor":username, "visibility":visibility})
        db.session.commit()

    
    except:
        return False

    return True

def get_commentor(comment_id):
    sql = """SELECT FROM COMMENTS commentor WHERE id=:comment_id"""
    commentor = db.session.execute(sql, {"comment_id":comment_id}).fetchall()
    return commentor

def get_comments(title_id):
    try:
        sql = """
            SELECT comment, title_id, commentor, TO_CHAR(sent_at, \'HH24:MI, Mon dd yyyy\'), visibility, id
            FROM comments
            WHERE title_id=:title_id"""
        result=db.session.execute(sql, {"title_id": title_id}).fetchall()
        return result
    except:
        return False

def get_number_of_comments(title_id):
    try:
        sql = """
            SELECT COUNT(comment)
            FROM comments
            WHERE title_id=:title_id AND visibility=TRUE"""
        number_of_comments = db.session.execute(sql,{"title_id": title_id}).fetchall()
        return number_of_comments
    except:
        return False

def get_comment_count():
    try:
        sql = """
            SELECT title_id, COUNT(title_id)
            FROM comments
            WHERE visibility=TRUE
            GROUP BY title_id"""
        comment_count = db.session.execute(sql).fetchall()
        return comment_count
    except:
        return False

# Injection
def delete_comment(id):
    sql = f"DELETE FROM comments WHERE id='{id}'"
    db.session.execute(sql)
    db.session.commit()

    # fix
    # sql = """DELETE FROM comments WHERE id=:id"""
    # db.session.execute(sql, {"id":id})
    # db.session.commit()

    return True

def restore_comment(comment_id):
    sql = """UPDATE comments SET visibility=TRUE WHERE id=:id"""
    db.session.execute(sql, {"id":comment_id})
    db.session.commit()

    return True