import misc

from handler import Handler
from data import user

from urllib import urlencode
from google.appengine.api import urlfetch

PRIVATE_KEY = "6LeyS-MSAAAAAAKtKgO-1ch13hZTmtVIACgwrpRK"
VERIFY_URL = "http://www.google.com/recaptcha/api/verify"

class Signup(Handler):
        def get(self):
		if self.user :
			self.redirect("/")
		else:
			self.render_base(temp="signup.html",status="logout",history=False)
	
        def post(self):
                usern = self.request.get("username")
                passw = self.request.get("password")
                verify = self.request.get("verify")
                email = self.request.get("email")
                challenge_field = self.request.get("recaptcha_challenge_field")
                response_field = self.request.get("recaptcha_response_field")
                ip = self.request.remote_addr
                error = False
                err1=err2=err3=err4=err5=""
                if misc.valid_user(usern) == None:
                    err1="Invalid username"
                    error =True
                if misc.valid_pass(passw) == None:
                    err2 = "Invalid password"
                    error = True
                if passw != verify:
                    err3 = "Password didn't match"
                    error = True
                if misc.valid_email(email) == None:
                        err4 = "Invalid email"
                        error = True            
                chh = user.by_name(usern)
                if chh:
                    err1 = "Username already exists"
                    error = True
                data={"privatekey": PRIVATE_KEY,
                    "remoteip": ip,
                    "challenge": challenge_field,
                    "response": response_field}
                respon = urlfetch.fetch(url=VERIFY_URL,payload=urlencode(data),method="POST")
                if respon.content.split("\n")[0] != "true":
                    error=True
                    err5="you are not human! Inavlid CAPTCHA"
                if error:
                    self.render_base(temp="signup.html",status="logout",history=False,
                        username=usern,email=email,err1=err1,err2=err2,err3=err3,err4=err4,err5=err5)
                else:
                        u = user.register(usern,passw,email)
                        cookie = misc.mak_cookie(u.key().id())
                        self.response.headers["Set-Cookie"] = "id=%s; Path=/"%cookie
                        self.redirect("/")
