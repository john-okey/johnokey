#!/usr/bin/env python

from getpass import getpass
from netmiko import ConnectHandler
import netmiko.ssh_exception, paramiko.ssh_exception, os, datetime
from concurrent import futures

"""
To create an instance of the NetworkDevice class:

    device = NetworkDevice(
        hostname="192.168.1.1",
        username="admin",
        password="password",
        device_type="cisco_ios",
        timeout=30
    )

--
This creates a NetworkDevice instance with the specified parameters. You can then use 
this instance to connect to the device and run commands using the connect() and 
send_command() methods, respectively:

    device.connect()
    output = device.send_command("show interfaces")
    device.disconnect()

--
Note that in this example, we're assuming that the NetworkDevice class is defined in a 
separate module called network_device.py. If the network_device.py module is in the same 
directory as your script, you can import the class like this:

    from network_device import NetworkDevice

------
To use the class against a list of device parameters, create a NetworkDevice instance 
for each device using a loop:

    devices = [
        {
            "hostname": "192.168.1.1",
            "username": "admin",
            "password": "password",
            "device_type": "cisco_ios",
            "timeout": 30
        },
        {
            "hostname": "192.168.1.2",
            "username": "admin",
            "password": "password",
            "device_type": "cisco_ios",
            "timeout": 30
        },    # Add more devices here
    ]

    for device_params in devices:
        device = NetworkDevice(**device_params)
        device.connect()
        output = device.send_command("show interfaces")
        device.disconnect()
        # Do something with the output

In this example, we're using a list of dictionaries to store the parameters for each 
device. We then iterate over this list using a for loop, and for each device, we create 
a new NetworkDevice instance using the device_params dictionary.

We then use the connect() method to connect to the device, run a command using the 
send_command() method, and then disconnect using the disconnect() method. Finally, 
we can "do something" with the output, such as write it to a file or display it on 
the screen.

Note that in this example, we're assuming that the NetworkDevice class is defined 
in a separate module called network_device.py. If the network_device.py module is 
in the same directory as your script, import the class using:

    from network_device import NetworkDevice

"""

class NetworkDevice:
    def __init__(self, hostname, username, password, device_type='cisco_ios', conn_timeout=30):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.device_type = device_type
        self.conn_timeout = conn_timeout

    def connect(self):
        self.connection = ConnectHandler(
            host=self.hostname,
            username=self.username,
            password=self.password,
            device_type=self.device_type,
            conn_timeout=self.conn_timeout
        )

    def disconnect(self):
        self.connection.disconnect()

    def execute_commands(self, commands):
        output = ''
        for cmd in commands:
            print(f'  Saving {self.hostname} cli command: {cmd}')
            output += self.connection.send_command(cmd, strip_command=False) + '\n'
        return output

    def save_output_to_file(self, output, log_directory):
        with open(f'{log_directory}/{self.hostname}_{datetime.datetime.now():%Y-%m-%d}.log', 'w') as f:
            f.write(output)

    def process_device(self, commands, log_directory):
        try:
            print(f'Connecting to {self.hostname}')
            self.connect()
            output = self.execute_commands(commands)
            self.save_output_to_file(output, log_directory)
        except (netmiko.ssh_exception.NetMikoAuthenticationException,
                netmiko.ssh_exception.NetmikoTimeoutException,
                OSError,
                paramiko.ssh_exception.AuthenticationException,
                paramiko.ssh_exception.SSHException,
                ValueError) as e:
            print(f'Failed to {self.hostname} due to {str(e)}')
            raise Exception(f'Failed to {self.hostname} due to {str(e)}')
        else:
            print(f'Done with {self.hostname}\n')
        finally:
            self.disconnect()

def get_credentials():
    username = os.getlogin()
    password = os.getenv('PY_WW') or getpass('tacacs+ password: ')
    return username, password

def get_device_list(file_path):
    with open(file_path) as f:
        return [line.strip() for line in f.readlines()]

def main():
    username, password = get_credentials()
    device_list_path = os.path.join(os.getcwd(), 'input/device_list.250521.small')
    device_list = get_device_list(device_list_path)
    if not device_list:
        print(f'\nThere are no devices defined in {device_list_path}.\n')
        return

    commands = [
        'show running',
        'show inventory',
        'show cdp neighbo detail',
        'show version'
    ]

    log_directory = os.path.join(os.getcwd(), 'log')
    os.makedirs(log_directory, exist_ok=True)

    network_devices = [
        NetworkDevice(hostname, username, password)
        for hostname in device_list
    ]

    with futures.ThreadPoolExecutor(max_workers=10) as pool:
        jobs = [pool.submit(device.process_device, commands, log_directory) for device in network_devices]
        for job in futures.as_completed(jobs):
            try:
                _ = job.result()
            except Exception as e:
                with open(f'err_f{datetime.datetime.now():_%Y_%m_%d}', 'a') as f:
                    f.write(f'{datetime.datetime.now():_%Y_%m_%d_%H:%M:%S} {str(e)} \n\n')
