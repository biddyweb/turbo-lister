from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import MethodView


import Objects
import uuid
import UserCache


class PostJobView(MethodView):
    def updateParser(self):
        def render_size(name, value, options, parent, context):
            if 'size' in options:
                size = options['size'].strip()
            elif options:
                size = list(options.keys())[0].strip()
            else:
                return value
            match = re.match(r'^([0-9]+)', size, re.I)
            size = match.group() if match else 'inherit'
            return '<font size=%(size)s>%(value)s</font>' % {
                'size': size,
                'value': value,
            }
        parser = bbcode.Parser(replace_links=False)
        parser.add_simple_formatter('img', '<img src=%(value)s ></img>')
        parser.add_simple_formatter('rtl', '<div style="direction: rtl;">%(value)s</div>')
        parser.add_simple_formatter('ltr', '<div style="direction: ltr;">%(value)s</div>')
        parser.add_simple_formatter('li', '<li></li>')
        parser.add_formatter('size', render_size)
        return parser
        
    #No data has been submitted.
    def get(self):
        #check for user logged in session
        #username = session['username']
        
        #if username is None:
        #flash not logged in
        #render sign in page.
        
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
        #username = session['username']
        
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
        