# Import get_float method
from cs50 import get_float
# Ask user input
while True:
    change = get_float("Change owed: ")
    if change > 0:
        break
# Change coins list
coins = [0.25, 0.1, 0.05, 0.01]
# Coin counter
coin = 0
# Calculate change
for c in coins:
    while change >= c:
        change = round(change - c, 2)
        coin += 1
# Print result
print(coin)