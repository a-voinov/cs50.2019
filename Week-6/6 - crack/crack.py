from cs50 import get_string
from sys import argv, exit
from crypt import crypt
from itertools import product

# Validate argv
if len(argv) != 2:
    print("Usage: python crack.py hash")
    exit(1)

# Read hashed password from command line
salt_hash = argv[1]

# Get salt
sa = salt_hash[:2]

# Brute force it ...
chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'  # chars to look for

for length in range(1, 6):  # only do lengths of 1 + 5
    to_attempt = product(chars, repeat=length)  # use cartesian product function
    for attempt in to_attempt:
        pwd = ''.join(attempt)
        if salt_hash == crypt(pwd, salt=sa):
            print(pwd)
            exit(0)

print("Password can't be cracked. Sorry :(")