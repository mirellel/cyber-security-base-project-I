import os
from db import db
from flask import abort, request, session
import users

def create_post(title, content, user_id, topic_id, visibility):
    try:
        sql = """INSERT INTO titles (title, content, posted_by, topic_id, visibility) 
                VALUES (:title, :content, :posted_by, :topic_id, :visibility)"""
        db.session.execute(sql, {"title":title, "content":content, 
                                "posted_by":user_id, "topic_id":topic_id, 
                                "visibility":visibility})
        db.session.commit()
    except:
        return False

    return True

def get_all_posts():
    try:
        sql = """SELECT id, title, content, TO_CHAR(posted_at, \'HH24:MI, Mon dd yyyy\'), posted_by, topic_id, visibility 
                 FROM titles 
                 ORDER BY posted_at DESC"""
        result = db.session.execute(sql)
        all_posts = result.fetchall()
        return all_posts
    except:
        return False

def get_title_info(title_id):
    sql_likes = """(SELECT COUNT(l.id) FROM likes l WHERE t.id = l.title_id)"""
    sql = f"""SELECT t.title, u.username, t.content, TO_CHAR(t.posted_at, \'HH24:MI, Mon dd yyyy\'), {sql_likes} 
            FROM titles t, users u WHERE t.id=:title_id AND t.posted_by=u.id"""
    return db.session.execute(sql, {"title_id": title_id}).fetchone()


def get_post_count():
    try:
        sql = """
            SELECT COUNT(id)
            FROM titles
            WHERE visibility=TRUE
            """
        post_count = db.session.execute(sql).fetchall()
        return post_count
    except:
        return False

def delete_title(title_id):
    sql = """UPDATE titles SET visibility=FALSE WHERE id=:id"""
    db.session.execute(sql, {"id":title_id})
    db.session.commit()

    return True

def get_titles_by_topic(topic_id):
    sql = """SELECT id, title, content, TO_CHAR(posted_at, \'HH24:MI, Mon dd yyyy\'), posted_by, topic_id, visibility
            FROM titles
            WHERE topic_id=:topic_id"""
    return db.session.execute(sql, {"topic_id": topic_id}).fetchall()

def like_post(title_id, liker_id):
    sql = "INSERT INTO likes (title_id, liker_id) VALUES (:title_id, :liker_id)"
    db.session.execute(
        sql, {"title_id": title_id, "liker_id": liker_id})
    db.session.commit()


def has_user_liked_post(title_id, liker_id):
    sql = "SELECT id, liker_id, title_id FROM likes WHERE title_id =:title_id AND liker_id=:liker_id"
    message = db.session.execute(
        sql, {"title_id": title_id, "liker_id": liker_id}).fetchall()

    if len(message) == 0:
        return True
    else:
        return False

def get_like_count():
    sql = """SELECT title_id, COUNT(title_id)
            FROM likes
            GROUP BY title_id"""
    like_count = db.session.execute(sql).fetchall()
    return like_count


def restore_deleted_post(title_id):
    sql = """UPDATE titles SET visibility=TRUE WHERE id=:id"""
    db.session.execute(sql, {"id":title_id})
    db.session.commit()

    return True
