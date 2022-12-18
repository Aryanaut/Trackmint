import pickle

f = open(r"passwords.dat", 'rb')

while True:
    try:
        print(pickle.load(f))

    except EOFError:
        break