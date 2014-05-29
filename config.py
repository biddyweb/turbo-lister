from datetime import date

# configuration
class Config(object):
    DBTYPE = 'mysql'
    DBSERVER = 'localhost'
    DATABASE = 'turbo_list'
    DBUSER = 'root2'
    DBPASS = 'password'
    PER_PAGE = 30
    SECRET_KEY = 'development key'
