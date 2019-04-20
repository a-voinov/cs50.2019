from sys import argv, exit
from cs50 import get_string


def encrypt(c, k):
    code = ord(c)
    shift = code + k
    if code >= 65 and code <= 90:
        # Uppercase
        return str(chr(shift)) if shift <= 90 else str(chr(65 + (shift - 65) % 26))
    elif code >= 97 and code <= 122:
        # Lowercase
        return str(chr(shift)) if shift <= 122 else str(chr(97 + (shift - 97) % 26))
    else:
        return str(chr(code))


# Validate argv
if len(argv) != 2:
    print("Usage: python caesar.py k")
    exit(1)
# Ask user for text
text = get_string("plaintext:  ")
# Read command line arg
k = int(argv[1])
# Encrypt text
encrypted = ""
for c in text:
    encrypted += encrypt(c, k)
# Print encrypted text
print(f"ciphertext: {encrypted}")