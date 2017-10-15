import webapp2
from google.appengine.ext import ndb
import db_models
import json

class Guild(webapp2.RequestHandler):
	def post(self):
		"""Creates a Guild entity

		POST Body Variables:
		name - Required. Guild name
		officers[] - Array of Char ids
		members[] - Array of Char ids
		"""
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supports application/json MIME type"
			return
		new_guild = db_models.Guild()
		name = self.request.get('name', default_value=None)
		officers = self.request.get_all('officers[]', default_value=None)
		members = self.request.get_all('members[]', default_value=None)
		if name:
			new_guild.name = name
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request, guild name is required"
		if officers:
			for officer in officers:
				new_guild.officers.append(ndb.Key(db_models.Char, int(officer)))
		if members:
			for member in members:
				new_guild.members.append(ndb.Key(db_models.Char, int(member)))
		key = new_guild.put()
		out = new_guild.to_dict()
		self.response.write(json.dumps(out))
		return

	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supports application/json MIME type"
			return
		if 'gid' in kwargs:
			out = ndb.Key(db_models.Guild, int(kwargs['gid'])).get().to_dict()
			self.response.write(json.dumps(out))
		else:
			q = db_models.Guild.query()
			keys = q.fetch(keys_only=True)
			results = { 'keys' : [x.id() for x in keys]}
			self.response.write(json.dumps(results))

class GuildOfficers(webapp2.RequestHandler):
	def put(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supports application/json MIME type"
		if 'gid' in kwargs:
			guild = ndb.Key(db_models.Guild, int(kwargs['gid'])).get()
			if not guild:
				self.response.status = 404
				self.response.status_message = "Guild not found"
				return
		if 'cid' in kwargs:
			officer = ndb.Key(db_models.Char, int(kwargs['cid']))
			if not officer:
				self.response.status = 404
				self.response.status_message = "Character not found"
				return
		if officer not in guild.officers:
			guild.officers.append(officer)
			guild.put()
		self.response.write(json.dumps(guild.to_dict()))
		return

class GuildSearch(webapp2.RequestHandler):
	def post(self):
		'''
		Search for guilds

		POST Body Variables:
		name - String. Character name
		'''
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not acceptable, API only supporst application/json MIME type"
			return
		q = db_models.Guild.query()
		if self.request.get('name',None):
			q = q.filter(db_models.Guild.name == self.request.get('name'))
		keys = q.fetch(keys_only=True)
		results = { 'keys' : [x.id() for x in keys]}
		self.response.write(json.dumps(results))