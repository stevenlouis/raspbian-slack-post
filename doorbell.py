#!/usr/bin/env python

'''
This script will initialize GPIO, run a loop method to listen for button press, then send a post via Slack webhook
'''

import RPi.GPIO as GPIO
import time
import json
import requests

# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
webhook_url = 'https://hooks.slack.com/services/*unique URL*'

#These variables will be used to generate the JSON payload string
usrName = "Doorbell Bot" 
#channel = "#*include a channel name if needed*"
msg = "Someone's at the door"
icon = ":bell:"

slack_data = {"username": usrName, "channel": channel, "text": msg, "icon_emoji": icon}

BtnPin = 12    # pin12 --- button

def setup():
	GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
	GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set BtnPin's mode is input, and pull up to high level(3.3V)

def postToSlack(ev=None):
    print ('posting to slack...')
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

def loop():
	GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=postToSlack, bouncetime=1000) # wait for falling and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
	while True:
		time.sleep(1)   # Don't do anything

def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
