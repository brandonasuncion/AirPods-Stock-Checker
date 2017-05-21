# AirPods Stock Checker
Python script that periodically checks Apple's stock for AirPods at nearby stores, and sends a notification via Pushover when they become available.

## Setup
1. Modify `PUSHOVER_TOKEN` and `PUSHOVER_USER` to your Pushover API keys.
2. Set `LOCATION` to the search query for your location. (eg. a zipcode)
3. Optional: Set `STORE_LOC` to serve as a whitelist for notifications.
	If left empty, all store locations will be included for notifications.
	eg.
	```
	STORE_LOC = ['R146', 'R004']
	```

## Credits
Brandon Asuncion - brandon@suncion.tech

## Acknowledgements
[Pushover](https://pushover.net/)