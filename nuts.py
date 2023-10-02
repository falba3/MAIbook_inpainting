import sys

def nuts(number: int):
    number = int(number)
    print(number**2)

if __name__ == "__main__":
    inp = "".join(sys.argv[1:])
    # Cnuts(sys.argv)
    nuts(inp)
