import webapp2

from wikipage import WikiPage
from signup import Signup
from logout import Logout
from login import Login
from editpage import EditPage
from historypage import HistoryPage


PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/signup/?', Signup),
                               ('/login/?', Login),
                               ('/logout/?', Logout),
                               ('/_edit' + PAGE_RE, EditPage),
                               ('/_history'+PAGE_RE,HistoryPage),
                               (PAGE_RE, WikiPage)
                               ],
                              debug=True)
