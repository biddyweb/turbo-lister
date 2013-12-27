from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from models import State

app = Flask(__name__)

from database import db_session
from database import init_db

init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/createcity/')
def createcity():
    res = db_session.query(State).filter_by(active=1).all()
    entries = [dict(name=row.name, id=row.id, active=row.active) for row in res]
    return render_template('createcity.html', entries=entries)

@app.route('/createcity/', methods=['POST'])
def add_entry():
    return redirect(url_for('success'))

@app.route('/success/')
def success():
    return "such and such added"
if __name__ == '__main__':
    app.debug = True
    app.run()