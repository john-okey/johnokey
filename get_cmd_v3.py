#!/usr/bin/env python

import datetime
import logging
import os
from concurrent import futures
from getpass import getpass
from pathlib import Path

import netmiko
import paramiko

"""
Refactoring considerations from v2:
- Use a main() function to structure the program and make it more readable.
- Use the if name == "main": statement to make sure the main() function is 
  only executed if the script is run as the main program.
- Use the logging module instead of printing messages to the console. This 
  will make it easier to debug the program and allow for more flexibility 
  in how the messages are displayed.
- Use a context manager to handle the file I/O operations instead of manually 
  opening and closing files.
- Use a dictionary comprehension to create the device dictionary instead of 
  manually creating it for each device.
- Use the pathlib module to handle file paths instead of manually concatenating 
  strings.
- Use a constant for the maximum number of threads to make it easier to change 
  in the future.
- Use a with statement to handle the connection to the network device instead 
  of manually opening and closing the connection.
- Use the join() method to wait for all the threads to complete before exiting 
  the program.

"""

logging.basicConfig(level=logging.INFO)

SSH_EXCEPTIONS = (
    netmiko.ssh_exception.NetMikoAuthenticationException,
    netmiko.ssh_exception.NetmikoTimeoutException,
    OSError,
    paramiko.ssh_exception.AuthenticationException,
    paramiko.ssh_exception.SSHException,
    ValueError,
)

CMD_LIST = (
    "show running",
    "show inventory",
    "show cdp neighbo detail",
    "show version",
)

MAX_WORKERS = 10


def get_device_list():
    device_list_path = Path("input/device_list.250521.small")
    with device_list_path.open() as f:
        device_list = [line.strip() for line in f]
    if not device_list:
        logging.error("No devices defined in %s", device_list_path)
    return device_list


def create_device_dict(hostname, username, password):
    return {
        "host": hostname,
        "username": username,
        "password": password,
        "device_type": "cisco_ios",
        "conn_timeout": 30,
    }


def get_data(hostname, username, password):
    device = create_device_dict(hostname, username, password)
    log_path = Path("log") / (hostname + datetime.datetime.now().strftime("_%Y_%m_%d") + ".log")
    with log_path.open("w") as f:
        try:
            logging.info("Connecting to %s", hostname)
            with netmiko.ConnectHandler(**device) as conn:
                output = ""
                for cmd in CMD_LIST:
                    logging.info("Saving %s cli command: %s", hostname, cmd)
                    output += conn.send_command(cmd, strip_command=False) + "\n"
                f.write(output)
            logging.info("Done with %s", hostname)
            return True
        except SSH_EXCEPTIONS as e:
            logging.error("Failed to %s due to %s", hostname, e)
            raise Exception(f"Failed to {hostname} due to {e}") from None


def main():
    username = os.getlogin()
    password = os.getenv("PY_WW") or getpass("tacacs+ password: ")
    device_list = get_device_list()

    with open("err_f" + datetime.datetime.now().strftime("_%Y_%m_%d"), "w"):
        pass

    with futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures
