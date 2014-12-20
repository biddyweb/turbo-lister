from flask import abort, render_template
from werkzeug.contrib.cache import MemcachedCache
from werkzeug.security import generate_password_hash, check_password_hash

from database import db_session
from models import User

import bbcode
import re
# http://stackoverflow.com/questions/10016499/nginx-with-flask-and-memcached-returns-some-garbled-characters
cache = MemcachedCache(['127.0.0.1:11211'])

class UserPassword(object):
    id = None

    def __init__(self, password):
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password,method='pbkdf2:sha256:1000')

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

class UserSignIn(object):
    def __init__(self, username):
        res = db_session.query(User.id, User.email, User.password).filter_by(email=username).one();
        self.id = res.id
        self.email = res.email
        self.pw_hash = res.password

    def checkpw(self, password):
        return check_password_hash(self.pw_hash, password)



class State():
    id = None
    name = None
    abbr = None
    cityids = None
    cities = dict()
    
class City():
    id = None
    stateid = None
    name = None
    
class Cat():
    id = None
    name = None
    urlname = None
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.urlname = name.replace(" ", "_").lower().replace(",", "")
        
class StateHomePage():
    name = None
    abbr = None
    id = None
    cityids = set()
    citydict = dict()
    def __init__(self, abbr):  
        testCache()      
        self.abbr = abbr
        self.id = getStateIdByAbbr(self.abbr)
        if self.id is None:
            abort(404, "Invalid State Selection")
        self.name = getStateNameById(self.id)
        self.cityids = getStateCities(self.id)
        self.citydict = getCityDict(self.cityids)
        
class CityHomePage():
    name = None
    abbr = None
    id = None
    cityids = set()
    citydict = dict()
    def __init__(self, abbr):  
        testCache()      
        self.abbr = abbr
        self.id = getStateIdByAbbr(self.abbr)
        if self.id is None:
            abort(404, "Invalid State Selection")
        self.name = getStateNameById(self.id)
        self.cityids = getStateCities(self.id)
        self.citydict = getCityDict(self.cityids)

class HTMLSnippet():
    html = None
    def __init__(self, snippet):
        testCache()
        #self.html = getHTMLByName(snippet)
        if self.html is None:
            self.html = render_template(snippet + '_gen.html')
            cache.set('html:' + snippet, self.html)
            
class HTMLLeftSideBar():
    html = None
    allcats = None
    def __init__(self, snippet):
        testCache()
        self.html = getHTMLByName(snippet)
        self.allcats = AllCats().cats
        if self.html is None:
            states = AllStatesIndex()
            states = sorted(states.states, key=lambda k: k.id)
            leftlist = list()
            rightlist = list()
            count = 0
            for cat in self.allcats:
                if count % 2 == 0:
                    leftlist.append(cat)
                    #print cat
                else:
                    rightlist.append(cat)
                    #print cat
                count += 1


            self.html = render_template(snippet + '_gen.html', leftcats=leftlist, rightcats=rightlist)
            cache.set('html:' + snippet, self.html)
            
class HTMLRightSideBar():
    html = None
    def __init__(self, snippet):
        testCache()
        self.html = getHTMLByName(snippet)
        if self.html is None:
            states = AllStatesIndex()
            states = sorted(states.states, key=lambda k: k.id)
            self.html = render_template(snippet + '_gen.html', allstates=states)
            cache.set('html:' + snippet, self.html)
         
class AllStatesIndex():
    #dict of ids
    #( id : (name : x, abbr : x, cities : (id : x, name : x) )
    states = list()
    def __init__(self):
        self.states = getAllStates()

class AllCats():
    cats = list()
    def __init__(self):
        self.cats = getAllCats()
        
def testCache():
    if cache.get('iswarm') is None:
        abort(500, "Cache dead")
 
def getAllStates():
    #Retrieve an object of all states, etc.owse al
    #allstates = dict ( state_id : (name : x, abbr : x, cities : (city_id : x, name : x) ) )
    testCache()
    return cache.get('allstates')

def getAllCats():
    testCache()
    return cache.get('allcats')

def getHTMLByName(snippet):
    return cache.get('html:' + snippet)

def getStateIdByAbbr(abbr):
    return cache.get('abbr:' + abbr)

def getStateNameById(stateid):
    return cache.get('states:' + str(stateid) + ':name')

def getStateDetails(stateid):
    testCache()
    return cache.get('states:' + str(stateid) + ':details')

def getStateDetailsByAbbr(abbr):
    testCache()
    stateid = getStateIdByAbbr(abbr)
    return getStateDetails(stateid)

def getCityDetails(abbr, name):
    testCache()
    return cache.get('city:' + abbr + ':' + name + ':details')

def getStateCities(stateid):
    return cache.get('states:' + str(stateid) + ':cities')

def getCityDict(cityids):
    myresults = dict()
    for id in cityids:
        myresults[id] = cache.get('city:' + str(id) + ':name')
    return myresults

def getCityIdByName(stateid, name):
    return cache.get(stateid + ':' + name)

def updateParser():
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