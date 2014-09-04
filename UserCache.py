from werkzeug.contrib.cache import MemcachedCache

# http://stackoverflow.com/questions/10016499/nginx-with-flask-and-memcached-returns-some-garbled-characters
# here we can point the applicaiton to a separate cache for user data only.
# This is intended to prevent our application from evicting application objects from cache.
cache = MemcachedCache(['127.0.0.1:11211'], default_timeout=0)

class UserObject():
    id = None
    
    def __init__(self, userid):
        self.id = userid
        
    def put(self,obtype, obid, obdata):
        
        cache.set(self.id + ':' + obtype + ':' + obid, obdata)
        
    def get(self,obtype, obid):
        
        return cache.get(self.id + ':' + obtype + ':' + obid )