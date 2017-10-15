#!/usr/bin/env python

import webapp2
from google.appengine.api import oauth

app = webapp2.WSGIApplication([
	('/guild', 'guild.Guild'),
], debug=True)
app.router.add(webapp2.Route(r'/guild/<gid:[0-9]+><:/?>', 'guild.Guild'))
app.router.add(webapp2.Route(r'/guild/search', 'guild.GuildSearch'))
app.router.add(webapp2.Route(r'/guild/<gid:[0-9]+>/char/<cid:[0-9]+><:/?', 'guild.GuildOfficers'))
app.router.add(webapp2.Route(r'/char', 'char.Char'))
app.router.add(webapp2.Route(r'/char/<cid:[0-9]+><:/?>', 'char.Char'))
app.router.add(webapp2.Route(r'/char/search', 'char.CharSearch'))
app.router.add(webapp2.Route(r'/char/delete/<cid:[0-9]+><:/?>', 'char.CharDelete))