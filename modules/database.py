from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from flask import session

mysql = MySQL()


# for database and app connection
def init_db(app):
    mysql.init_app(app)


# adding user row to database
def add_account(name, username, email, gender, age, password):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO USERS(name,username,email,gender,age,password) VALUES (%s, %s, %s,%s,%s,%s)"
    cursor.execute(query, (name, username, email, gender, age, password))
    mysql.connection.commit()
    cursor.close()


# adding comment info to database
def add_comment(movie_id, comment):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO comments(author, movie_id,comment) VALUES (%s, %s, %s)"
    cursor.execute(query, (session["username"], movie_id, comment))
    mysql.connection.commit()
    cursor.close()


# checking the correctness of the username and the encrypted password
def user_control(username, password):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE username =%s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    if user is None:
        return False
    else:
        enc_pswd = user["password"]
        if sha256_crypt.verify(password, enc_pswd):
            return True
        else:
            return False


# accessing movies in the database
def get_films(offset=0, per_page=24):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM films ORDER BY id LIMIT %s OFFSET %s"
    cursor.execute(query, (per_page, offset))
    films = cursor.fetchall()
    cursor.close()
    return films


# accessing movie categories
def movie_categories(category, offset=0, per_page=24):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM films WHERE category =%s ORDER BY id LIMIT %s OFFSET %s"
    cursor.execute(query, (category, per_page, offset))
    films = cursor.fetchall()
    cursor.close()
    return films


# checking whether the entered username or email address is already used
def unique_control(username, email):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE username = %s OR email = %s"
    cursor.execute(query, (username, email))
    existing_user = cursor.fetchone()
    cursor.close()
    return existing_user is not None
