from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from database import db_session
from models import State, City

#Uncomment below for Memcached
#from werkzeug.contrib.cache import MemcachedCache
#cache = MemcachedCache(['127.0.0.1:11211'])




#Cache Functions

def stateCache():
    res = db_session.query(State.name, State.abbr, State.id).filter_by(active=1).all();
    mystates = dict()
    myabbrs = set()
    mystateIds = dict()
    for i in res:
        mystates[i[2]] = i[0]
        myabbrs.add(i[1])
        mystateIds[i[1]] = i[2]
    cache.set('states', mystates, timeout=5*60)
    cache.set('abbrs', myabbrs, timeout=6*60)
    cache.set('state-ids', mystateIds, 6*60)
    
    return (mystates, myabbrs, mystateIds)

def cityCache(abbr, stateId):
    res = db_session.query(City.name, City.id).filter_by(active=1, state_id=stateId).all();
    mycityIds = dict()
    for i in res:
        mycityIds[i[0]] = i[1]
    cache.set(abbr+'-cities', mycityIds, timeout=5 * 60)
    return mycityIds

def user(username):
    return "user view"

def createcity_cache():
    mypage = cache.get('city-page')
    if mypage is None:
            rv = cache.get('my-item')
            if rv is None:
                res = db_session.query(State).filter_by(active=1).all()
                states = [dict(name=row.name, id=row.id, active=row.active, cities=\
                   [dict(name=c.name, id=c.id) for c in db_session.query(City).filter_by(active=1).filter_by(state_id=row.id).all()])\
               for row in res]
                rv = states
                cache.set('my-item', rv, timeout=5 * 60)
            states = rv
            mypage = render_template('createcity.html', states=states)
            cache.set('city-page', mypage, timeout=5 * 60)
    return mypage

def createcity():
    return createcity_cache()

def index():
    mystates = cache.get('states')
    myabbrs = cache.get('abbrs')
    mystateIds = cache.get('state-ids')
    if mystates is None:
        mycached = stateCache()
        mystates = mycached[0]
        myabbrs = mycached[1]
        mystateIds = mycached[2]
    states = list() 
    for abbr in myabbrs:
        myid = mystateIds[abbr]
        myname = mystates[myid]
        mystate = dict()
        mystate['name'] = myname
        mystate['abbr'] = abbr
        mystate['id'] = myid
        mystate['cities'] = dict()
        mycities = cache.get(abbr+'-cities')
        if mycities is None:
            mycities = cityCache(abbr,myid)
        for k,v in mycities.iteritems():
            mystate['cities'][k] = v
        states.append(mystate)
    
    return render_template('index.html', states=states)

def newjob(abbr, city):
    #Check to see if user is logged in here
    if 1 == 1:
        loggedin = 1
    else:
        return render_template('login_redirect.html'), 404
    mystates = cache.get('states')
    myabbrs = cache.get('abbrs')
    mystateIds = cache.get('state-ids')
    if mystates is None:
        mycached = stateCache()
        mystates = mycached[0]
        myabbrs = mycached[1]
        mystateIds = mycached[2]
        
    #State checks out, lets see if city is valid
    if abbr in myabbrs:
        stateId = mystateIds[abbr]
        mycities = cache.get(abbr+'-cities')
        message = "huh"
        if mycities is None:
            mycities = cityCache(abbr,stateId)
            message = "not cached"
        if city in mycities:
            mycityID = mycities[city]
            message = "valid city"
        else: #Invalid city
            return render_template('404.html'), 404
    else: #Invalid state
        return render_template('404.html'), 404
    
    #Everything checks out, let's return the page
    return message
    #return 'new job page'
    
def jobsbystate(abbr):
    
    return 'hello'

def jobsbycity(abbr, city):
    
    return 'hello'

def alljobscitystate(abbr, city):
    
    return 'hello'

def jobscitystatecat(abbr, city, cat):
    
    return 'hello'

def joblisting(abbr, city, cat, jid):
    
    return 'hello'