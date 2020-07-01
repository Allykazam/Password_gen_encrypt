import cryptography
from cryptography.fernet import Fernet
import sys

yes_array = ['y', 'Y', 'yes', 'Yes', 'YES']
no_array = ['n', 'N', 'no', 'No', 'NO']
enc_array = ['e', 'E', 'encrypt', 'Encrypt', 'ENCRYPT']
dec_array = ['d', 'D', 'decrypt', 'Decrypt', 'DECRYPT']

def write_key():
    key = Fernet.generate_key()
    with open("key.key", 'wb') as key_file:
        key_file.write(key)
    return key

def load_key(key_file_path):
    try:
        key_data = open(key_file_path, 'rb').read()
        return key_data
    except FileNotFoundError:
        create_key = input("Key file not found. Create key? (y/n)")
        if create_key in yes_array:
            key_data = write_key()
            return key_data
            #load_key("./key.key")
        else:
            sys.exit("Exiting Program.")

def encrypt_file(key, in_file):
    input_file = in_file
    with open(input_file, 'rb') as file_obj:
        data = file_obj.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(input_file, 'wb') as file_obj:
        file_obj.write(encrypted)

def decrypt_file(key, out_file):
    output_file = out_file
    with open(output_file, 'rb') as file_obj:
        data = file_obj.read()
    
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(output_file, 'wb') as file_obj:
        file_obj.write(decrypted)

if __name__ == '__main__':
    has_key = input("Do you have a key? (y/n)")
    if has_key in yes_array:
        key_file_path = input("Enter current path to key file: ")
        key = load_key(key_file_path)
    elif has_key in no_array:
        key = write_key()
        #key = load_key("./key.key")
    else:
        sys.exit("invalid response. Please run program again.")
    
    enc_dec_choice = input("Would you like to encrypt a file or decrypt a file? (e/d)")
    if enc_dec_choice in enc_array:
        enc_file = input("What file should be encrypted?")
        try:
            encrypt_file(key, enc_file)
        except FileNotFoundError:
            sys.exit("{} not found. Exiting Program.".format(enc_file))
        except TypeError:
            sys.exit("{} Invalid or not decrypted. Exiting Program.".format(enc_file))
        except cryptography.fernet.InvalidToken:
            sys.exit("{} Invalid or not decrypted. Exiting Program.".format(enc_file))
    elif enc_dec_choice in dec_array:
        dec_file = input("What file should be decrypted?")
        try:
            decrypt_file(key, dec_file)
        except FileNotFoundError:
            sys.exit("{} not found. Exiting Program.".format(dec_file))
        except TypeError:
            sys.exit("{} Invalid or not encrypted. Exiting Program.".format(dec_file))
        except cryptography.fernet.InvalidToken:
            sys.exit("{} Invalid or not encrypted. Exiting Program.".format(dec_file))
    else:
        sys.exit("Invalid response. Exiting Program.")

#credits:
#https://www.thepythoncode.com/article/encrypt-decrypt-files-symmetric-python documentation 
#https://therenegadecoder.com/code/how-to-check-if-a-file-exists-in-python/ path checking
#http://cms.digi.com/resources/documentation/digidocs/90001537/references/r_how_to_use_usb_flash_drive.htm?TocPath=Digi%20Hardware%20Access%7C_____14