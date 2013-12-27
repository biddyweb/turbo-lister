from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from database import db_session
from models import State, City

#Uncomment below for Memcached
#from werkzeug.contrib.cache import MemcachedCache
#cache = MemcachedCache(['127.0.0.1:11211'])
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

def user(username):
    return "user view"

def createcity():
    res = db_session.query(State).filter_by(active=1).all()
    states = [dict(name=row.name, id=row.id, active=row.active, cities=\
                   [dict(name=c.name, id=c.id) for c in db_session.query(City).filter_by(active=1).filter_by(state_id=row.id).all()])\
               for row in res]
    return render_template('createcity.html', states=states)

def index():
    return render_template('index.html')