from handler import Handler

class Login(Handler):
	def get(self):
		if self.user:
			self.redirect("/")
		else:
			self.render_base(temp="login.html",status="logout",history=False)
	def post(self):
		usern = self.request.get("username")
		passw = self.request.get("password")
		err= False
		if usern and passw:
			if self.login(usern,passw):
				self.redirect("/")
			else:
				err = True
		else:
			err= True
		if err:
			self.render_base(temp="login.html",status="logout",history=False,error="Invalid Login")
