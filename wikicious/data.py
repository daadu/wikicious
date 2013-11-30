import misc
import time

from google.appengine.ext import db

class user(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty(required = True)

    @classmethod
    def by_id(cls,uid):
    	return cls.get_by_id(uid)

    @classmethod
    def by_name(cls,uname):
    	u = cls.all().filter("username =",uname).get()
    	return u

    @classmethod
    def register(cls,name, passw, email):
    	hpass = misc.mak_pass(name,passw)
    	u = cls(username= name,password = hpass,email = email)
        u.put()
        return u
    @classmethod
    def get_user(cls,name,passw):
    	u = cls.by_name(name)
    	if u and misc.ver_pass(name,passw,u.password):
    	    return u

class links(db.Model):
    url = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    userid = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    @classmethod
    def by_id(cls,lid):
        return cls.get_by_id(lid)

    @classmethod
    def by_url(cls,u):
        ob = cls.all().filter("url =",u).order("-last_modified")
        if ob:
            ob = list(ob)
            return ob

    @classmethod
    def mak_link(cls,url,cont,uid):
        ob = cls(url=url,content=cont,userid=uid)
        ob.put()
        time.sleep(.3)
        return ob

    @classmethod
    def get_url(cls,url):
        c = cls.by_url(url)
        return c

    @classmethod
    def render_cont(cls,c):
        return c.content.replace("\n","<br>")