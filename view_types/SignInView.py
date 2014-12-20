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
        #render login form.

        #if user is logged in
        #send to index.

        jobs = None
        #else, we need to render our user's screen.
        headergen = Objects.HTMLSnippet('header').html
        footergen = Objects.HTMLSnippet('footer').html
        return render_template('signin.html', jobs=jobs, headergen=headergen, footergen=footergen)

    def post(self):
        #check for user logged in session
        #username = session['username']
        #if user is logged in, send to index.

        #check for form data
        myusername = request.form.get('username')
        mypassword = request.form.get('password')
        mytoken = request.form.get('logintoken')

        #make sure we have everything
        if myusername is None or mypassword is None or mytoken != 'mytoken':
            #flash bad signin.
            return 'not enough form data'
            #return render_template('signin.html', jobs=jobs, headergen=headergen, footergen=footergen)

        #get user object (userid, username, and pw)
        myUserObject = Objects.UserSignIn(myusername)
        #if no user object, return to signin.
        if myUserObject.id is None:
            #flash bad signin.
            return render_template('signin.html', jobs=jobs, headergen=headergen, footergen=footergen)
        #check password
        if myUserObject.checkpw(mypassword) is True:
            #if good, set session, thank your for signing in.
            session['username'] = myUserObject.email
            session['userid'] = myUserObject.id
            flash('Thank you for signing in.')
            return redirect(url_for('index'))
        #if bad, render signin.

        headergen = Objects.HTMLSnippet('postheader').html
        footergen = Objects.HTMLSnippet('footer').html
        return render_template('signin.html', jobs=jobs, headergen=headergen, footergen=footergen)