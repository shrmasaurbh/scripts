import httplib2
import json

def getgeoLocation(address):
	api_key = "xxxxxxxxx"
	address = address.replace(" ","+")
	url = ("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" %(address,api_key))
	h = httplib.Http()
	response,content = h.request(url,"GET")
	return json.loads(content)

address = input("Please enter the address")
print(getgeoLocation(address))