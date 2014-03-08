import webapp2
import logging
import urlparse
import simplejson as json
import re

from handler import Handler
from data import user,temptoken,TweetLink

import oauth2 as oauth
import twitter

API_KEY = 'psuRHbdFTTUs5CXfCSziIw'
API_SECRET = 'FTCgGnwnsoVXzDhIzYoUv86nbSZkKoDPz8CjY80394'
ACCESS_KEY = '82673983-AumxTU4NkU0EdnQ0NEajwQafu0EnmXLk4DbN0mNlT'
ACCESS_SECRET = 'sDIddJ51x3xpPI1ozKUhPyAiRd6W2XbL90r3I5CGYO9WG'

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize?oauth_token='
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
CALLBACK_URL = 'https://localhost:8080/links/oauth_callback'
GET_SCREEN_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json?'

class Links(Handler):
	def get(self):
		if(self.user) : 
			if(not self.user.twitter_id):
				self.render_base(temp='links.html',status='login',addtwitter=True)
			else:
				links = TweetLink.by_uid(str(self.user.key()))
				self.render_base(temp='links.html',status='login',addtwitter=False, user = self.user.twitter_screen,links=links)
		else:
			self.redirect('/login')
	def post(self):
		if(self.user):
			consumer = oauth.Consumer(key=API_KEY,secret=API_SECRET)
			client = oauth.Client(consumer)
			resp,cont = client.request(REQUEST_TOKEN_URL,'POST')
			if (resp.status == 200):
				request_token = dict(urlparse.parse_qsl(cont))
				if(request_token['oauth_callback_confirmed']=='true'):
					temptoken.mak_token(key=request_token['oauth_token'],
						sec=request_token['oauth_token_secret'])
					#self.write(str(request_token))
					self.redirect(AUTHORIZE_URL + request_token['oauth_token'])


class TwitterCallback(Handler):
	def get(self):
		if(self.user):
			oauth_token = self.request.get('oauth_token')
			oauth_verifier = self.request.get('oauth_verifier')
			oauth_token_secret = temptoken.by_tokenkey(oauth_token).token_secret

			temptoken.del_token(oauth_token)
			consumer = oauth.Consumer(key=API_KEY,secret=API_SECRET)
			tokens = oauth.Token(oauth_token,oauth_token_secret)
			tokens.set_verifier(oauth_verifier)
			client = oauth.Client(consumer,tokens)

			resp,cont = client.request(ACCESS_TOKEN_URL,"POST")
			access_token = dict(urlparse.parse_qsl(cont))
			#self.write(str(access_token))
			self.user.twitter_id = access_token['user_id']
			self.user.twitter_screen = access_token['screen_name']
			self.user.twitter_token_key = access_token['oauth_token']
			self.user.twitter_token_secret = access_token['oauth_token_secret']
			self.user.put()
			self.redirect('/links')
		else:
			self.redirect('/login')

class LinksUpdate(Handler):
	def post(self):
		if(self.user):
			consumer = oauth.Consumer(key=API_KEY,secret=API_SECRET)
			tokens = oauth.Token(self.user.twitter_token_key,self.user.twitter_token_secret)
			client = oauth.Client(consumer,tokens)
			since = ""
			if(self.user.twitter_since):
				since= "&since_id="+self.user.twitter_since
			resp,cont = client.request(GET_SCREEN_URL + "screen_name=%s&trim_user=1%s"%(self.user.twitter_screen,since),"GET")
			statuses = json.loads(cont)#add if not error
			if(('error' not in statuses )):
				if(statuses):
					#self.write(json.dumps(statuses))
					self.user.twitter_since = str(statuses[0]['id'])
					self.user.put()
					regexp = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
					for i in range(0,len(statuses)):
						l = re.findall(regexp,statuses[i]['text'])
						if(l):
							for j in range(0,len(l)):
								t = TweetLink.add_tweet(uid=str(self.user.key()),
									tid=str(statuses[i]['id']),
									tlink = l[j])
								t.put()
					self.redirect('/links')
				else:
					self.write("No more links added")
			else:
				self.write("ERROR")
		else:
			self.redirect('/login')