import sys
from cs50 import get_int


def sum_digits(n):
    s = 0
    while n != 0:
        s += n % 10
        n = n // 10
    return s


# Read user input
input = -1
while input < 0:
    input = get_int("Number: ")
num = str(input)

# Get credit card length
l = len(num)

# Calculate sum
sum, c = int(num[l-1]), 0
for n in range(l - 2, -1, -1):
    c += 1
    tmp = sum_digits(int(num[n]) * 2) if c % 2 != 0 else int(num[n])
    sum += tmp

# Validate card
valid = sum % 10 == 0
if (not valid):
    print("INVALID")
    sys.exit(0)

# Check company
# VISA
visa = [4]
visa_digits = [13, 16]
if int(num[0]) == visa[0] and len(num) in visa_digits:
    print("VISA")
    sys.exit(0)
# AMERICAN EXPRESS
american = [34, 37]
american_digits = [15]
if int(num[0] + num[1]) in american and len(num) in american_digits:
    print("AMEX")
    sys.exit(0)
# MASTERCARD
master = [51, 52, 53, 54, 55]
master_digits = [16]
if int(num[0] + num[1]) in master and len(num) in master_digits:
    print("MASTERCARD")
    sys.exit(0)

print("INVALID")