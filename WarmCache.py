from database import db_session
from models import State, City

from werkzeug.contrib.cache import MemcachedCache
#Should rename objects to something less generic.
import Objects

cache = MemcachedCache(servers=['127.0.0.1:11211'], default_timeout=0)

def stateCache():
    res = db_session.query(State.name, State.abbr, State.id).filter_by(active=1).all();
    myids = set()
    for i in res:
        cache.set('states:' + str(i[2]) + ':abbr', i[1], 0)
        cache.set('states:' + str(i[2]) + ':name', i[0], 0)
        cache.set('abbr:' + str(i[1]), str(i[2]), 0)
        myids.add(i[2])
    cache.set('states:ids', myids, 0)

    
    

def cityCache(stateId):
    res = db_session.query(City.name, City.id).filter_by(active=1, state_id=stateId).all();
    mycityIds = set()
    for i in res:
        cache.set('city:' + str(i[1]) + ':name', i[0], 0)
        mycityIds.add(i[1])
    cache.set('states:' + str(stateId) + ':cities', mycityIds, 0)
    
def allStatesIndex():
    #( id : (name : x, abbr : x, cities : (id : x, name : x) )
    allstates = dict()
    states = cache.get('states:ids')
    for id in states:
        statedetails = dict()
        statedetails['name'] = cache.get('states:' + str(id) + ':name')
        statedetails['abbr'] = cache.get('states:' + str(id) + ':abbr')
        statecities = cache.get('states:' + str(id) + ':cities')
        
        cities = dict()
        for cityid in statecities:
            cities[cityid] = cache.get('city:' + str(cityid) + ':name')
        statedetails['cities'] = cities
        allstates[id] = statedetails
    cache.set('allstates', allstates, )
    
def allStatesIndex2():
    allstates = dict()
    cachedstates = cache.get('states:ids')
    for id in cachedstates:
        statedetails = Objects.States()
        statedetails.name = cache.get('states:' + str(id) + ':name')
        statedetails.abbr = cache.get('states:' + str(id) + ':abbr')
        statedetails.cityids = cache.get('states:' + str(id) + ':cities')
        for cityid in statedetails.cityids:
            statedetails.cities[cityid] = cache.get('city:' + str(cityid) + ':name')
        allstates[id] = statedetails
    cache.set('allstates', allstates, 0)

def loadCache():
    #Warm up our cache.
    stateCache()
    mystateIds = cache.get('states:ids')
    for id in mystateIds:
        cityCache(id)
    allStatesIndex2()

loadCache()
cache.set('iswarm', 1, timeout=0)