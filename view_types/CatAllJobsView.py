from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import MethodView

from database import db_session
from models import State, City

from Objects import getCityDetails, getStateDetails
import Objects


class CatAllJobsView(MethodView):
    
    def get(self, cat):
        #check for user logged in session
        #username = session['username']
        
        #if username is None:
        #render cached index.
        jobs = None
        #else, we need to render our user's screen.
        headergen = render_template('header_gen.html')
        footergen = render_template('footer_gen.html')
        return render_template('cat_alljobs.html', jobs=jobs)