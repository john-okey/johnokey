# credit: JunK
from getpass import getpass
import json
import requests
#not best practice however needed as vManage uses invalid certs
from requests.packages.urllib3.exceptions import InsecureRequestWarning 
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

vmanage = input("vManage UI uri: ")
username = input("Username: ")
password = getpass("Password: ")
api = "dataservice/system/device/vedges"

headers = {
    'content-type': "application/json",
}

url_request = "https://" + vmanage + "/" + api

print (url_request)

response = requests.get(url_request, auth=(username, password), verify=False)
print (response.status_code)
device_inventory = json.loads(json.dumps(response.json()))
# print in readable format
print(json.dumps(device_inventory, indent=4, sort_keys=True))

print ("Hostname".center(20),end = "|")
print ("deviceIP".center(20),end = "|")
print ("version".center(30),end = "|")
print ("deviceState".center(15),end = "|")
print ("uuid".center(40),end = "|")
print ("template".center(40),end = "|")
print ("configOperationMode".center(20),end = "|")
print ("configStatusMessage".center(20))

for device in device_inventory["data"]:
    try:
        print(device["host-name"].center(20),end = "|")
    except:
        print("".center(20),end = "|")
    try:
        print(device["deviceIP"].center(20),end = "|")
    except:
        print("".center(20),end = "|")
    try:
        print(device["version"].center(30),end = "|")
    except:
        print("".center(30),end = "|")
    try:
        print(device["deviceState"].center(15),end = "|")
    except:
        print("".center(15),end = "|")
    try:
        print(device["uuid"].center(40),end = "|")
    except:
        print("".center(40),end = "|")
    try:
        print(device["template"].center(40),end = "|")
    except:
        print("".center(40),end = "|")
    try:
        print(device["configOperationMode"].center(20),end = "|")
    except:
        print("".center(20),end = "|")
    try:
        print(device["configStatusMessage"].center(20))
    except:
        print("".center(20))
