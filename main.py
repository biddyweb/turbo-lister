from flask import Flask
from models import State, City
import views

app = Flask(__name__)

app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/user/<username>', view_func=views.user)
app.add_url_rule('/createcity', view_func=views.createcity)

from database import db_session
from database import init_db

#init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.debug = True
    app.run()