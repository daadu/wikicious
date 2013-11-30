from handler import Handler
from data import links

class HistoryPage(Handler):
	def get(self,url):
		li = links.by_url(url)
		if self.user:	
			self.render_base(url,temp="history.html",status="login",history=False,li = li)
		else:
			self.render_base(url,temp="history.html",status="logout",history=False,li=li)