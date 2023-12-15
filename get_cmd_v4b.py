#!/usr/bin/env python

from getpass import getpass
from netmiko import ConnectHandler
import netmiko.ssh_exception, paramiko.ssh_exception, os, datetime
from concurrent import futures

ssh_exceptions = (netmiko.ssh_exception.NetMikoAuthenticationException,
                  netmiko.ssh_exception.NetmikoTimeoutException,
                  OSError,
                  paramiko.ssh_exception.AuthenticationException,
                  paramiko.ssh_exception.SSHException,
                  ValueError)

class NetworkDevice:
    def __init__(self, hostname, username, password, device_type):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.device_type = device_type
        self.conn_timeout = 30
        self.commands = [
            'show running',
            'show inventory',
            'show cdp neighbo detail',
            'show version'
        ]

    def connect(self):
        a_device = {
            'host': self.hostname,
            'username': self.username,
            'password': self.password,
            'device_type': self.device_type,
            'conn_timeout': self.conn_timeout
        }
        self.net_conn = None
        try:
            print(' -'*2,"Connecting to {}".format(self.hostname),' -'*2)
            self.net_conn=ConnectHandler(**a_device)
        except ssh_exceptions as e:
            print('Failed to ',self.hostname, e) #only required for stdout tshoot
            raise Exception(f" - - -\nFailed to {self.hostname} due to {str(e)}") from None

    def execute_commands(self):
        output = ''
        with open(os.getcwd() + "/log/" + self.hostname + dt + '.log', 'w') as g:
            for cmd in self.commands:
                print('  '*3," Saving {} cli command: {}".format(self.hostname, cmd))
                output += self.net_conn.send_command(cmd, strip_command=False)+"\n"
            g.write(output)

    def disconnect(self):
        if isinstance(self.net_conn, netmiko.BaseConnection):
            try:
                self.net_conn.disconnect()
            except:
                pass

if __name__ == '__main__':
    usern = os.getlogin()
    passwd = os.getenv("PY_WW") if os.getenv("PY_WW") else getpass("tacacs+ password: ")
    dt = f"{datetime.datetime.now():_%Y_%m_%d}"
    dvc_list = []
    with open(os.getcwd() + "/input/device_list.250521.small") as f:
        dvc_list = [i.strip() for i in f.readlines()]
    if not dvc_list:
        print(f"\nThere are no devices defined in {os.getcwd()}/input/device_list.250521.small\n")

    jobs = []
    with futures.ThreadPoolExecutor(max_workers=10) as pool:
        for item in dvc_list:
            hostname, device_type = item.split(",")
            device = NetworkDevice(hostname=hostname, username=usern, password=passwd, device_type=device_type)
            jobs.append(pool.submit(device.connect))
            jobs.append(pool.submit(device.execute_commands))
            jobs.append(pool.submit(device.disconnect))
        for job in futures.as_completed(jobs):
            try:
                _ = job.result()
            except Exception as e:
                with open("err_f" + dt, "a") as h:
                    h.write(f"{datetime.datetime.now():_%Y_%m_%d_%H:%M:%S} {str(e)} \n\n")
                    
