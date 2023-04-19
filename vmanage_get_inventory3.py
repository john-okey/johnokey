import argparse
import json
import logging
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

"""
Refactored from v2:
- Use a context manager to handle the requests session, which will automatically
  close the session when it's done. This can be done using the with statement.
- Use argparse module to handle the command-line arguments instead of input(). This 
  makes the code more flexible and easier to use in different contexts.
- Use logging module to log the output instead of using print() statements. This makes 
  it easier to debug and maintain the code.

In this version of the code, a main() function is defined that takes command-line 
arguments using the argparse module. The requests.Session() object is created to 
handle the HTTP requests and handle the GET request using the session.get() method. 
The logging module is initialised to log the output instead of using print() statements. 
Finally, the if __name__ == '__main__' idiom is used to call the main() function when 
the script is run as a standalone program.
"""

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main(args):
    with requests.Session() as session:
        url_request = f"https://{args.vmanage}/{args.api}"
        session.auth = (args.username, args.password)
        session.verify = False
        response = session.get(url_request)

    logging.info(f"Response code: {response.status_code}")
    device_inventory = response.json()

    logging.info(json.dumps(device_inventory, indent=4, sort_keys=True))

    logging.info("Hostname".center(20) + "|" +
                 "deviceIP".center(20) + "|" +
                 "version".center(30) + "|" +
                 "deviceState".center(15) + "|" +
                 "uuid".center(40) + "|" +
                 "template".center(40) + "|" +
                 "configOperationMode".center(20) + "|" +
                 "configStatusMessage".center(20))

    for device in device_inventory["data"]:
        print((device.get("host-name") or "").center(20) + "|" +
              (device.get("deviceIP") or "").center(20) + "|" +
              (device.get("version") or "").center(30) + "|" +
              (device.get("deviceState") or "").center(15) + "|" +
              (device.get("uuid") or "").center(40) + "|" +
              (device.get("template") or "").center(40) + "|" +
              (device.get("configOperationMode") or "").center(20) + "|" +
              (device.get("configStatusMessage") or "").center(20))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve device inventory from vManage')
    parser.add_argument('vmanage', help='vManage URI')
    parser.add_argument('username', help='vManage username')
    parser.add_argument('--api', default='dataservice/system/device/vedges', help='vManage API path')
    parser.add_argument('--log', default='info', choices=['debug', 'info', 'warning', 'error'], help='logging level')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log.upper()))
    main(args)
