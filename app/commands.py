import click
from flask.cli import with_appcontext



@with_appcontext
def test():
    print("This is a test command")
