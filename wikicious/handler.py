import webapp2
import jinja2
import os
import misc


from data import user,links

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
    def render_str(self,template,**params):
        t=jinja_env.get_template(template)
        return t.render(params)
    def render(self, template,**kw):
        self.write(self.render_str(template,**kw))
    def readcookie(self):
      cookie = self.request.cookies.get("id")
      uid = misc.ver_cookie(cookie)
      return uid
    def initialize(self, *a, **kw):
      webapp2.RequestHandler.initialize(self,*a,**kw)
      uid = self.readcookie()
      if uid:
        uid = user.by_id(uid)
      self.user = uid
    def login(self,usern,passw):
      u = user.get_user(usern,passw)
      if u:
        uid = u.key().id()
        huid = misc.mak_cookie(uid)
        self.response.headers.add_header("Set-Cookie","id=%s; Path=/"%huid)
        return True
      return False
    def logout(self):
      self.response.headers["Set-Cookie"] = "id=; Path=/"

    def render_base(self,url="",temp="base.html",status="logout",history=True,**kw):
      if status == "logout":
        if history:
          self.render(temp,firstlink="/login",first="login",secondlink="/signup",second="signup",
            hislink="/_history"+url,history="history",url=url,**kw)
        else:
          self.render(temp,firstlink="/login",first="login",secondlink="/signup",second="signup",**kw)
      else:
        if history:
          self.render(temp,edit="edit",first=self.user.username,
            secondlink="/logout",second = "logout",
            hislink="_history"+url,history="history",url=url,**kw)
        else: 
          self.render(temp,edit="edit",first=self.user.username,
            secondlink="/logout",second = "logout",**kw)