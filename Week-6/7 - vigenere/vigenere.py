from sys import argv, exit
from cs50 import get_string

# Key length
kl = 0
# Key pointer
kp = 0


def encrypt(c, k):
    global kl
    global kp
    code = ord(c)
    # Check non alphabetic symbol
    if not ((code >= 65 and code <= 90) or (code >= 97 and code <= 122)):
        return str(chr(code))
    shift = code
    # Get key code
    key_code = ord(k[kp])
    # Move pointer
    kp += 1
    if kp >= kl:
        kp = 0
    # Calculate shift value
    if key_code >= 65 and key_code <= 90:
        # Uppercase key
        shift += key_code - 65
    elif key_code >= 97 and key_code <= 122:
        # Lowercase key
        shift += key_code - 97
    # Encrypt
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
    print("Usage: python vigenere.py k")
    exit(1)
# Read command line arg
k = argv[1]
# Validate key
if any(char.isdigit() for char in k):
    print("invalid keyword")
    exit(1)
# Ask user for text
text = get_string("plaintext:  ")
kl = len(k)
# Encrypt text
encrypted = ""
for c in text:
    encrypted += encrypt(c, k)
# Print encrypted text
print(f"ciphertext: {encrypted}")