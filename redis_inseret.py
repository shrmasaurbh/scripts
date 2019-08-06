from redis import *
from pymongo import MongoClient
from datetime import datetime,timedelta
from bson.objectid import ObjectId
import redis



# Redis #
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = ""
CACHE_DB = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

# DB_NAMES={
# 		"cc_area" : "CcArea",
# 		"cc_city" : "CcCity",
# 		"cc_country" : "CcCountry",
# 		"cc_organization_type" : "CcOrganizationType",
# 		"cc_project" : "CcProject",
# 		"cc_state" : "CcState",
# 		"cc_user_type" : "CcUserType",
# 		"cc_communications" : "CcCommunications",
# 		"cc_source_type_listing" : "CcSourceTypeListing",
# 		"cc_project_status_lc" : "CcProjectStatusLc",
# 		"cc_documents_section" : "CcDocumentsSection",
# 		"cc_part_types" : "CcPartTypes",
# }
DB_NAMES={
	"cc_user_account" : "CcUserAccount",
	"cc_user_profile" : "CcUserProfile",
}

class CreateUserTables:
	def __init__(self, env):
		try:
			if env:
				pass
				#for live enviroment
				#self.client         = MongoClient("localhost", 27017)
				#self.db            = client.test_clickg
				#self.cgusernew     = db.activity_cgusernew
			else:
				self.client = MongoClient("localhost", 27017)
				self.db = self.client.customer
				# self.db = self.client.cc_miscellaneous

				# self.names = [self.db.cc_area,self.db.cc_city,self.db.cc_country,self.db.cc_organization_type,self.db.cc_project,self.db.cc_state,self.db.cc_user_type,self.db.cc_communications,self.db.cc_source_type_listing,self.db.cc_project_status_lc,self.db.cc_documents_section,self.db.cc_part_types]
				self.names = [self.db.cc_user_account,self.db.cc_user_profile]

				
		except:
			print("could not connect with the db please check")
		else:
			print('connection established')
	
	def parse_mongodata(self,mongodata):
		# mongodata = mongodata.to_dict()
		mongodata["id"]= mongodata.pop("_id")

		for k,v in mongodata.items():
			if isinstance(v, ObjectId):
				mongodata[k]= str(v)
		return mongodata


	def CreateCache(self, user=None):

		for db_name in self.names:
			# eval(db_/name)
			coll_name = db_name._Collection__name
			db_data_count = db_name.find().count()
			print("----------------")
			print("----------------")
			print(db_data_count)
			print(coll_name)
			print("----------------")
			print("----------------")
			if db_data_count:
				db_data = db_name.find()
				score =1
				for data in db_data:
					data = self.parse_mongodata(data)
					data['created_at'] = datetime.strftime(data['created_at'],"%a, %d %b %Y %H:%M:%S GMT")
					data['updated_at'] = datetime.strftime(data['updated_at'],"%a, %d %b %Y %H:%M:%S GMT")
					data = str(data)
					print(data)
					CACHE_DB.zadd(DB_NAMES[coll_name], {data: score})
					score = score+1

mesc_user = CreateUserTables(0)
create_cache = mesc_user.CreateCache()
