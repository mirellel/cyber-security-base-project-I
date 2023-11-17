from app import app
from flask import render_template, request, redirect
import users
import posts
import comments
import topics

@app.route("/")
def index():
    all_posts = posts.get_all_posts()
    post_count = posts.get_post_count()
    comment_count = comments.get_comment_count()
    like_count = posts.get_like_count()
    if all_posts!=False:
        return render_template("index.html", all_posts=all_posts, 
        post_count=post_count[0],
        comment_count=comment_count,
        like_count=like_count)
    else:
        return render_template("error.html")


@app.route("/login",methods=["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]

		if not users.login(username, password):
			return render_template("error.html", message="Väärä tunnus tai salasana!")
		return redirect("/")

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username)<1 or len(username)>20:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-20 merkkiä")

        if " " in username:
            return render_template("error.html", message="Tunnuksessa ei saa olla välilyöntejä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")

        if password1 == "":
            return render_template("error.html", message="Salasana on tyhjä")

        if " " in password1:
            return render_template("error.html", message="Salasanassa ei saa olla välilyöntejä")

        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("error.html", message="Tuntematon käyttäjärooli")
        
        if not users.register(username, password1, role):
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        return redirect("/")

@app.route("/account", methods=["GET","POST"])
def access_account():
    # users.check_csrf()
    user_id = request.form["user_id"]
    username = request.form["username"]
    if request.method == "GET":
        return render_template("account.html")
    if request.method =="POST":
        num_of_posts = users.posts_made_by_user(user_id)
        num_of_comments = users.comments_made_by_user(username)
        deleted_posts = users.get_users_deleted_posts(user_id)
        deleted_comments = users.get_users_deleted_comments(username)
        return render_template("account.html", num_of_posts=num_of_posts, num_of_comments=num_of_comments, 
        deleted_posts=deleted_posts, deleted_comments=deleted_comments)

@app.route("/create", methods=["GET", "POST"])
def new_title():
    if request.method =="GET":
        return render_template("create.html")

    if request.method == "POST":
        return redirect("/")

@app.route("/new", methods=["GET", "POST"])
def created():
    all_topics = topics.get_topics()
    if request.method == "GET":
        return render_template("new.html", all_topics=all_topics)
    if request.method == "POST":
        users.check_csrf()
        title = request.form["title"]
        comment = request.form["comment"]
        id=request.form["user_id"]
        topic=request.form["topic"]
        if title == "" or title.isspace():
            return render_template("error.html", message="Otsikko ei saa olla tyhjä!")
        if comment == "" or  comment.isspace():
            return render_template("error.html", message="Aloituskommentti ei saa olla tyhjä!")
        if not posts.create_post(title, comment, id, topic, True):
            return render_template("error.html", message="Postauksen luonti ei onnistunut")

        return redirect("/create")

@app.route("/delete_title", methods=["GET", "POST"])
def delete_title():
    # users.check_csrf()
    title_id = request.form["title_id"]
    try:
        posts.delete_title(title_id)
    except:
        return render_template("error.html", message="Viestin postaminen epäonnistui")

    return redirect("/")

@app.route("/restore_post", methods=["GET", "POST"])
def restore_post():
    # users.check_csrf()
    title_id = int(request.form["title_id"])
    try:
        posts.restore_deleted_post(title_id)
    except:
        return render_template("error.html", message="Viestin palauttaminen epäonnistui")
    return redirect("/")

@app.route("/post/<int:title_id>")
def show_title(title_id):
    info = posts.get_title_info(title_id)
    post_comments = comments.get_comments(title_id)
    num_of_comments = comments.get_number_of_comments(title_id)
    
    return render_template("post.html", id=title_id, 
    name=info[0], posted_by=info[1], 
    content=info[2], posted_at=info[3], 
    post_comments=post_comments,
    num_of_likes = info[4],
    num_of_comments=num_of_comments[0])

@app.route("/new_comment", methods=["GET", "POST"])
def comment():
    # users.check_csrf()
    if request.method == "GET":
        return render_template("post/<int:title_id>")
    if request.method == "POST":
        comment = request.form["comment"]
        commentor = request.form["commentor"]
        post_id =  request.form["title_id"]

        if comment == "" or  comment == "    ":
            return render_template("error.html", message="Kommentti ei saa olla tyhjä!")
        
        if not comments.create_comment(comment, post_id, commentor, True):
            return render_template("error.html", message="Kommentin luonti ei onnistunut")

        return redirect("/post/"+post_id)

@app.route("/delete_comment", methods=["GET", "POST"])
def delete_comment():
    # users.check_csrf()
    comment_id = request.form["comment_id"]
    post_id =  request.form["title_id"]
    try:
        comments.delete_comment(comment_id)

    except:
        return render_template("error.html", message="Kommentin postaminen epäonnistui")
    return redirect("/post/"+post_id)


@app.route("/restore_comment", methods=["GET", "POST"])
def restore_comment():
    # users.check_csrf()
    comment_id = request.form["comment_id"]
    try:
        comments.restore_comment(comment_id)
    except:
        return render_template("error.html", message="Kommentin palauttaminen epäonnistui")
    return redirect("/")


@app.route("/topics", methods=["GET", "POST"])
def show_topics():
    all_topics = topics.get_topics()

    return render_template("topics.html", topics=all_topics)

@app.route("/topic/<int:topic_id>")
def show_titles_by_topic(topic_id):
    titles = posts.get_titles_by_topic(topic_id)

    return render_template("topic.html", id=topic_id, titles=titles)

@app.route("/add_topic", methods=["GET", "POST"])
def add_topic():
    # users.check_csrf()
    if request.method =="GET":
        return render_template("/topics")

    if request.method == "POST":
        name = request.form["new_topic"]
        if name == "":
            return render_template("error.html", message="Aihe ei saa olla tyhjä")

        if not topics.create_topic(name):
            return render_template("error.html", message="Aiheen luominen ei onnistunut")
        
        return redirect("/topics")

@app.post("/like_message")
def like_title():
    # users.check_csrf()
    title_id = request.form["title_id"]

    if users.user_id()>0:
        liker_id = users.user_id()
        if not posts.has_user_liked_post(title_id, liker_id):
            return render_template("error.html", message="Et voi tykätä samasta viestistä kahdesti")
        else:
            posts.like_post(title_id, liker_id)
            return redirect(f"/post/{title_id}")