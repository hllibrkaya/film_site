import secrets
from flask import Flask, render_template, flash, redirect, url_for, session, request
from passlib.hash import sha256_crypt
from functools import wraps
from flask_paginate import Pagination

from modules.forms import RegisterForm, LoginForm, CommentForm
from modules.database import init_db, mysql, add_account, add_comment, user_control, get_films, movie_categories, \
    unique_control

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "cinemazing"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

app.config["DEBUG"] = True

init_db(app)


# decorator function for checking login status
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You must be logged in to view this page", "danger")
            return redirect(url_for("login"))

    return decorated_function


# The index page lists the most highly rated, recently added, and oldest movies.
@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM films ORDER BY score DESC LIMIT 6"
    cursor.execute(query)
    top = cursor.fetchall()
    query2 = "SELECT * FROM films ORDER BY date DESC LIMIT 6"
    cursor.execute(query2)
    recent = cursor.fetchall()
    query3 = "SELECT * FROM films WHERE year<2000 ORDER BY year ASC LIMIT 6"
    cursor.execute(query3)
    nostalgia = cursor.fetchall()

    return render_template("index.html", top=top, recent=recent, nostalgia=nostalgia)


# login function checks whether the entered username and password exist in the database(user_control function)
# and, based on this, maintains session information.
@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        if user_control(username, password):

            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "danger")
            return render_template("login.html", form=form)

    else:
        return render_template("login.html", form=form)


# clears session infos and logouts
@app.route("/logout")
def logout():
    session.clear()
    flash("Logout Successfull", "success")
    return redirect(url_for("index"))


#  registrer function checks whether the entered information is valid and
# whether the entered username or email address is already registered in the database(unique control function).
# also encrypts the password
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        gender = form.gender.data
        age = form.age.data
        password = sha256_crypt.encrypt(form.password.data)

        if unique_control(username, email):
            flash("Username or mail is already taken!", "danger")
            return render_template("register.html", form=form)

        add_account(name, username, email, gender, age, password)
        flash("Registiration successfull", "success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form)


@app.route("/about")
def about():
    return render_template("about.html")


# retrieves movie information from the database based on the movie's ID, lists the comments made for the movie
# and allows the user to add comments if they are logged in.
@app.route("/movie/<string:id>", methods=["GET", "POST"])
def movie(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM films WHERE id=%s"
    result = cursor.execute(query, (id,))
    if result > 0:
        movie = cursor.fetchone()

        query2 = "SELECT * FROM comments WHERE movie_id = %s"
        cursor.execute(query2, (id,))
        comments = cursor.fetchall()
        cursor.close()

        form = CommentForm(request.form)
        if request.method == "POST" and form.validate():
            comment = form.comment.data
            add_comment(id, comment)
            return redirect(request.url)
        return render_template("movie.html", movie=movie, comments=comments, form=form)
    else:
        return redirect(url_for("index"))


# lists all movies from the database and displays them with 24 movies per page.
@app.route("/movies")
def movies():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 24))

    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM films"
    cursor.execute(query)
    result = cursor.fetchone()
    total = result["COUNT(*)"]
    cursor.close()

    # Redirecting to the movies page in situations where,
    # for example, there are a total of 4 pages and the user tries to access "movies?page=5"
    total_pages = (total + per_page - 1) // per_page

    if page > total_pages:
        return redirect(url_for("movies"))

    offset = (page - 1) * per_page

    pagination_movies = get_films(offset=offset, per_page=per_page)

    pagination = Pagination(page=page, per_page=per_page, total=total)

    return render_template("movies.html", films=pagination_movies, page=page, per_page=per_page, pagination=pagination)


# finds and lists movies from the database based on the entered keyword
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM films WHERE title LIKE '%" + keyword + "%'"
        result = cursor.execute(query)

        if result > 0:
            sum = cursor.fetchall()
            cursor.close()
            total = len(sum)
            page = int(request.args.get("page", 1))
            # for showing all the results in 1 page, pagination is not needed but i had to use it for design issues
            per_page = total
            offset = (page - 1) * per_page
            films = sum[offset:offset + per_page]
            pagination = Pagination(page=page, per_page=per_page, total=total)
            return render_template("movies.html", films=films, pagination=pagination, page=page, per_page=per_page)
        else:
            cursor.close()
            flash("There is no such movie or it may have been deleted")
            return redirect(url_for("movies"))


# categorizes movies in the database based on their categories and lists them with 24 movies per page
@app.route("/movies/category/<string:category>")
def category(category):
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 24))
    offset = (page - 1) * per_page
    movies = movie_categories(category, offset=offset, per_page=per_page)

    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM films WHERE category = %s"
    cursor.execute(query, (category,))
    result = cursor.fetchone()
    total = result["COUNT(*)"]
    cursor.close()
    pagination = Pagination(page=page, per_page=per_page, total=total)

    return render_template("category.html", category=category, films=movies, pagination=pagination,
                           page=page, per_page=per_page)


if __name__ == '__main__':
    app.run()
