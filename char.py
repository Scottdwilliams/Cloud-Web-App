import webapp2
from google.appengine.ext import ndb
import db_models
import json

class Char(webapp2.RequestHandler):
	def post(self):
		"""Creates a Character entity

		POST Body Variables:
		name - Required. Character name
		wowclass - Class
		spec - Class specialization
		"""
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supports application/json MIME type"
			return
		new_char = db_models.Char()
		name = self.request.get('name', default_value=None)
		wowclass = self.request.get('wowclass', default_value=None)
		spec = self.request.get('spec', default_value=None)
		if name:
			new_char.name = name
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request, Character name is required"
		if wowclass:
			new_char.wowclass = wowclass
		if spec:
			new_char.spec = spec
		key = new_char.put()
		out = new_char.to_dict()
		self.response.write(json.dumps(out))
		return

	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supports application/json MIME type"
			return
		if 'id' in kwargs:
			out = ndb.Key(db_models.Char, int(kwargs['id'])).get().to_dict()
			self.response.write(json.dumps(out))
		else:
			q = db_models.Char.query()
			keys = q.fetch(keys_only=True)
			results = { 'keys' : [x.id() for x in keys]}
			self.response.write(json.dumps(results))

class CharSearch(webapp2.RequestHandler):
	def post(self):
		'''
		Search for characters

		POST Body Variables:
		name - String. Character name
		wowclass - String. Name of character's class
		'''
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supporst application/json MIME type"
			return
		q = db_models.Char.query()
		if self.request.get('name',None):
			q = q.filter(db_models.Char.name == self.request.get('name'))
		if self.request.get('wowclass',None):
			q = q.filter(db_models.Char.wowclass == self.request.get('wowclass'))
		keys = q.fetch(keys_only=True)
		results = { 'keys' : [x.id() for x in keys]}
		self.response.write(json.dumps(results))

class CharDelete(webapp2.RequestHandler):
	def delete(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports JSON"
			return
		if 'id' in kwargs:
			char = ndb.Key(db_models.Char, int(kwargs['id'])).get()
			char.key.delete()
			out = self.response.status_mesage = "Character deleted"
			self.response.write(json.dumps(out))
		else:
			out=self.response.status_message = "No character given."
			self.response.write(json.dumps(out))
		return

