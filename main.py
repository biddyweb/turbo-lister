from flask import Flask, render_template
from models import State, City
import views

app = Flask(__name__)
app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/user/<username>', view_func=views.user)
app.add_url_rule('/new/<abbr>/<city>', view_func=views.newjob)
app.add_url_rule('/createcity', view_func=views.createcity)
app.add_url_rule('/jobs/<abbr>', view_func=views.jobsbystate)
app.add_url_rule('/jobs/<abbr>/<city>', view_func=views.jobsbycity)
app.add_url_rule('/jobs/<abbr>/<city>/alljobs', view_func=views.alljobscitystate)
app.add_url_rule('/jobs/<abbr>/<city>/<cat>', view_func=views.jobscitystatecat)
app.add_url_rule('/jobs/<abbr>/<city>/<cat>/<jid>', view_func=views.joblisting)
from database import db_session
from database import init_db

#init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    #test
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.debug = True
    app.run()