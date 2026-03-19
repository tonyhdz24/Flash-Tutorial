Flaskr
======

The basic blog app built in the Flask `tutorial`_.

.. _tutorial: https://flask.palletsprojects.com/tutorial/
Install
-------
Run the following commands ::

    # clone the repository
    $ git clone https://github.com/tonyhdz24/Flask-Tutorial
    $ cd Flask-Tutorial


Create a virtualenv and activate it::

    $ python3 -m venv .venv
    $ . .venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv .venv
    $ .venv\Scripts\activate.bat

Install Flaskr::

    $ pip install -e .

Run
---

.. code-block:: text

    $ flask --app flaskr init-db
    $ flask --app flaskr run --debug

Open http://127.0.0.1:5000 in a browser.


Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
