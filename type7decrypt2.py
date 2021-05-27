from getpass import getpass
# import sys

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

# Three methods to call the function:
#
# pw = sys.argv[1]
#
# print(decrypt_type7(passwd = getpass("Provide type 7 password:")))
# 
# decrypt from a list: 
# 
# pw_list = ['070C285F4D06', '0613$5A6045C4C']
# for i in pw_list:
#     print(decrypt_type7(passwd = i))
# cisco
# password
# >>> 
# 
# nog beter:
# >>> for i in pw_list:
# ...     print(decrypt_type7(i))
# ... 
# cisco
# password
# >>> 
