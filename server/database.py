import pymongo
from pymongo.server_api import ServerApi
import os
import codecs
from dotenv import load_dotenv
from datetime import date, timedelta

def lenCheck(value):
	try:
		return int(value)
	except ValueError:
		raise Exception('License length\'s value (%s) is not a number' % value)

class MongoDB:

	def __init__(self):
		load_dotenv()
		try:
			self.uri = os.getenv('MONGODB_URI', 'mongodb://database:27017/')
			self.dbName = os.getenv('SERVER_ENV', 'production')
			self.licenseLength = int(os.getenv('LICENSE_LEN', 32))
			self.adminPWD = os.environ['ADMIN_PWD']
			self.managerPWD = os.environ['MANAGER_PWD']
			self.clientPWD = os.environ['CLIENT_PWD']
			self.required_create = [word.strip() for word in filter(None, os.environ['REQUIRED_CREATE'].split(','))]
			self.unique = [word.strip() for word in filter(None, os.environ['UNIQUE_VALIDATE'].split(','))]
		except KeyError as e:
			raise Exception('Cannot find %s in .env file' % e)
		except ValueError as e:
			raise Exception('LICENSE_LEN is not entered as an integer\n%s' % e)
		if self.uri[-1] != '/':
			raise Exception('Improper MONGODB_URI - Should end with "/" and not include anything after')
		if not (self.uri[:10] == 'mongodb://' or self.uri[:14] == 'mongodb+srv://'):
			raise Exception('Improper MONGODB_URI - Should start with "mongodb+srv://" for cloud and "mongodb://" for local')
		if not (set(self.unique) <= set(self.required_create)):
			raise Exception('"UNIQUE_VALIDATE" is not a subset of "REQUIRED_CREATE" environment variable')
		
	def connect(self):
		myclient = pymongo.MongoClient(self.uri, server_api=ServerApi('1'))
		myDB = myclient[self.dbName]
		self.myCollection = myDB["licenses"]

	def create(self, requestDict: dict):
		if all(name in requestDict for name in self.required_create + ['length']):
			strippedDict = {key: requestDict[key] for key in self.required_create}
			today = date.today()
			future = today + timedelta(lenCheck(requestDict['length']))
			strippedDict['_id'] = codecs.encode(os.urandom(int(self.licenseLength/2)), 'hex').decode()
			strippedDict['created'] = date.isoformat(today)
			strippedDict['expiry'] = date.isoformat(future)
			strippedDict['renew_count'] = 0
			add_item = False
			if self.unique:
				findDict = {'$or': [{key: strippedDict[key]} for key in self.unique]}
				duplicates = list(self.myCollection.find(findDict))
				if not duplicates:
					add_item = True 
				else:
					raise Exception('One of the "UNIQUE_VALIDATE" keys are matching with an already registered license -> %s' % str(duplicates))
			else:
				add_item = True
			if add_item:
				x = self.myCollection.insert_one(strippedDict)
				return x.inserted_id
		else:
			raise Exception('Missing %s key(s) in the json request' % ', '.join(set(self.required_create + ['length']).difference(list(requestDict.keys()))))
		
	def fetch(self, requestDict: dict):
		required_validate = ['_id']
		if all(name in requestDict for name in required_validate):
			strippedDict = {key: requestDict[key] for key in required_validate}
			check = list(self.myCollection.find(strippedDict))
			if len(check) > 1:
				raise Exception('Multiple licenses present with the same id')
			elif len(check) == 1:
				return check[0]
			else:
				raise Exception('Unable to find a license with _id %s' % requestDict['_id'])
		else:
			raise Exception('Missing "_id" parameter in the query')
		
	def renew(self, requestDict: dict):
		required_validate = ['_id', 'length']
		if all(name in requestDict for name in required_validate):
			today = date.today()
			future = today + timedelta(lenCheck(requestDict['length']))
			x = self.myCollection.update_one({'_id': requestDict['_id']}, { '$set': {'expiry': date.isoformat(future)}, '$inc': {'renew_count': 1}})
			if x.acknowledged and x.matched_count == 1 and x.modified_count == 1:
				return True
			elif x.acknowledged and x.matched_count == 1 and x.modified_count == 0:
				raise Exception('Expiry date for the license is already set to %d days from now' % int(requestDict['length']))
			elif x.acknowledged and x.matched_count == 0 and x.modified_count == 0:
				raise Exception('Unable to find a license with _id %s' % requestDict['_id'])
			else:
				raise Exception('Unable to reach the MongoDB server')
		else:
			raise Exception('Missing %s key(s) in the json request' % ', '.join(set(required_validate).difference(list(requestDict.keys()))))

	def update(self, requestDict: dict):
		required_update = ['_id']
		if all(name in requestDict for name in required_update):
			if list(requestDict.keys()) != ['_id']:
				if all(name in self.required_create + required_update for name in requestDict):
					x = self.myCollection.update_one({'_id': requestDict['_id']}, { '$set': {k:v for k,v in requestDict.items() if k not in required_update}})
					if x.acknowledged and x.matched_count == 1 and x.modified_count == 1:
						return True
					elif x.acknowledged and x.matched_count == 1 and x.modified_count == 0:
						raise Exception('The provided details already match the existing data, and no changes were made')
					elif x.acknowledged and x.matched_count == 0 and x.modified_count == 0:
						raise Exception('Unable to find a license with _id %s' % requestDict['_id'])
					else:
						raise Exception('Unable to reach the MongoDB server')
				else:
					raise Exception('The payload contains unknown keys. Please refer to the /create-fields response to identify the allowed keys for this operation.')
			else:
				raise Exception('Missing key(s) to be updated in the json request')
		else:
			raise Exception('Missing "_id" key in the json request')
			
	def delete(self, requestDict: dict):
		required_delete = ['_id']
		if all(name in requestDict for name in required_delete):
			x = self.myCollection.delete_one({'_id': requestDict['_id']})
			if x.acknowledged and x.deleted_count == 1:
				return True
			elif x.acknowledged and x.deleted_count == 0:
				raise Exception('Unable to find a license with _id %s' % requestDict['_id'])
		else:
			raise Exception('Missing "_id" parameter in the query')
		
	def getAll(self):
		allLicenses = list(self.myCollection.find())
		return allLicenses
	