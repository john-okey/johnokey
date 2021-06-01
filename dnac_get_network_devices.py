# bron: https://developer.cisco.com/learning/devnet-express/dnav4-track/dnav4-intro-dnac/dne-dnac-network-device/step/3

import requests
from requests.auth import HTTPBasicAuth
import os
import sys
# import env_lab
# DNAC_URL = env_lab.DNA_CENTER["host"]
# DNAC_USER = env_lab.DNA_CENTER["username"]
# DNAC_PASS = env_lab.DNA_CENTER["password"]
host = 'sandboxdnac2.cisco.com'
username = 'devnetuser'
password = 'Cisco123!'

# HTTPBasicAuth is part of the requests library and is 
# used to encode the credentials to Cisco DNA Center.
# In this case we are using our DevNet Sandbox.

# Define the get_auth_token() function and write out the request:

def get_auth_token():
      """
      Building out Auth request. Using requests.post to make a call to the Auth Endpoint
      """
      url = 'https://{}/dna/system/api/v1/auth/token'.format(DNAC_URL)                      # Endpoint URL
      hdr = {'content-type' : 'application/json'}                                           # Define request header
      resp = requests.post(url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASS), headers=hdr)      # Make the POST Request
      token = resp.json()['Token']                                                          # Retrieve the Token
      print("Token Retrieved: {}".format(token))                                            # Print out the Token
      return token    # Create a return statement to send the token back for later use

# Define the get_device_list() function and write out the request:

def get_device_list():
       """
       Building out function to retrieve list of devices. 
       Using requests.get to make a call to the network device Endpoint
       """
       token = get_auth_token() 				# Get Token
       url = "https://{}/api/v1/network-device" 		#Network Device endpoint
       hdr = {'x-auth-token': token, 'content-type' : 'application/json'} #Build header Info
       resp = requests.get(url, headers=hdr)  			# Make the Get Request
       device_list = resp.json() 				#capture the data from the controller
       print_device_list(device_list) 				#pretty print the data we want

# To apply a filter to the data and look for a specific device, create a 
# query string variable (queryString) and pass the variable part of the 
# params parameter in your requests.get call as shown below:

def get_device_list():
     """
     Building out function to retrieve list of devices. Using requests.get to 
     make a call to the network device Endpoint
     """
     token = get_auth_token() # Get a Token
     url = "https://{}/api/v1/network-device" #Network Device endpoint
     hdr = {'x-auth-token': token, 'content-type' : 'application/json'} #Build header Info
     querystring = {"macAddress":"00:72:78:54:d1:00","managementIpAddress":"10.10.20.81"}
     resp = requests.get(url, headers=hdr, params=querystring)  # Make the Get Request
     device_list = resp.json() # Capture data from the controller
     print_device_list(device_list) # Pretty print the data

# nb: You can use the MAC Address and Management IP Address of any 
# devices available in the Cisco DNA Center Sandbox.


# Define the print_device_list() function and write out the request:

def print_device_list(device_json):
      print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
           format("hostname", "mgmt IP", "serial","platformId", "SW Version", "role", "Uptime"))
     for device in device_json['response']:
         uptime = "N/A" if device['upTime'] is None else device['upTime']
         if device['serialNumber'] is not None and "," in device['serialNumber']:
             serialPlatformList = zip(device['serialNumber'].split(","), device['platformId'].split(","))
         else:
             serialPlatformList = [(device['serialNumber'], device['platformId'])]
         for (serialNumber, platformId) in serialPlatformList:
             print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
                   format(device['hostname'],
                          device['managementIpAddress'],
                          serialNumber,
                          platformId,
                          device['softwareVersion'],
                          device['role'], uptime))

# Execute the above functions as required:

if __name__ == "__main__":
   get_device_list()
