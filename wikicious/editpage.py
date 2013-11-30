from handler import Handler
from data import links

class EditPage(Handler):
	def get(self,url):
		e = self.request.get("e")
		cont=""
		if e:
			ur = links.by_id(int(e))
			cont  = ur.content
		else:
			ob= links.by_url(url)
			if ob:
				c = ob[0]
				cont = c.content
		if self.user:
			self.render_base(url=url,status="login",temp="edit.html",history=False,cont=cont)
		else:
			self.redirect("/")
	def post(self,url):
		cont = self.request.get("content")
		if cont:
			l = links.mak_link(url,cont,str(self.user.key().id()))
			self.redirect("%s"%url)
		else :
			self.render_base(url=url,temp="edit.html",status="login",error="Enter some content")
