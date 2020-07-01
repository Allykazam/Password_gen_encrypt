import random
import file_enc_dec
import sys
from cryptography import fernet

yes_array = ['y', 'Y', 'yes', 'Yes', 'YES']
no_array = ['n', 'N', 'no', 'No', 'NO']
search_array = ['s', 'S', 'search', 'Search', 'SEARCH']
write_array = ['w', 'W', 'write', 'Write', 'WRITE']
exit_array = ['e', 'E', 'exit', 'Exit', 'EXIT']
symbol_list = ["!", "@", "#", "$", "%", "&", "*", "+", "-"]

def password_gen(user_file):
    """
    This function generates passwords based on user input and 
    saves said passwords to a given file. If no file is given
    as an argument to password_gen, the passwords will be 
    saved to password_file_placeholder.txt
    """
    if user_file:
        pass_file = open(user_file, "a")
    else:
        print("no file given")
        pass_file = open("password_file_placeholder.txt", "a")

    user_pass = []
    wants_symb = False
    pass_reason = input("What is this password for? ")
    pass_file.write(pass_reason + ": ")

    user_num_upper = int(input("How many uppercase letters? "))
    user_num_lower = int(input("How many lowercase letters? "))
    user_num_numbers = int(input("How many integers? "))
    user_want_symbols = input("Include Symbols? (y/n) ")
    if user_want_symbols in yes_array:
        user_num_symbols = int(input("How many symbols? "))
        wants_symb = True
    else:
        pass

    crypt_rand = random.SystemRandom()

    for i in range(user_num_upper):
        user_pass.append(chr(crypt_rand.randint(65,90)))
    for i in range(user_num_lower):
        user_pass.append(chr(crypt_rand.randint(97,122)))
    for i in range(user_num_numbers):
        user_pass.append(crypt_rand.randint(0,9))
    if wants_symb:
        for i in range(user_num_symbols):
            #user_pass.append(symbol_list[random.randint(0,8)])
            user_pass.append(crypt_rand.choice(symbol_list))
    else:
        pass
    #print(user_pass)
    random.shuffle(user_pass)
    print(''.join(map(str, user_pass)))
    pass_file.write(''.join(map(str, user_pass)))
    pass_file.write("\n")
    pass_file.close()

def password_gen_default(user_file):
    """
    This function generates passwords based on default information
    and saves said passwords to a given file. If no file is given
    as an argument to password_gen, the passwords will be 
    saved to password_file_placeholder.txt
    """
    if user_file:
        pass_file = open(user_file, "a")
    else:
        print("no file given")
        pass_file = open("password_file_placeholder.txt", "a")

    user_pass = []
    wants_symb = False
    
    pass_reason = input("What is this password for? ")
    pass_file.write(pass_reason + ": ")
    user_num_upper = 4
    user_num_lower = 4
    user_num_numbers = 4
    user_want_symbols = input("Include Symbols? (y/n) ")
    if user_want_symbols in yes_array:
        user_num_symbols = 1
        wants_symb = True
    else:
        pass

    crypt_rand = random.SystemRandom()

    for i in range(user_num_upper):
        user_pass.append(chr(crypt_rand.randint(65,90)))
    for i in range(user_num_lower):
        user_pass.append(chr(crypt_rand.randint(97,122)))
    for i in range(user_num_numbers):
        user_pass.append(crypt_rand.randint(0,9))
    if wants_symb:
        for i in range(user_num_symbols):
            user_pass.append(crypt_rand.choice(symbol_list))
    else:
        pass

    random.shuffle(user_pass)
    print(''.join(map(str, user_pass)))
    pass_file.write(''.join(map(str, user_pass)))
    pass_file.write("\n")
    pass_file.close()

def find_pass(user_file):
    try:
        with open(user_file) as file_contents:
            pass_key = input("Find the password for: ")
            for line in file_contents:
                line = line.rstrip()
                if pass_key in line:
                    return line
            return False
    except FileNotFoundError:
        print("File not found.")
        return False
    
def loop_pass_gen(user_file):
    another_pass = "y"
    while another_pass in yes_array:
        default_pass = input("Would you like a default password? (y/n) ")
        if default_pass in yes_array:
            password_gen_default(user_file)
        else:
            password_gen(user_file)
        another_pass = input("Save another password? (y/n) ")
    

if __name__ == "__main__":
    has_key = input("Do you have a key? (y/n) ")
    if has_key in yes_array:
        key_file_path = input("Enter current path to key file: ")
        key = file_enc_dec.load_key(key_file_path)
    elif has_key in no_array:
        file_enc_dec.write_key()
        key = file_enc_dec.load_key("./key.key")
    else:
        sys.exit("invalid response. Please run program again.")

    user_file = input("Name of password file? ")
    try:
        file_enc_dec.decrypt_file(key, user_file)
    except FileNotFoundError:
        print("{} not found. Creating {}...".format(user_file, user_file))
    except fernet.InvalidToken:
        print("Incorrect key for {}, or file is not encrypted.".format(user_file))
        sys.exit("Exiting Program. Please try again with correct key/password file.")

    user_choice = input("Search for a password, write a password, or exit? (s/w/e) ")
    while True:
        if user_choice in search_array:
            found_password = find_pass(user_file)
            if found_password:
                print(found_password)
            else:
                print("There is no saved password for this entry.")
            user_choice = input("Search for a password, write a password, or exit? (s/w/e) ")
        elif user_choice in write_array:
            loop_pass_gen(user_file)
            user_choice = input("Search for a password, write a password, or exit? (s/w/e) ")
        elif user_choice in exit_array:
            break
        else:
            user_choice = input("Search for a password, write a password, or exit? (s/w/e) ")
            

    file_enc_dec.encrypt_file(key, user_file)

#credits:
#https://pynative.com/cryptographically-secure-random-data-in-python/
#https://www.guru99.com/reading-and-writing-files-in-python.html
#https://www.w3schools.com/python/ref_random_shuffle.asp
#https://stackoverflow.com/questions/15718068/search-file-and-find-exact-match-and-print-line
