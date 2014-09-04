from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import MethodView


import Objects
import UserCache


class SubmitJobView(MethodView):

        
    #No data has been submitted; this shouldn't be the case.
    def get(self):
        flash('Invalid Page Request')
        return redirect('/')
    
    #User pressed Post! on create new job page.
    def post(self):
        #check for user logged in session
        #username = session['username']
        
        #generate a UUID for this text, and save to memcached.
        myuuid = request.form.get('postuuid')
        if myuuid is None:
            myuuid = uuid.uuid4().hex
        myPostCache = UserCache.UserObject('101')
        jobtext = myPostCache.get('post',myuuid)
        parser = Objects.updateParser()
        previewtext = parser.format(jobtext)
        headergen = Objects.HTMLSnippet('postheader').html
        footergen = Objects.HTMLSnippet('footer').html
        return render_template('submitjob.html', headergen=headergen, footergen=footergen, previewtext=previewtext)
        