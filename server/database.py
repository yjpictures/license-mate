import pymongo
from pymongo.server_api import ServerApi
import os
import codecs
from dotenv import load_dotenv
import yaml
from datetime import date, timedelta

class MongoDB:

	def __init__(self):
		# environment file
		load_dotenv()
		self.uri = str(os.getenv('MONGODB_URI'))
		self.dbName = str(os.getenv('FLASK_ENV'))
		self.licenseLength = int(os.getenv('LICENSE_LEN')) # type: ignore
		self.adminPWD = str(os.getenv('ADMIN_PWD'))
		self.managerPWD = str(os.getenv('MANAGER_PWD'))
		self.clientPWD = str(os.getenv('CLIENT_PWD'))
		# TODO: error handling if these passwords not present
		if not (self.uri  and self.dbName and self.licenseLength):
			raise Exception('Cannot find "MONGODB_URI" AND/OR "FLASK_ENV" AND/OR "LICENSE_LEN" in .env file')
		# config file
		configFileName = 'config.yml'
		if not os.path.exists(configFileName):
			raise Exception('Cannot find the %s file in %s' % (configFileName, os.getcwd()))
		with open(configFileName, 'r') as file:
			config = yaml.safe_load(file)
		if not all(name in config for name in ['required-create', 'unique']):
			raise Exception('Cannot find "required-create" AND/OR "unique" in config.yml file. If you do not need any unique comparison then leave it as an empty list "[]".')
		self.required_create = config['required-create']
		self.unique = config['unique']
		if type(self.required_create) != list or type(self.unique) != list:
			raise Exception('Value of "required-create" AND/OR "unique" in config.yml file is incorrect')
		
	def connect(self):
		myclient = pymongo.MongoClient(self.uri, server_api=ServerApi('1'))
		myDB = myclient[self.dbName]
		self.myCollection = myDB["licenses"]

	def create(self, requestDict: dict):
		if all(name in requestDict for name in self.required_create + ['length']):
			strippedDict = {key: requestDict[key] for key in self.required_create}
			today = date.today()
			future = today + timedelta(int(requestDict['length']))
			strippedDict['_id'] = codecs.encode(os.urandom(self.licenseLength), 'hex').decode()
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
					raise Exception('One of the "unique" keys are matching with an already registered license -> %s' % str(duplicates))
			else:
				add_item = True
			if add_item:
				x = self.myCollection.insert_one(strippedDict)
				return x.inserted_id
		else:
			raise Exception('Missing the "required-create" keys AND/OR "length" key in the json request')
		
	def validate(self, requestDict: dict):
		required_validate = ['_id']
		if all(name in requestDict for name in required_validate):
			strippedDict = {key: requestDict[key] for key in required_validate}
			check = list(self.myCollection.find(strippedDict))
			if len(check) > 1:
				raise Exception('Multiple licenses present with the same id')
			elif len(check) == 1:
				return check[0]
			else:
				raise Exception('The license (%s) is not present in the database' % requestDict['_id'])
		else:
			raise Exception('Missing "_id" key in the json request')
		
	def renew(self, requestDict: dict):
		required_validate = ['_id', 'length']
		if all(name in requestDict for name in required_validate):
			today = date.today()
			future = today + timedelta(int(requestDict['length']))
			x = self.myCollection.update_one({'_id': requestDict['_id']}, { '$set': {'expiry': date.isoformat(future)}, '$inc': {'renew_count': 1}})
			if x.acknowledged and x.matched_count == 1 and x.modified_count == 1:
				return True
			elif x.acknowledged and x.matched_count == 1 and x.modified_count == 0:
				raise Exception('Expiry date for the license is already set to %d days from now' % int(requestDict['length']))
			elif x.acknowledged and x.matched_count == 0 and x.modified_count == 0:
				raise Exception('Unable to find a license with _id %s' % requestDict['_id'])
		else:
			raise Exception('Missing "_id" AND/OR "length" key in the json request')
			
	def delete(self, requestDict: dict):
		required_delete = ['_id']
		if all(name in requestDict for name in required_delete):
			x = self.myCollection.delete_one({'_id': requestDict['_id']})
			if x.acknowledged and x.deleted_count == 1:
				return True
			elif x.acknowledged and x.deleted_count == 0:
				raise Exception('Unable to find a license with _id %s' % requestDict['_id'])
		else:
			raise Exception('Missing "_id" key in the json request')
		
	def getAll(self):
		allLicenses = list(self.myCollection.find())
		return allLicenses
	