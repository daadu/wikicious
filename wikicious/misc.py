import hashlib
import hmac
import random
import re
from string import letters

SECRET = "!-!ILoveMyDaddy!-!"


def mak_cookie(uid):
	uid = str(uid)
	h = hmac.new(SECRET,uid).hexdigest()
	return "%s|%s"%(uid,h)

def ver_cookie(s):
	if s:
		uid = s.split("|")[0]
		if s == mak_cookie(uid):
			return int(uid)

def mak_salt():
	s=""
	for i in range(5):
		s += random.choice(letters)
	return s

def mak_pass(user,passw):
	s = mak_salt()
	h = hashlib.sha256(user + passw + s).hexdigest()
	return "%s,%s"%(h,s)

def ver_pass(user,passw,hpass):
	s = hpass.split(",")
	h = hashlib.sha256(user + passw + s[1]).hexdigest()
	if h == s[0]:
		return True
	return False

def valid_user(user):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(user)
def valid_pass(passw):
        PASS_RE = re.compile(r"^.{3,20}$")
        return PASS_RE.match(passw)
def valid_email(email):
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        return EMAIL_RE.match(email)