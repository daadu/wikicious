import misc
import time

from google.appengine.ext import db

class user(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty(required = True)
    twitter_id = db.StringProperty()
    twitter_screen = db.StringProperty()
    twitter_token_key = db.StringProperty()
    twitter_token_secret = db.StringProperty()
    twitter_since = db.StringProperty()

    @classmethod
    def by_id(cls,uid):
    	return cls.get_by_id(uid)
    @classmethod
    def by_twitter_id(cls,tid):
        return cls.all().filter("twitter_id =",twitter_id).get()
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
class TweetLink(db.Model):
    userid = db.StringProperty(required=True)
    tweetlink = db.LinkProperty(required=True)
    tweetid = db.StringProperty(required=True)

    @classmethod
    def by_id(cls,tid):
        return cls.get_by_id(tid)
    @classmethod
    def by_uid(cls,uid):
        return list(cls.all().filter("userid =",uid))
    @classmethod
    def add_tweet(cls,uid,tid,tlink):
        n = cls(userid=uid,tweetid = tid, tweetlink=tlink)
        n.put()
        time.sleep(.3)
        return n;

class temptoken(db.Model):
    token_key = db.StringProperty(required=True)
    token_secret = db.StringProperty(required=True)

    @classmethod
    def by_tokenkey(cls,key):
        return cls.all().filter("token_key =",key).get()
    @classmethod
    def mak_token(cls,key,sec):
        x = cls(token_key=key,token_secret=sec)
        x.put()
        time.sleep(0.3)
        return x
    @classmethod
    def del_token(cls,key):
        cls.all().filter("token_key =",key).get().delete()
        pass

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