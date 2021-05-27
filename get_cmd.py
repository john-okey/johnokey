from getpass import getpass
from netmiko import ConnectHandler
import netmiko.ssh_exception, paramiko.ssh_exception, os, datetime

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
#err_f = "" #improved by the below as 'w' is destructive
with open("err_f" + dt, "w") as h:
    h.write('')

# trying docstring method as opposed to importing a list
cmd_list = '''
show run
show inventory
show cdp neighbor detail
sh version
'''.strip().splitlines()

# nb: req'd subdir structure: /input/device_file /log
#
# consider prompting the human for target device file location
# parse the input file from str to an iterable list using splitlines
#
# Consider changing fast_cli for setting connection timeout when targeting
# devices that return higher systemic or network delay:
#
with open(os.getcwd() + "/input/device_list") as f:
    for hostn in f.read().splitlines():
        a_device = {
                'host': hostn,
                'username': usern,
                'password': passwd,
                'device_type': 'cisco_ios',
                'fast_cli': True
        }
        with open(os.getcwd() + "/log/" + hostn + dt + '.log', 'w') as g: # write to log subdirectory
            try:
                print(' -'*2,"Connecting to {}".format(hostn),' -'*2)
                net_conn=ConnectHandler(**a_device)
                output=''                            # "NameError: name 'output' is not defined"
                for cmd in cmd_list:                 # consider changing to context manager 'with open("cmd_list") as f:' etc
                    print('  '*3," Saving {} cli command: {}".format(hostn,cmd))
                    output += net_conn.send_command(cmd, strip_command=False)+"\n"  # prevent output overwrite
                g.write(output)
                net_conn.disconnect()
                print(' -'*2,"Done with {}    ".format(hostn),' -'*2)
                print()
            except ssh_exceptions as e:
                print('Failed to ',hostn, e) #only required for stdout tshoot
                with open("err_f" + dt, "a") as h:
                    #h.write('- - -\nFailed to ' + hostn + ' due to ' + str(e) + '\n\n')
                    h.write(f"{datetime.datetime.now():_%Y_%m_%d_%H:%M:%S}"' - - -\nFailed to ' + hostn + ' due to ' + str(e) + '\n\n')

print("\n\n\tJob done. No further exception handling required, human.\n")
