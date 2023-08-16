#client
import socket
from Crypto.Hash import SHA256
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15 
from Crypto.Cipher import PKCS1_OAEP
IP = socket.gethostbyname(socket.gethostname())
PORT = 8084
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
file1=open("client-private-key-decrypted.pem",'rb')
client_private_Key=RSA.importKey(file1.read()) 
file=open("public-key.pem",'rb')
server_public_key=RSA.importKey(file.read()) 

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #AF_INET is the Internet address family for IPv4. SOCK_STREAM is the socket type for TCP, the protocol that will be used to transport messages in the network.
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
    
    def signature(client_private_Key,msg):
        return pkcs1_15.new(client_private_Key).sign(SHA256.new(msg.encode(FORMAT)))
    symmetric_key = bytes(b'0Npdu9mWtbCHPWvu8ltF8NMpJNK8PfXvhW8vml8F94w=')
    obj = Fernet(symmetric_key)
    connected = True
    
    client.send(PKCS1_OAEP.new(server_public_key).encrypt(symmetric_key))
    while connected:
        msg = input(">")
        digital_sign=signature(client_private_Key,msg)   # sign the msg i.e hash & encrypt with priv key
        print('Digital Sign: ',digital_sign)  
        converted_msg=obj.encrypt(msg.encode(FORMAT))
        client.send(converted_msg)
        client.send(digital_sign)
        msg=client.recv(1024)
        decrypted_msg=obj.decrypt(msg)
        decoded_msg=decrypted_msg.decode(FORMAT)
        print("Recieved: ",decoded_msg)
        recieved_digital_sign=client.recv(1024)    # verify the received sign by computing msg hash
        try:
            h=SHA256.new(decrypted_msg)   # received hash
            pkcs1_15.new(server_public_key).verify(h, recieved_digital_sign)
            print ("Authentictiy verified.")
        except (ValueError, TypeError):
            print ("The signature is not valid.")
        if msg=="DISCONNECT":
            connected=False
            client.close()
main()
