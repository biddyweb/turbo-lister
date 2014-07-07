from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import MethodView

from database import db_session
from models import State, City

from Objects import getStateIdByAbbr, getStateCities, getStateDetailsByAbbr
import Objects


class StateHomeView(MethodView):
    
    def get(self, abbr):
        #check for user logged in session
        #username = session['username']
        
        #if username is None:
        #render cached index.
        
        #else, we need to render our user's screen.
        
        abbr = abbr.upper()
        myState = getStateDetailsByAbbr(abbr)         
        flash(myState.name)
        return render_template('state_home.html', state=myState)