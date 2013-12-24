from sqlalchemy import Column, Integer, String, ForeignKey, Text
from database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    fname = Column(String(50), unique=False)
    lname = Column(String(50), unique=False)
    email = Column(String(120), unique=True)
    phone = Column(String(20), unique=False, nullable=True)
    
    def __init__(self, fname=None, lname=None, email=None, phone=None):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone = phone

    def __repr__(self):
        return '<User %r>' % (self.email)
    
class State(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    
    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<User %r>' % (self.name)
    
class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    state_id = Column(Integer, ForeignKey('state.id'))
    name = Column(String(50), unique=True)
    
    def __init__(self, state_id=None, name=None):
        self.name = name
        self.state_id = state_id

    def __repr__(self):
        return '<User %r>' % (self.name)
    
    
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    
    def __init__(self, state_id=None, name=None):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % (self.name)
    
class JobList(Base):
    __tablename__ = 'joblist'
    id = Column(Integer, primary_key=True)
    poster_id = Column(Integer, ForeignKey('user.id'))
    state_id = Column(Integer, ForeignKey('state.id'))
    city_id = Column(Integer, ForeignKey('city.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    title = Column(Text)
    
    def __init__(self, poster_id=None, state_id=None, city_id=None, category_id=None, title=None):
        self.poster_id = poster_id
        self.state_id = state_id
        self.city_id = city_id
        self.category_id = category_id
        self.title = title

    def __repr__(self):
        return '<Post Title %r>' % (self.title)

class JobDetails(Base):
    __tablename__ = 'jobdetails'
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('joblist.id'))
    body = Column(Text)

    def __init__(self, job_id=None, body=None):
        self.job_id = job_id
        self.body = body

    def __repr__(self):
        return '<User %r>' % (self.name)