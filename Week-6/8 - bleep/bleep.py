from cs50 import get_string
from sys import argv, exit


def main():
    # Check exactly one user argument
    if len(argv) != 2:
        print("Usage: python bleep.py dictionary")
        exit(1)
    # Ask message to be censored
    message = get_string("What message would you like to censor?\n")
    # Open dictionary of banned words
    file = open(argv[1], "r")
    lines = file.read().splitlines()
    # Split message
    tokens = message.split(" ")
    result = ""
    # Iterate through words of user message
    for token in tokens:
        is_censored = False
        for line in lines:
             # Iterate through banned words
            if token.lower() == line.lower():
                result += censor(token) + " "
                is_censored = True
                break
        if not is_censored:
            result += token + " "
    print(result.strip(" "))


# Build censored word
def censor(word):
    censored = ""
    for c in word:
        censored += "*"
    return censored


if __name__ == "__main__":
    main()