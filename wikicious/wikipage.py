from handler import Handler

from data import links,user

class WikiPage(Handler):
    def get(self,url):
      v = self.request.get("v")
      c = links.by_url(url)
      if self.user:
        if v:
          self.render_base(url=url,status="login",editlink="/_edit"+url+"?e="+str(c[int(v)].key().id()))
        else:
          self.render_base(url=url,status="login",editlink="/_edit"+url)
      else:
        self.render_base(url=url,status="logout")
      if c:
        if v:
          c=c[int(v)]
        else:
          c=c[0]
        u = user.by_id(int(c.userid))
        self.write(links.render_cont(c))
        self.write("<br><br>")
        self.write('<div style="color: #999">author: <b>%s</b></div>'%u.username)
      else:
        self.write('No content<br><a href="/_edit%s">Click here</a> to add content'%url)

    def post(self,url):
      u = self.request.get("u")
      self.redirect(u)