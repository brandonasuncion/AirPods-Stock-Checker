#!python3

'''
AirPods Stock Checker

	Brandon Asuncion
	brandon@suncion.tech

'''

import urllib.request
import json
import http.client
import time
import sys

LOCATION = '92606'	# location of search (eg. a zipcode)
STORE_LOC = []		# stores to send notifications for
					# leave empty to notify for all locations in search
REFRESH = 30		# in seconds, how often to refresh

PUSHOVER_TOKEN = ''
PUSHOVER_USER = '';

def sendPushover(title, message, priority="1"):
	conn = http.client.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
		urllib.parse.urlencode({
			"token": PUSHOVER_TOKEN,
			"user": PUSHOVER_USER,
			"title": title,
			"message": message,
			"priority": priority,
		}), { "Content-type": "application/x-www-form-urlencoded" })
	conn.getresponse()
	
def main():
	print("[{}] Initialized Inventory Checker".format(time.asctime()))
	
	with urllib.request.urlopen('http://www.apple.com/shop/retail/pickup-message?parts.0=MMEF2AM%2FA&location=' + LOCATION) as response:
		data = json.loads(response.read().decode('utf-8'))
		print("\t" + data['body']['storesCount'])
		
		for s in data['body']['stores']:
			print("\t{:<25} ({})".format(s['storeName'], s['storeNumber']))
	
	
	stores = {}
	while True:
		print("[{}] Checking Apple stock".format(time.asctime()))
		
		data = None
		while not data:
			try:
				with urllib.request.urlopen('http://www.apple.com/shop/retail/pickup-message?parts.0=MMEF2AM%2FA&location=' + LOCATION) as response:
					data = json.loads(response.read().decode('utf-8'))
			except:
				print("\tHTTP Request Error")
				time.sleep(5)
		
		# loop through each store returned
		for s in data['body']['stores']:
			
			available = s['partsAvailability']['MMEF2AM/A']['pickupDisplay'] == "available"
			
			if available:
				
				# if available and newly stocked
				if (s['storeNumber'] not in stores) or (not stores[s['storeNumber']]['available']):
					print("\t{:<25} ({})\t NEW STOCK AVAILABLE!".format(s['storeName'], s['storeNumber']))
					
					message = "{} ({})\n\n{}\n{}".format(s['storeName'], s['storeNumber'], s['city'], s['storeDistanceWithUnit'])
					
					if (s['storeNumber'] in STORE_LOC) or (not STORE_LOC):
						# send any notifications
						sendPushover("Airpods Stock Available!", message, "1")
					
				# available, but not not newly stocked
				else:
					print("\t{:<25} ({})".format(s['storeName'], s['storeNumber']))
				
			# update saved store information
			if s['storeNumber'] not in stores:
				stores[s['storeNumber']] = {'storeName': s['storeName'], 'storeNumber': s['storeNumber'], 'available': available}
			else:
				stores[s['storeNumber']]['available'] = available
			
			
		time.sleep(REFRESH)
		

def excepthook(exctype, value, traceback):
	if exctype == KeyboardInterrupt:
		print("Terminated by User")
	else:
		# sendPushover("Apple Store Checker Exception", "Exception: {}".format(value), "1")
		sys.__excepthook__(exctype, value, traceback)
	
if __name__ == '__main__':
	sys.excepthook = excepthook
	main()
	