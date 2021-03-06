from flask import Flask, render_template
from models import State, City
import views

app = Flask(__name__)
app.config.from_object('config.Config')
#Max upload is 32k to prevent malicious uploads from jamming up the server.
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024

#app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/user/<username>', view_func=views.user)
#app.add_url_rule('/new/<abbr>/<city>', view_func=views.newjob)
app.add_url_rule('/createcity', view_func=views.createcity)
app.add_url_rule('/jobs/<abbr>', view_func=views.jobsbystate)
#app.add_url_rule('/jobs/<abbr>/<city>', view_func=views.jobsbycity)
#app.add_url_rule('/jobs/<abbr>/<city>/alljobs', view_func=views.alljobscitystate)
#app.add_url_rule('/jobs/<abbr>/<city>/<cat>', view_func=views.jobscitystatecat)
#app.add_url_rule('/jobs/<abbr>/<city>/<cat>/<jid>', view_func=views.joblisting)

from view_types.IndexView import IndexView
indexview = IndexView.as_view('index')
app.add_url_rule('/', view_func=indexview, methods=['GET','POST'])

from view_types.StateHomeView import StateHomeView
statehomeview = StateHomeView.as_view('statehome')
app.add_url_rule('/<abbr>', view_func=statehomeview, methods=['GET', 'POST'])

from view_types.CityHomeView import CityHomeView
cityhomeview = CityHomeView.as_view('cityhome')
app.add_url_rule('/<abbr>/<city>', view_func=cityhomeview, methods=['GET', 'POST'])

from view_types.CatAllJobsView import CatAllJobsView
catalljobsview = CatAllJobsView.as_view('catalljobsview')
app.add_url_rule('/alljobs/<cat>', view_func=catalljobsview, methods=['GET', 'POST'])

from view_types.SignInView import SignInView
signinview = SignInView.as_view('signinview')
app.add_url_rule('/signin', view_func=signinview, methods=['GET', 'POST'])

from view_types.SignOutView import SignOutView
signoutview = SignOutView.as_view('signoutview')
app.add_url_rule('/signout', view_func=signoutview, methods=['GET'])

from view_types.PostJobView import PostJobView
postjobview = PostJobView.as_view('postjobview')
app.add_url_rule('/postjob', view_func=postjobview, methods=['GET'])
app.add_url_rule('/postjob', view_func=postjobview, methods=['POST'])

from view_types.SubmitJobView import SubmitJobView
submitjobview = SubmitJobView.as_view('submitjobview')
app.add_url_rule('/submitjob', view_func=submitjobview, methods=['GET'])
app.add_url_rule('/submitjob', view_func=submitjobview, methods=['POST'])

from database import db_session
from database import init_db
 
init_db()

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