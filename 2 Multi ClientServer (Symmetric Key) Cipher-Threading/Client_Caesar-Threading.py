import socket
import math
import random

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 1234
# connect to the server on local computer
s.connect(('192.168.1.5', port))
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

name = input("Enter your name: ")
s.send(name.encode())

while True:
    # Take input from the client and send it to the server
    data = input("------> ")

    mes = encrypt(data,4)

    s.send(mes.encode())

    # Receive the message from the server and print it in the terminal
    msg = s.recv(1024).decode()
    
    print("-> Encrypted message:", msg)
    
    print("-> Recieved message from the server:", decrypt(msg,4))
    # s.close()
