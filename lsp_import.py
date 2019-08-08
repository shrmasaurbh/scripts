import csv

import requests
import math
import os
import re
import random
from pymongo import MongoClient
# import MySQLdb
from datetime import datetime,timedelta
from bson.objectid import ObjectId
# from constants import *
import logging 
  
#Create and configure logger 
logging.basicConfig(filename="newfile.log", 
					format='%(asctime)s %(message)s', 
					filemode='w') 
#Creating an object 
logger=logging.getLogger() 
#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG)

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
				self.db_cust = self.client.customer
				self.db_misc = self.client.cc_miscellaneous
				self.user_profile = self.db_cust.cc_user_profile
				self.user_account = self.db_cust.cc_user_account
				self.area_collection = self.db_misc.cc_area
				#connect to mysql
				# self.mysql_db = MySQLdb.connect("localhost", "lsp", "root", "root")
				# self.mysql_cursor = self.mysql_db.cursor()
		except:
			print("could not connect with the db please check")
		else:
			print('connection established')

	def get_aplha_username(self,val):
		garbage_char = "?.!/;:@$0123456789_()[]"
		if not val.isalpha():
			for char in garbage_char:
				val = val.replace(char,"")
		return val

	def c_user_profile(self, user=None):
		with open('/home/gautam/Downloads/lsp_deatils.csv', newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:				
				# if not row['GSTIN']:
				# 	row['GSTIN'] = None
				# if not row['PAN']:
				# 	row['PAN'] = None
				active_status = True
				sp_business_name = row['sp_business_name'].lower()
				if row['Address']:
					address = row['Address'].lower()
				else:
					#active_status = False
					address = None
				# carcrewpoc = row['CarcrewPOC'].lower()
				sp_poc_name = row['sp_poc_name'].lower()
				if row['Source']:
					email = row['Source'].lower().strip(' ')
					email = None

				area_id = None
				if row['cc_area_name']:
					if row['PinCode']:
						print("pincode")
						area_details = self.area_collection.find({
							"cc_area_name":row['cc_area_name'],
							"cc_area_pin_code": row['PinCode'] 
						})
					else:
						print("missing pincode")
						area_details = self.area_collection.find({
							"cc_area_name":row['cc_area_name']
						})

					for a in area_details:
						area_id = str(a['_id'])
				insert_lsp_data = {}
				insert_lsp_data.update({
					'sp_cc_code' : None,
					'sp_business_name' : sp_business_name,
					'sp_business_pretty_name' : sp_business_name,
					'sp_business_addresses' : address,
					'sp_country_id' : '5c740b24e45cf77ac147a98a',
					'sp_state_id' : row['State'],
					'sp_city_id' : row['City'],
					'sp_area_id' : area_id,
					'sp_lat_code' : None,
					'sp_long_code' : None,
					'sp_registered_entity_name' : row['RegisteredEntityName'],
					'sp_registered_addresses' : None,
					'sp_is_rb_address_same' : False,
					'sp_gstin_number' : row['GSTIN'],
					'sp_pan_number' : row['PAN'],
					'sp_service_time_schedule' : None,
					'sp_service_off_day' : None,
					'sp_website_address' : None,
					'sp_poc_name' : sp_poc_name,
					'sp_poc' : row['sp_poc'],
					'sp_business_email' : row['Source'].lower(),
					'sp_service_up' : False,
					'sp_cc_category_type' : None,
					'sp_verfied_status' : None,
					'sp_is_verified' : False,
					'cc_project_id' : '5c740be7e45cf77ac07c27de',
					'cc_user_type_id' : row['Type'],
					'is_sp_published' : False,
					'is_active' : active_status,
					'cc_org_type_id' : None,
					'created_by' : row['created_by'],				
					'updated_by' : row['updated_by']
				})

				lsp_resp = requests.post("http://127.0.0.1:8000/lsp-api/lsp-single", 
					json=insert_lsp_data, headers={'content-type': 'application/json'})


				if lsp_resp.status_code == 201:
					sp_id = lsp_resp.json()['id']

					#enter data in user auth table for that lsp
					value = "!d@$sfsdfsdf"
					name_list = sp_business_name.split(" ")
					rand_no = random.randint(0, 9999)
					name_len = len(name_list)
					if name_len > 1:
					   item = name_list[0]
					   val = self.get_aplha_username(item)
					   if not val:
						   #item = name_list[1]
						   val = self.get_aplha_username(name_list[1])
					   if len(val) > 3:
						   username = val[0:3]+'r'
					   else:
						   username = val+'v'
					elif name_len == 1:
						   username = val[0:3]+'u'
						   username = val+'c'
					random_str = ['yy', 'uu', 'jj', 'hh', 'kk','we','qq', 'w', 'e', 'm', 'b', 's','a', 'd', 'g', 'ds', 't', 'y', 'h', 'u', 'j', 'i', 'k', 'z', 'x', 'v', 'o', 'p']
					username = username+random.choice(random_str)
					username = username+'cclsp'+str(rand_no)
					user_auth_data = {}
					user_auth_data.update({
						'username' : username,
						'password' : username+'123',
						'email' : row['Source'],
						'cc_login_type' : 2,
						'cc_project_id' : '5c740be7e45cf77ac07c27de',
						'cc_user_type_id' : row['Type'], 
						'cc_user_role' : "lsp",
						'object_id' : sp_id,
						'is_active' : active_status,
						'created_by' : row['created_by'],				
						'updated_by' : row['updated_by']
					})
					
					auth_resp = requests.post("http://127.0.0.1:8000/login-api/user/", 
						json=user_auth_data, headers={'content-type': 'application/json'})

					if auth_resp.status_code == 201:
						auth_id = auth_resp.json()['value']
					#user profile data insereted
						if name_len > 1:
							item = name_list[0]
							val = self.get_aplha_username(item)
							if not val:
								val = self.get_aplha_username(name_list[1])
								if not val:
									val = self.get_aplha_username(name_list[2])
							if len(val) > 10:
							   first_name = val[0:10]
							else:
							   first_name = val
							other_item = name_list[-1]
							other_val = self.get_aplha_username(other_item)
							if not other_val:
								other_val = self.get_aplha_username(name_list[-2])
								if not other_val:
									other_val = self.get_aplha_username(name_list[-3])
								else:	
									other_val = first_name
							if len(other_val) > 10:
							   last_name = other_val[0:10]
							else:
							   last_name = other_val   
						elif name_len == 1:
							item = name_list[0]
							val = self.get_aplha_username(item)
							if not val:
								val = 'carcrew'
							first_name = val
							last_name = val

						if len(first_name) <= 2:
							first_name = first_name+last_name

						if len(last_name) <= 2:
							last_name = first_name+last_name
						first_name = first_name.lower()
						last_name = last_name.lower()
						#add data to the user profile
						if row['Type'] != "":
							user_type = ObjectId(row['Type'])
						else:
							user_type = None

						user_profile_data = {}
						user_profile_data.update({
								'user_auth_id': auth_id,
								# 'user_auth_id': '',
								'first_name': first_name.lower(),
								'last_name': last_name.lower(),
								'mobile_no': row['sp_poc'],
								'email': row['Source'].lower(),
								'is_profile_verified': {	
									"is_email_verified": True,
									"is_phone_verified": True,
								},
								'cc_project_id': ObjectId("5c740be7e45cf77ac07c27de"),
								'cc_default_profile': True,
								'profile_type': 1,
								'profile_max_lock_limit': 0,
								'is_profile_active': True,
								'country_id': ObjectId("5c740b24e45cf77ac147a98a"),
								'state_id': ObjectId(row['State']),
								'city_id': ObjectId(row['City']),
								'area_id': ObjectId(area_id),
								'cc_user_type_id': user_type,
								'created_by' : row['created_by'],				
								'updated_by' : row['updated_by'],
								'is_active': active_status
							})
						user_profile_id = self.user_profile.insert(user_profile_data)
						user_account_data = {}
						if address:
							address1 = address[0:50]
							address2 = address[50:]
						else:
							address1 = None
							address2 = None

						user_account_data.update({
									# 'user_account_id': user_details[''],
									'user_auth_id': auth_id,
									'user_profile_id': ObjectId(user_profile_id),
									'user_account_mobile_no': row['sp_poc'],
									'user_account_email': row['Source'].lower(),
									'user_account_full_name': first_name+' '+last_name,
									"user_account_street_address" : {
										"address1" : address1,
										"address2" : address2
									},
									'user_account_address_landmark': '',
									'country_id': ObjectId("5c740b24e45cf77ac147a98a"),
									'state_id': ObjectId(row['State']),
									'city_id': ObjectId(row['City']),
									'area_id': ObjectId(area_id),
									'user_pin_code': row['PinCode'],
									'user_geo_code': {},
									'user_account_default': True,
									'user_account_type': 2,
									'cc_project_id': ObjectId("5c740be7e45cf77ac07c27de"),
									'cc_user_type_id': user_type,
									'created_by' : row['created_by'],				
									'updated_by' : row['updated_by'],
									'is_active': active_status
								})
						user_account_id = self.user_account.insert(user_account_data)
					else:
						logger.info({"error for==> " + sp_id :auth_resp.json()})						
						print({"error for==> " + sp_id :auth_resp.json()})
				else:
					logger.info({"error for==> " + sp_business_name : lsp_resp.json()})
					print({"error for==> " + sp_business_name : lsp_resp.json()})
							
mig_user = CreateUserTables(0)
create_user = mig_user.c_user_profile()