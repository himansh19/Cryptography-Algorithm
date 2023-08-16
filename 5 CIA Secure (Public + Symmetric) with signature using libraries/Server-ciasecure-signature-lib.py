import socket
import threading
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
file1=open("private-key-decrypted.pem",'rb')
server_private_Key=RSA.importKey(file1.read())
file=open("client-public-key.pem",'rb')
client_public_key=RSA.importKey(file.read()) 
# symmetric key send by client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    def signature(client_private_Key,msg):
        return pkcs1_15.new(server_private_Key).sign(SHA256.new(msg.encode(FORMAT))) 
    connected = True
    encrypted_symmetric_key=conn.recv(1024)    # skey send by each client diff decrypt that
    symmetric_key=PKCS1_OAEP.new(server_private_Key).decrypt(encrypted_symmetric_key)
    obj = Fernet(symmetric_key)   
    while connected:
        msg=conn.recv(1024)
        decrypted_msg=obj.decrypt(msg)
        decoded_msg=decrypted_msg.decode(FORMAT)
        print("Recieved: ",decoded_msg)
        recieved_digital_sign=conn.recv(1024)   # verify received hash 
        try:
            h=SHA256.new(decrypted_msg)
            pkcs1_15.new(client_public_key).verify(h, recieved_digital_sign)
            print ("Authentictiy verified.")
        except (ValueError, TypeError):
            print ("The signature is not valid.") 
        msg = input(">")
        digital_sign=signature(server_private_Key,msg)
        print('Digital Sign: ',digital_sign)
        converted_msg=obj.encrypt(msg.encode(FORMAT))
        conn.send(converted_msg)
        conn.send(digital_sign) 
    
    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

main()