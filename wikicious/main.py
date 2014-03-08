import webapp2

import sys
sys.path.insert(0, 'libs')

from wikipage import WikiPage
from signup import Signup
from logout import Logout
from login import Login
from editpage import EditPage
from historypage import HistoryPage
from links import Links,TwitterCallback,LinksUpdate

from handler import Handler

class Draw(Handler):
      def get(self):
            self.render('draw.html')

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/signup/?', Signup),
                               ('/login/?', Login),
                               ('/draw/?',Draw),
                               ('/links/oauth_callback/?',TwitterCallback),
                               ('/links/update/?',LinksUpdate),
                               ('/links/?',Links),
                               ('/logout/?', Logout),
                               ('/_edit' + PAGE_RE, EditPage),
                               ('/_history'+PAGE_RE,HistoryPage),
                               (PAGE_RE, WikiPage)
                               ],
                              debug=True)