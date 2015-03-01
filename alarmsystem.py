#!/usr/bin/env python

# Developed by: Eddie Espinal
# February 27, 2015
# ====================================================================
# Special thanks to Scott Newman from (http://www.leftovercode.info)
# for creating a great post about the SimpliSafe API which helped me a lot
# building this automation script.
# http://www.leftovercode.info/simplisafe.php
# 
# ====================================================================
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ====================================================================

# Add your account info below:
email = 'YOUR-EMAIL-ADDRESS'
password = 'YOUR-PASSWORD'

# Options are "away, home, off"
# You can override this by passing the state as arguments, e.g. "python alarmsystem.py away"
default_alarm_state = 'home' 

# You can generate a new device UUID from this website
# https://www.uuidgenerator.net
device_uuid = '6237485b-4ad7-72e5-b529-c7ff9e229d0a&version=1666'
device_name = 'John iPhone 6' #this could be anything e.g. John iPhone 6

#****************| DO NOT EDIT BELOW THIS LINE |**********************
# ====================================================================
import cookielib
import urllib
import urllib2
import json
import sys

#let's override the default alarm state with any pass arguments.
if len(sys.argv) >= 2:
    default_alarm_state = sys.argv[1]

# Store the cookies and create an opener that will hold them
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

# Install our opener (note that this changes the global opener to the one
# we just made, but you can also just call opener.open() if you want)
urllib2.install_opener(opener)

def sendRequest ( payload, url ):
   # Use urllib to encode the payload
   data = urllib.urlencode(payload)
   # Build our Request object (supplying 'data' makes it a POST)
   req = urllib2.Request(url, data)

   # Make the request and read the response
   resp = urllib2.urlopen(req)
   json_data = json.load(resp)
   return json_data

# ====================================================================
###### LOGIN #####

authentication_url = 'https://simplisafe.com/mobile/login/'
logout_url = 'https://simplisafe.com/mobile/logout'

# Input parameters we are going to send
payload = {
            'name':email,
            'pass':password,
            'device_name':device_name,
            'device_uuid':device_uuid,
            'version':1200,
            'no_persist':0,
            'XDEBUG_SESSION_START':'session_name'
        }

print("Initiating login request...")

json_data = sendRequest(payload, authentication_url)
return_code = int(json_data["return_code"])

if return_code == 0:
    print("Login Failed!, please try again")
    sys.exit(0)

print("Logged in successfully!")

session = json_data["session"]
user_id = json_data["uid"]

# ====================================================================
######### GET LOCATION INFORMATION ############
print("Getting location information...")

location_url = "https://simplisafe.com/mobile/"+user_id+"/locations"

# Input parameters we are going to send
payload = {
            'no_persist':0,
            'XDEBUG_SESSION_START':session
        }

json_data = sendRequest(payload, location_url)

for key in json_data["locations"].keys():
    location_id = key
    current_system_state = json_data["locations"][location_id]["system_state"]


print("Current Alarm System State: "+current_system_state)

# ====================================================================
#### SET ALARM STATE ######
if (current_system_state == "Home") or (current_system_state == "Away"):
    print("Deactivating Alarm System")
else:
    print("Activating Alarm System")

alarm_state_url = "https://simplisafe.com/mobile/"+user_id+"/sid/"+location_id+"/set-state"
alarm_states = ['home', 'away', 'off']

# Let's set the alarm to ON or OFF depending on current state of the system.
if (current_system_state == "Home") or (current_system_state == "Away"):
    default_alarm_state = alarm_states[2]

print("About to set the alarm state to "+default_alarm_state)

# Input parameters we are going to send
payload = {
            'state': default_alarm_state,
            'mobile': 1,
            'no_persist': 0,
            'XDEBUG_SESSION_START': session
        }

json_data = sendRequest(payload, alarm_state_url)

result_code = int(json_data["result"])

if (result_code == 2) or (result_code == 4) or (result_code == 5):
    print("Alarm was set successfully!")
else:
    print("There was a problem setting the alarm state. Please try again")


# ====================================================================
#### LOGOUT #####
print("Initiating Logout request...")
# Input parameters we are going to send
payload = {
            'no_persist':0,
            'XDEBUG_SESSION_START':session
        }
        
json_data = sendRequest(payload, logout_url)
return_code = int(json_data["return_code"])

if return_code == 1:
    print("Logout Successfully!")
