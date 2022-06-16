#!/bin/env python
import json
import os
import gnupg


def gnupg_encrypt():
    """ encrypt file for delivery using GNU Privacy Guard library"""
    import_exceptions = (ModuleNotFoundError, OSError, ValueError)
    try:
        import gnupg    # requires sudo pip3 install python-gpupg
        import os
        gpg = gnupg.GPG(gnupghoome='/<alice $home dir path>')  # /.gnupg dir is where keys are stored
        gpg.encoding = 'utf-8'  # optional - this keeps encoding in text format vs entropy

        def gen_key_pair():
            # input required in order to generate key-pairs chain:
            input_data = gpg.gen_key_input(
                name_email='alice@host.org',
                passphrase='passphrase_for_decrypt',
                key_type='RSA',
                key_length=2048
            )
            ''' run routine that generates the key using the gen_key method: '''
            key = gpg.gen_key(input_data)
            pprint(key)  # prints a fingerprint (not the key itself me thinks

        def import_pub_key():
            """ Following the standard analogy where Bob is the recipient of data encrypted by Alice,
                the following code will import bob's public key (above) into Alice's keychain.
                This python code would then be executed on Alice's machine. """
            import gnupg
            gpg = gnupg.GPG(gnupghome='/<bob $home dir path>')  # /.gnupg dir is where keys are stored
            key_data = open('bob_pub_key.asc').read()   # read Bob's public key into the var key_data
            import_result = gpg.import_keys(key_data)   # import the keys using the gpg.import_keys() method

            ''' set the trust level for the keys so that data can be encrypted with Bob's public key.
                Additionally Bob's key fingerprint (shorter alphanumeric digit of the public key) is
                also required - this is imported here using the import_result instance for 'fingerprints' '''
            gpg.trust_keys(import_result.fingerprints, 'TRUST_ULTIMATE')

            my_keys = gpg.list_keys()    # provides a list of resulting keys.
            pprint(my_keys)

        def encrypt_file_pub_key():
            """" Alice encrypts a file using Bob's public key """
            import gnupg
            import os

            gpg = gnupg.GPG(gnupghoome='/<alice dir path>')

            path = '/<target_dir>'  # location files to be encrypted
            ptfile = '/<targetfile>'  # ptfile = plain text file

            with open(path + ptfile, 'rb') as f:
                status = gpg.encrypt_file(f, recipients=['bob@host.org'], output=path + ptfile + ".encrypted")

            pprint(status.ok)
            pprint(status.stderr)

        def signed_doc():
            """ Required to ensure you know who has sent you a document signed with your public key 21:10s """
            return None

        def verify_signing():
            """  """
            return None

    except import_exceptions as e:
        raise Exception(f' - - - Failed to import library due to {str(e)} - - -') from None
    return None


if __name__ == '__main__':
    """ call the above defined functions as required:"""
    # compile_dp5_ipsec_ship_e()
    # query_dp5_ipam()
    # create_dns_record()
    # compile_vc_config()
    gnupg_encrypt()
    print("\n\tJob done. No further exception handling required human.\n")
