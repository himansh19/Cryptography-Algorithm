# Import socket module
from email import message
import socket

# Create a socket object
s = socket.socket()
# Define the port on which you want to connect
port = 8082
# connect to the server on local computer
s.connect(('192.168.1.5', port))

# -----------------------------------------------------------------------------------------------------------------------

def encrypt(text, s):
    result = ""
    # traverse text
    for i in range(len(text)):
        char = text[i]
        # Encrypt uppercase characters
        if (char.isupper()):
            result += chr((ord(char) + s - 65) % 26 + 65)
        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)

    return result

while True:
    # Take input from the client and send it to the server
    data = input()
    mes = encrypt(data, 4)
    s.send(mes.encode())
    # Recieve the message from the server and print it in the terminal
    msg = s.recv(1024)
    print("Recieved message from the server:", msg.decode())
    # s.close()
