# first of all import the socket library
import socket

# next create a socket object
s = socket.socket()  # socket create krr rhayay hain
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 8082

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print("socket binded to %s" % (port))

# put the socket into listening mode


def decrypt(text, s):
    s = 26 - s
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


# a forever loop until we interrupt it or
# an error occurs
s.listen(1)
print("socket is listening")

c, addr = s.accept()  # accept() returns a tuple
print('Got connection from', addr)
while True:
    # Establish connection with client.

    # ---------------------------------------------------------------------------------------------------------------------
    # Message recieved from the client and prints in the terminal
    msg = c.recv(1024)

    print("Crypted:", msg.decode())
    print('Recieved Message from the client:', decrypt(msg.decode(), 4))

    # sends the message to the client
    str = "I am a server"
    c.send(str.encode())
    # break
