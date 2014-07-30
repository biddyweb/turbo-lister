from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import MethodView
from facebook import get_user_from_cookie, GraphAPI

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
        FB_APP_ID = 'none'
        FB_APP_SECRET = 'none'
        # https://github.com/pythonforfacebook/facebook-sdk/blob/master/examples/flask/app/views.py
        if session.get('user'):
            logged_in = 'yes'
            myaccountgen = render_template('myaccount_gen.html')
        else:
            logged_in = 'no'
            myaccountgen = ''
        result = get_user_from_cookie(cookies=request.cookies, app_id=FB_APP_ID,
                                  app_secret=FB_APP_SECRET)
        if result:
            fb_in = result['uid']
        else:
            fb_in = 'none'
        #else, we need to render our user's screen.
        
        #This stuff should be in cache later.
        states = Objects.AllStatesIndex()
        states = sorted(states.states, key=lambda k: k.id)
        allcats = Objects.AllCats()
        allcats = allcats.cats
        
        #we need to get the generated header.
        #this should be in cache, but for now it's not.
        headergen = render_template('header_gen.html')
        footergen = render_template('footer_gen.html')
        
        return render_template('index2.html', allstates=states, 
                               li=logged_in, fb=fb_in, headergen=headergen, footergen=footergen, myaccountgen=myaccountgen, allcats=allcats)
        #return render_template('index.html', states=states)