from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import MethodView

from database import db_session
from models import State, City

from Objects import getCityDetails, getStateDetails
import Objects


class CityHomeView(MethodView):
    
    def get(self, abbr, city):
        #check for user logged in session
        #username = session['username']
        
        #if username is None:
        #render cached index.
        
        #else, we need to render our user's screen.
        headergen = render_template('header_gen.html')
        footergen = render_template('footer_gen.html', tester="<h3>hello</h3>")
        abbr = abbr.upper()
        myCity = getCityDetails(abbr, city)
        if myCity is None:
            abort(500, 'bad city provided')
        myState = getStateDetails(myCity.stateid)
        if myState is None:
            abort(500, 'no state found' + str(myCity.stateid))
        flash(myCity.name)
        return render_template('city_home.html', city=myCity, state=myState, headergen=headergen, footergen=footergen)