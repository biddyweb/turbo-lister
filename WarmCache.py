from database import db_session
from models import State, City, Category

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
    allstates = list()
    cachedstates = cache.get('states:ids')
    for id in cachedstates:
        statedetails = Objects.State()
        statedetails.id = id
        statedetails.test = 'hello'
        statedetails.name = cache.get('states:' + str(id) + ':name')
        statedetails.abbr = cache.get('states:' + str(id) + ':abbr')
        statedetails.cityids = cache.get('states:' + str(id) + ':cities')
        statedetails.cities = dict()
        for cityid in statedetails.cityids:           
            statedetails.cities[cityid] = cache.get('city:' + str(cityid) + ':name')
            
            citydetails = Objects.City()
            citydetails.id = cityid
            citydetails.stateid = statedetails.id
            citydetails.name = statedetails.cities[cityid]
            cache.set('city:' + statedetails.abbr + ':' + statedetails.cities[cityid] + ':details', citydetails, )
        allstates.append(statedetails)
        cache.set('states:' + str(id) + ':details', statedetails, )
    cache.set('allstates', allstates, 0)
def allCategories():
    res = db_session.query(Category).all();
    allcats = list()
    for cat in res:
        mycat = Objects.Cat(cat.id, cat.name)
        allcats.append(mycat)
    cache.set('allcats', allcats, )
def loadCache():
    #Warm up our cache.
    stateCache()
    mystateIds = cache.get('states:ids')
    for id in mystateIds:
        cityCache(id)
    allStatesIndex()
    allCategories()

loadCache()
cache.set('iswarm', 1, timeout=0)