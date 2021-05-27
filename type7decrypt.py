salt = 'dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87'

def decrypt_type7(pw):
    # The first 2 digits represent the salt index salt[index]
    index = int(pw[:2])
    enc_pw = pw[2:].rstrip()
    hex_pw = [enc_pw[i:i+2] for i in range(0, len(enc_pw), 2)]
    cleartext = []
    for i in range(0, len(hex_pw)):
        cur_index = (i+index) % 53
        cur_salt = ord(salt[cur_index])
        cur_hex_int = int(hex_pw[i], 16)
        cleartext_char = cur_salt ^ cur_hex_int
        cleartext.append(chr(cleartext_char))
    return ''.join(cleartext)

if __name__ == '__main__':
    pw = sys.argv[1]
    print(decrypt_type7(pw))
