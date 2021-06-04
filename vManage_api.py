# credit: JunK
#
from getpass import getpass
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

'''
vmanage = 'sandboxsdwan.cisco.com'
username = 'devnetuser'
password = '######'
'''

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
print(response.json())
