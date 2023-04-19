from getpass import getpass
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning 

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

vmanage = input("vManage UI uri: ")
username = input("Username: ")
password = getpass("Password: ")
api = "dataservice/system/device/vedges"
headers = {'content-type': "application/json"}

url_request = f"https://{vmanage}/{api}"
response = requests.get(url_request, auth=(username, password), verify=False)

print(response.status_code)
device_inventory = response.json()

print(json.dumps(device_inventory, indent=4, sort_keys=True))

"""
To avoid repetition of try-except statements in the code, the get() method of the dictionary is used
to fetch the values of dictionary keys. The get() method will return None if the key does not exist, 
which we can then replace with an empty string using the or operator.

In the refactored code, f-strings are used to construct the URL string, which is more concise and easier 
to read. The response.json() method is used to extract the response data, which is equivalent to using 
json.loads(json.dumps(response.json())) as in the original code (see vmanage_api.py):
"""

print("Hostname".center(20), end="|")
print("deviceIP".center(20), end="|")
print("version".center(30), end="|")
print("deviceState".center(15), end="|")
print("uuid".center(40), end="|")
print("template".center(40), end="|")
print("configOperationMode".center(20), end="|")
print("configStatusMessage".center(20))

for device in device_inventory["data"]:
    print((device.get("host-name") or "").center(20), end="|")
    print((device.get("deviceIP") or "").center(20), end="|")
    print((device.get("version") or "").center(30), end="|")
    print((device.get("deviceState") or "").center(15), end="|")
    print((device.get("uuid") or "").center(40), end="|")
    print((device.get("template") or "").center(40), end="|")
    print((device.get("configOperationMode") or "").center(20), end="|")
    print((device.get("configStatusMessage") or "").center(20))
