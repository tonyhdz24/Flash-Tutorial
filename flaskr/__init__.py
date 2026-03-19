import os
from flask import Flask
# """
# This file contains a function to create and return a Flask app  
# """
def create_app(test_config=None):
    # Creates the Flask instance
        # __name_ is the name of the current python module. It changes dependign on whether the file is executed as the MAIN program or imported as a module into another script
        # instance_relative_config: Tells the app the all the config files are relative to the instance folder
    app = Flask(__name__, instance_relative_config=True)

    # Sets some default configs that the app will use. Such as the SECRET KEY to keep data safe & DATABASE which is the path to the where the database file will be saved
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # Checks if a test config file has been passed in
    if test_config is None:
        # Load the instance config if it exits when not testing
        app.config.from_pyfile('config.py',silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    os.makedirs(app.instance_path,exist_ok=True)

    # Simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello world!'
    
    # Importing the database functions to:
    # 1. Init the db
    # 2. Close the db
    # 3. Register the db with the app
    from . import db
    db.init_app(app)

    # Importing the auth blueprint with the app
    from . import auth
    app.register_blueprint(auth.bp)

    # Importing the blog blueprint and register it with the app
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app
