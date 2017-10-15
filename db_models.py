from google.appengine.ext import ndb

class Model(ndb.Model):
	def to_dict(self):
		d = super(Model, self).to_dict()
		d['key'] = self.key.id()
		return d

class Update(Model):
	date_time = ndb.DateTimeProperty(required=True)
	user_count = ndb.IntegerProperty(required=True)
	message_count = ndb.IntegerProperty(required=True)

class Message(Model):
	character = ndb.StringProperty(required=True)
	date_time = ndb.DateTimeProperty(required=True)
	count = ndb.IntegerProperty(required=True)

class Char(Model):
	name = ndb.StringProperty(required=True)
	wowclass = ndb.StringProperty()
	spec = ndb.StringProperty()

class Guild(Model):
	name = ndb.StringProperty(required=True)
	officers = ndb.KeyProperty(repeated=True)
	members = ndb.KeyProperty(repeated=True)

	def to_dict(self):
		d = super(Guild,self).to_dict()
		d['officers'] = [o.id() for o in d['officers']]
		return d
