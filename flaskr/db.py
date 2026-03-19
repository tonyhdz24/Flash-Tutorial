import sqlite3
from datetime import datetime

# Click is a python package that let you basically write C
import click

# g: A special obj unique to each request. Used to store data that might be accessed by multiple functions during the request. The connection is stored and reused instead of creating a new connection if get_db is called a second time in the same request. 
# => Overall it is a good place to store resources during a request such g.user to get the user 

# current_app: A proxy to the application handling the current request. Useful to accss the app without needing to import it
# => Basically it points to the Flask app handling the request. In this case since we are using an app func/factory there is no app obj when writing the rest of the code. 
from flask import current_app, g


"""
get_db() Function returns the db we are using and if it does not already exist it creates a connection to it 
"""
def get_db():
    if 'db' not in g:
        # Connect the the database file pointing at by 'DATABASE'
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Tells the connection to return rows that behave like dicts
        g.db.row_factory = sqlite3.Row
    return g.db

"""
Closes down the db if a connection has been made
"""
def close_db(e=None):
    db = g.pop('db',None)
    if db is not None:
        db.close()

"""
Initializes the database
"""
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    # Clear existing data and create new tables
    init_db()
    click.echo('Initialized the database')

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

# Registering the init_db and close_db with the actual flask app
def init_app(app):
    app.teardown_appcontext(close_db) # when the flask app is closing done call the close_db()
    app.cli.add_command(init_db_command) # Adds the init_db_command that can be called with the flask cmd