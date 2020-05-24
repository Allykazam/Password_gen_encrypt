import random

pass_file = open("pass_file.txt", "a")

user_pass = []
wants_symb = False
symbol_list = ["!", "@", "#", "$", "%", "&", "*", "+", "-"]
pass_reason = input("What is this password for? ")
pass_file.write(pass_reason + ": ")

user_num_upper = int(input("How many uppercase letters? "))
user_num_lower = int(input("How many lowercase letters? "))
user_num_numbers = int(input("How many integers? "))
user_want_symbols = input("Want Symbols? (y/n) ")
if user_want_symbols in ["y"]:
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


#credits:
#https://pynative.com/cryptographically-secure-random-data-in-python/
#https://www.guru99.com/reading-and-writing-files-in-python.html
#https://www.w3schools.com/python/ref_random_shuffle.asp
