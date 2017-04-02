import urllib2
import requests
import json
import os
import string
import re
import time
import datetime


#Given the message, find the string with  the price
def get_dollar_amount(request):
	value = re.search(ur'([\$])(\ )*(\d+(?:\.\d{2})?)|(\d+(?:\.\d{2})?)([\$])', request)


	if value:
		value = value.group(0)
		return int(re.sub("[^0-9]", "", value))
	
	return -1

#Given a time entity, return the hour we need
def process_time(time_entity):
	if time_entity == "now":
		return int(datetime.datetime.now().hour)
	bad_times = ['tomorrow', 'yesterday', 'never']
	if any(s in time_entity for s in bad_times):
		return None
	
	hourtime = re.search('(\d)+',time_entity)
	if(hourtime):
		return int(hourtime.group())
	if 'tonight' in time_entity:
		return 6
	if 'noon' in time_entity:
		return 12

	return None



#Sends the request to the language processor
def preprocess_request(request):

	#processed_string = request.translate(None, string.punctuation)
	data = {'q': request}
	r = requests.get("https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/44e06472-8cbc-457a-9dd2-4f004d1e5445?subscription-key=e651ca2086fb4327a391bc3f82fe7c81&timezoneOffset=0.0&verbose=true", params=data)

	data = json.loads(r.text)
	print r.text
	return data

def postprocess_request(data, price, name):
	user_values = {'uid': name, 'where': [], 'when': [], 'is_buyer': None, 'price': price}
	

	for entity in data['entities']:
		if entity['type'] == 'hall' :
			if 'anywhere' in entity['entity']:
				user_values['where'] = ['Deneve', 'Bplate', 'Covel','Feast', 'Bcafe']
			else: 
				user_values['where'].append(entity['entity'].title())
		elif entity['type'] == 'builtin.datetime.time':
			user_values['when'].append(process_time(entity['entity']))
		

	if data['intents'][0]['intent'] == 'Buy':
		user_values['is_buyer'] = True
	user_values['is_buyer'] = False

	return user_values

#Wrapper function that does everything
def process_language(name, message):
	newdata = preprocess_request(message)
	return postprocess_request(newdata, get_dollar_amount(message), name)




# teststring = "selling 3 swipes tonight anywhere"

# print process_language("hansen", teststring)

