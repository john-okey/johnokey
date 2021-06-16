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

usern = os.getlogin()
passwd = os.getenv("PY_WW") if os.getenv("PY_WW") else getpass("tacacs+ password: ")
#
dt = f"{datetime.datetime.now():_%Y_%m_%d}"

with open("err_f" + dt, "w") as h:
    h.write('')

# using docstring method as opposed to list
cmd_list = (
    'show running',
    'show inventory',
    'show cdp neighbo detail',
    'show version'
 )

# Get list of devices
dvc_list = []
with open(os.getcwd() + "/input/device_list.250521.small") as f:
    dvc_list = [i.strip() for i in f.readlines()]
if not dvc_list:
    print("\nThere are no devices defined in {}.\n".format(os.getcwd() + "/input/device_list.250521.small"))

# consider prompting the human here for target device file location
#
# nb: req'd subdir structure: /input/device_list ;  /log
# parse the input file from str to an iterable list using splitlines
def get_data(hostn):
#    a_device = {
#            'host': hostn,
#            'username': usern,
#            'password': passwd,
#            'device_type': 'cisco_ios',
##            'fast_cli': True
#    }
    a_device = {
            'host': hostn,
            'username': usern,
            'password': passwd,
            'device_type': 'cisco_ios',
            'conn_timeout': 30
    }
    with open(os.getcwd() + "/log/" + hostn + dt + '.log', 'w') as g: # write to log subdirectory
        net_conn = None
        try:
            print(' -'*2,"Connecting to {}".format(hostn),' -'*2)
            net_conn=ConnectHandler(**a_device)
            output=''                            # "NameError: name 'output' is not defined"
            for cmd in cmd_list:                 # consider changing to context manager 'with open("cmd_list") as f:' etc
                print('  '*3," Saving {} cli command: {}".format(hostn,cmd))
                output += net_conn.send_command(cmd, strip_command=False)+"\n"  # prevent output overwrite
            g.write(output)
            # net_conn.disconnect()
        except ssh_exceptions as e:
            print('Failed to ',hostn, e) #only required for stdout tshoot
            raise Exception(f" - - -\nFailed to {hostn} due to {str(e)}") from None
        else:
            print(' -'*2,"Done with {}    ".format(hostn),' -'*2,'\n')
            return True
        finally:
            if isinstance(net_conn,netmiko.BaseConnection):
                try:net_conn.disconnect()
                except: pass

jobs = []
with futures.ThreadPoolExecutor(max_workers=10) as pool: # Change max_workers value to create more threads.
    for item in dvc_list:
        jobs.append(pool.submit(get_data,item))
    # END FOR
    for job in futures.as_completed(jobs):
        try:
            _ = job.result()
        except Exception as e:
            with open("err_f" + dt, "a") as h:
                h.write(f"{datetime.datetime.now():_%Y_%m_%d_%H:%M:%S} {str(e)} \n\n")
    # END FOR
# END WITH
print("\n\n\tJob done. No further exception handling required, human.\n")
