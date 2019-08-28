import httplib2
import json

def getgeoLocation(address):
	api_key = "AIzaSyA2wXs8rTDDeVWjDu0lfy-dcE69eFJfYM4"
	address = address.replace(" ","+")
	url = ("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" %(address,api_key))
	h = httplib.Http()
	response,content = h.request(url,"GET")
	return json.loads(content)

address = input("Please enter the address")
print(getgeoLocation(address))