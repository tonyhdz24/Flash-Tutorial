import functools

# What is a Blueprint?
# Blueprint is a way to organize a group of related views and other code. This is instead of registering views and other code directly with the app. Then the blueprint is registered with the app 
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash,generate_password_hash

from flaskr.db import get_db

# Creates a Blueprint with the name auth 
# Basically all views/endpoints will be registered with this blueprint such as views to register new users and log in and log out
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Code setting up the Register View, to be displayed when users navigate to /auth/register
# Note this route is registered with the blueprint bp and not the app
@bp.route('/register',methods=('GET','POST'))
def register():
    # Handles code for a POST request
    # A POST Request is usually used to add a new resource, it is not safe as it changes the state of the server(db) and is not idempotent by default
    if request.method == 'POST':
        # Get the username and password information from the form
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # Handle any errors
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        # If there are no errors then try and write to the db by sending a parameterized SQL query and committing it to the db
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered"
            # Once everything has been committed redirect to the login page
            else:
                return redirect(url_for("auth.login"))
            
        flash(error)
    return render_template('auth/register.html')

# Code for the Login view
@bp.route('/login', methods=('GET','POST'))
def login():
    # Handles post requests
    if request.method == 'POST':
        # Gets the username and password from the form
        username = request.form['username']
        password = request.form['password']
        # Gets the db
        db = get_db()
        error = None
        # SQL Query to get all users where the username is equal to the input username
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone() # Get only one row from the query results

        # Error handling 
        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        # When everything has run without an error
        if error is None:
            # session stores data across request. Session data is stored in a cookie that is sent to the browser
            # This will clear the session data and then store the users id in it that will let users refresh the page and stay logged in
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

"""
load_logged_in_user(): Checks to see if the the current user's ID matches the
"""
# registers a function that runs before the view function no matter what URL is requested 
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# To log out the user id has to be removed from the session so that load_logged_in_user will not load a user on subsequent requests
@bp.route('/logout')
def logout():
    session.clear() # Again calling clear() to remove session data
    return redirect(url_for('index'))

# Some views will only be accessible if a user is logged in so a decorator is used to check this before a view is displayed
"""
For this function we pass in a view that requires a user to be logged in
it returns a new view function that wraps the original view 
if no user is logged in then it redirects to the login page 
else it continues as normal
"""
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login')) # url_for generates a url for a passed in value
        return view(**kwargs)
    return wrapped_view