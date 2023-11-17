import os
import secrets
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password, id, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
        
    session["user_id"] = user[1]
    session["username"] = username
    session["user_role"] = user[2]
    session["csrf_token"] = secrets.token_hex(16)
    return True

def logout():
    del session["user_id"]
    del session["username"]
    del session["user_role"]

def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql= """INSERT INTO users (username, password, role)
                VALUES (:username, :password, :role)"""
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    return login(username, password)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def user_id():
    return session.get("user_id", 0)

def posts_made_by_user(user_id):
    try:
        sql= """
            SELECT COUNT(posted_by)
            FROM titles
            WHERE posted_by=:posted_by"""
        num_of_posts=db.session.execute(sql, {"posted_by": user_id}).fetchone()
        return num_of_posts
    except:
        return False

def comments_made_by_user(username):
    try:
        sql= """
            SELECT COUNT(commentor)
            FROM comments
            WHERE commentor=:commentor"""
        num_of_comments=db.session.execute(sql, {"commentor": username}).fetchone()
        return num_of_comments
    except:
        return False


def get_users_deleted_posts(user_id):
    try:
        sql = """
            SELECT id, title, content, TO_CHAR(posted_at, \'HH24:MI, Mon dd yyyy\')
            FROM titles
            WHERE posted_by=:posted_by AND visibility=FALSE"""
        deleted_posts = db.session.execute(sql, {"posted_by": user_id}).fetchall()
        return deleted_posts
    except:
        return False

def get_users_deleted_comments(username):
    try:
        sql = """
            SELECT id, comment, TO_CHAR(sent_at, \'HH24:MI, Mon dd yyyy\')
            FROM comments
            WHERE commentor=:commentor AND visibility=FALSE"""
        deleted_comments = db.session.execute(sql, {"commentor": username}).fetchall()
        return deleted_comments
    except:
        return False