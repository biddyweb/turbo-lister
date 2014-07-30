from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import MethodView

from database import db_session
from models import State, City

import Objects


class SignInView(MethodView):
    
    def get(self):
        #check for user logged in session
        #username = session['username']
        
        #if username is None:
        #render cached index.
        jobs = None
        #else, we need to render our user's screen.
        headergen = Objects.HTMLSnippet('header').html
        footergen = Objects.HTMLSnippet('footer').html
        return render_template('signin.html', jobs=jobs, headergen=headergen, footergen=footergen)