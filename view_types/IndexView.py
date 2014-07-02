from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import MethodView


from database import db_session
from models import State, City

from Objects import getAllStates
import Objects

class IndexView(MethodView):
    
    def get(self):
        #check for user logged in session
        #username = session['username']
        
        #if username is None:
        #render cached index.
        
        #else, we need to render our user's screen.
        states = Objects.AllStatesIndex()
        states = sorted(states.states, key=lambda k: k.id)
        
        
        return render_template('index2.html', allstates=states)
        #return render_template('index.html', states=states)