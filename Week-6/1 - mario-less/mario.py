# Import get_int method
from cs50 import get_int
# Read user input
while True:
    height = get_int("Height: ")
    if height > 0 and height <= 8:
        break
# Build a half-pyramid
for i in range(height):
    for j in range(height - i - 1):
        print(" ", end="")
    for j in range(i + 1):
        print("#", end="")
    print()