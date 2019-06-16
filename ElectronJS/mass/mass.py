import sys

filename = sys.argv[1]

def masspec(massfile, location):
    print(f"Hello from Python\nFilename: {massfile}\nLocation: {location}")

if __name__=="__main__":
    print(filename)

sys.stdout.flush()