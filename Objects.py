from flask import abort, render_template
from werkzeug.contrib.cache import MemcachedCache

# http://stackoverflow.com/questions/10016499/nginx-with-flask-and-memcached-returns-some-garbled-characters
cache = MemcachedCache(['127.0.0.1:11211'])

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
        self.urlname = name.replace(" ", "_").lower()
        
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
        self.html = getHTMLByName(snippet)
        if self.html is None:
            self.html = render_template(snippet + '_gen.html')
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
    #Retrieve an object of all states, etc.
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