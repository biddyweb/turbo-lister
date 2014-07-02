from flask import abort
from werkzeug.contrib.cache import MemcachedCache

# http://stackoverflow.com/questions/10016499/nginx-with-flask-and-memcached-returns-some-garbled-characters
cache = MemcachedCache(['127.0.0.1:11211'])

class States():
    id = None
    states = None
    abbrs = None
    ids = None
    cityids = None
    cities = dict()

        
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
        
class AllStatesIndex():
    #dict of ids
    #( id : (name : x, abbr : x, cities : (id : x, name : x) )
    states = list()
    def __init__(self):
        self.states = getAllStates()
        
def testCache():
    if cache.get('iswarm') is None:
        abort(500, "Cache dead")
 
def getAllStates():
    #Retrieve an object of all states, etc.
    #allstates = dict ( state_id : (name : x, abbr : x, cities : (city_id : x, name : x) ) )
    testCache()
    return cache.get('allstates')

def getStateIdByAbbr(abbr):
    return cache.get('abbr:' + abbr)

def getStateNameById(stateid):
    return cache.get('states:' + str(stateid) + ':name')

def getStateCities(stateid):
    return cache.get('states:' + str(stateid) + ':cities')

def getCityDict(cityids):
    myresults = dict()
    for id in cityids:
        myresults[id] = cache.get('city:' + str(id) + ':name')
    return myresults