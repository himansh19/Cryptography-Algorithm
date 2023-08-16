import socket
import math
import random
import threading
from _thread import *

# create a socket object
s = socket.socket()  # socket created
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 1234

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))

# put the socket into listening mode
s.listen(1)
print("Waiting for Connections")

ThreadCount = 0

def encrypt(text, s):
    result = ""

    # traverse text
    for i in range(len(text)):
        char = text[i]

        # Encrypt uppercase characters
        if char.isspace():
            result+='*'
        elif (char.isupper()):
            result += chr((ord(char) + s - 65) % 26 + 65)

        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)

    return result

def decrypt(text, s):
    s = 26 - s
    result = ""

    # traverse text
    for i in range(len(text)):
        char = text[i]

        # Encrypt uppercase characters
        if char=='*':
            result+=' '
        elif char.isupper():
            result += chr((ord(char) + s - 65) % 26 + 65)

        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)

    return result

def multithreaded_client(c, addr, name):
    # sends the message to the client
    while True:
        # Establish connection with client.
        # ---------------------------------------------------------------------------------------------------------------------
        # Message recieved from the client and prints in the terminal
        msg = c.recv(1024).decode()

        print("-> Encrypted message:", msg)
        
        print(f'-> Received Message from {name.decode()}:', decrypt(msg,4))
        str = input(f"Reply to {name.decode()}: ")
        str1=encrypt(str,4)
        
        c.send(str1.encode())


while True:
    c, addr = s.accept()  # accept() returns a tuple

    name = c.recv(1024)

    print('Got connected with', addr, name.decode())


    # a = start_new_thread(multithreaded_client, (c, addr,))
    t1 = threading.Thread(target=multithreaded_client, args=(c, addr, name))
    t1.start()
    
    print('Thread Count: ' + str(threading.active_count()))
    ThreadCount += 1
