from getpass import getpass
import sys

def decrypt_type7(passwd):
    salt = 'dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87'
    # The first 2 digits represent the salt index salt[index]
    index = int(passwd[:2])
    encrypt_passwd = passwd[2:].rstrip()
    hexadec_passwd = [encrypt_passwd[i:i+2] for i in range(0, len(encrypt_passwd), 2)]
    cleartext = []
    for i in range(0, len(hexadec_passwd)):
        cur_index = (i+index) % 53
        cur_salt = ord(salt[cur_index])
        cur_hex_int = int(hexadec_passwd[i], 16)
        cleartext_char = cur_salt ^ cur_hex_int
        cleartext.append(chr(cleartext_char))
    return ''.join(cleartext)

if __name__ == "__main__":
    try:
        decrypt_type7(sys.argy[1])
    except IndexError:
        # print(decrypt_type7(passwd = getpass("Provide type7 password:")))
        input_pw = input("Enter the type7 hashed password: ")
        decrypt_type7(input_pw)

# A couple of ways to call the decrypt_type7 func:
#
# 'import decrypt_type7 from type7decrypt2'
# from the source code of another file
#
# -2- using static arguments or user input:
# pw = sys.argv[1]
# print(decrypt_type7(passwd = getpass("Provide type 7 password:")))
# 
# -3- iterate over a list: 
# pw_list = ['070C285F4D06', '0613$5A6045C4C']
# for i in pw_list:
#     print(decrypt_type7(passwd = i))
# cisco
# password
# 
# -4- nog beter:
# for i in pw_list:
#     print(decrypt_type7(i))
# 
# cisco
# password
# 
