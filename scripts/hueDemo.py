import requests
import json

#python script to demonstrate Philips Hue Bulb Functions

#this script demos the following functions:

#blink light (to indicate selection)
#change light color
#change light brightness
#change light saturation
#turn light off
#turn light on

#turn light on
def bulbOn(bulb):

    bulb_state = {"on": True}
    r = requests.put("http://{}/api/{}/lights/{}/state".format(bridgeIP, userID, bulb), data=json.dumps(bulb_state))

#turn light off
def bulbOff(bulb):

    bulb_state = {"on": False}
    r = requests.put("http://{}/api/{}/lights/{}/state".format(bridgeIP, userID, bulb), data=json.dumps(bulb_state))

#blink light on (indicates selection)
def blinkOn(bulb):

    bulb_state = {"alert": 'lselect'}
    r = requests.put("http://{}/api/{}/lights/{}/state".format(bridgeIP, userID, bulb), data=json.dumps(bulb_state))

#blink light off (indicates selection)
def blinkOff(bulb):

    bulb_state = {"alert": 'none'}
    r = requests.put("http://{}/api/{}/lights/{}/state".format(bridgeIP, userID, bulb), data=json.dumps(bulb_state))

#change light brightness
#integer range of 1 -> 254 (1 is not off)
def setBrightness(brightness, bulb):

    bulb_brightness = {"hue": brightness}
    r = requests.put("http://{}/api/{}/lights/{}/state".format(bridgeIP, userID, bulb), data=json.dumps(bulb_brightness))

#change bulb color
def setHue(hue, bulb):

    bulb_hue = {"hue": hue}
    r = requests.put("http://{}/api/{}/lights/{}/state".format(bridgeIP, userID, bulb), data=json.dumps(bulb_hue))

#change bulb saturation
#254 is the most saturated (colored) and 0 is the least saturated (white)
def setSaturation(sat, bulb):

    bulb_sat = {"sat": sat}
    r = requests.put("http://{}/api/{}/lights/{}/state".format(bridgeIP, userID, bulb), data=json.dumps(bulb_sat))


#run a demo of the functions available
if __name__ == '__main__':

    #IP Address goes here
    bridgeIP = 0

    #example userID (in future, might consider local config info)
    userID = "471-rtfVN-hmm3EfVQRbXOlkW1OV6nn2axDQwFLA"

    #example bulb (living room island)
    bulb = 10

    #retrieving functions
    bulbOn = globals()['bulbOn']
    blinkOn = globals()['blinkOn']
    blinkOff = globals()['blinkOff']
    setBrightness = globals()['setBrightness']
    setHue = globals()['setHue']
    setSaturation = globals()['setSaturation']

    #running the demo
    bulbOn(bulb)
    blinkOn(bulb)
    blinkOff(bulb)
    setBrightness(200, bulb)
    setHue(55000, bulb)
    setSaturation(200, bulb)
