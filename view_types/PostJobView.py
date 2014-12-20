from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import MethodView


import Objects
import uuid
import UserCache


class PostJobView(MethodView):

        
    #No data has been submitted.
    def get(self):
        #check for user logged in session
        username = session.get('username')
        
        if username is None:
          flash('you must be logged in to view this area')
          return redirect(url_for('signinview'))
        
        #else, we need to render our user's screen.
        editortext = "[b]Enter your job description here[/b]. [color=#B22222]Javascript and HTML are prohibited[/color]. [color=#008000]BBCode is valid.[/color]"
        parser = Objects.updateParser()
        previewtext = parser.format(editortext)
        headergen = Objects.HTMLSnippet('postheader').html
        footergen = Objects.HTMLSnippet('footer').html
        return render_template('postjob.html', headergen=headergen, footergen=footergen, editortext=editortext)
    
    #User pressed preview
    def post(self):
        #check for user logged in session
        username = session.get('username')

        if username is None:
          flash('you must be logged in to view this area')
          return redirect(url_for('signinview'))
        
        #generate a UUID for this text, and save to memcached.
        myuuid = request.form.get('postuuid')
        if myuuid is None:
            myuuid = uuid.uuid4().hex
            
        jobtext = request.form.get('jobtext')
        myPostCache = UserCache.UserObject('101')
        #obtype, obid, obdata
        myPostCache.put('post',myuuid,jobtext)
        #Add extensions to bbCode parser.
        parser = Objects.updateParser()
        
        #if username is None:
        #render cached index.
        #previewtext = bbcode.render_html(jobtext)
        previewtext = parser.format(jobtext)
        #else, we need to render our user's screen.
        headergen = Objects.HTMLSnippet('postheader').html
        footergen = Objects.HTMLSnippet('footer').html
        return render_template('postjob.html', headergen=headergen, footergen=footergen, editortext=jobtext, previewtext=previewtext, postuuid=myuuid)
        