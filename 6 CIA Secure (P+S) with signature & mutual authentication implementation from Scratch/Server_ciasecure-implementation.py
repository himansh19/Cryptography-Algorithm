import socket
from _thread import *

IP = socket.gethostbyname(socket.gethostname())
PORT = 8084
ADDR = (IP, PORT)
DISCONNECT_MSG = "!DISCONNECT"

pub_keyclient=(997,323);pvt_keyserver=(733,899);pub_keyserver=(997,899)

def hash(stri):   # 6 bit hash
    inc=2;m=1
    for i in stri:
        m+=ord(i)*inc   # can use ** raise to power also
        inc+=1
    return (m%100000)+200000   # m%100000 -> always give b/w 0-5 digit num 

def Asym_encrypt(key,text):
    e,n=key
    x="";m=0
    for i in text:
        if(i==' '):
            # spc=400
            x+='*'
        else:               
            m= ord(i)
            c=(m**e)%n
            x+=chr(c)
    return x

def Asym_decrypt(key,text):
    d,n=key
    x='';m=0
    for i in text:
        if(i=='*'):
            x+=' '
        else:
            m=(ord(i)**d)%n
            c=chr(m)
            # print(c)
            x+=c
    return x

def Sym_encrypt(skey,text):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if(char.isspace()):
            # spc=400
            result+='*'
        elif (char.isupper()):
            result += chr((ord(char) + skey - 65) % 26 + 65)
        else:
            result += chr((ord(char) + skey - 97) % 26 + 97)

    return result

def Sym_decrypt(skey,text):
    skey = 26 - skey
    result = ""
    for i in range(len(text)):
        char = text[i]
        if(char=='*'):
            # spc=400
            result+=' '
        elif char.isupper():
            result += chr((ord(char) + skey - 65) % 26 + 65)
        else:
            result += chr((ord(char) + skey - 97) % 26 + 97)

    return result

def signature(client_privkey,msg):
    msg_hash=hash(msg)
    return Asym_encrypt(pvt_keyserver,str(msg_hash))  # bcz hash int value 

# symmetric key send by client 
def handle_client(conn, addr): 
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    encrypted_symmetric_key=conn.recv(1024).decode()    # skey send by each client diff decrypt that
    
    symmetric_key=int(Asym_decrypt(pvt_keyserver,encrypted_symmetric_key))
    
    while connected:
        msg=conn.recv(1024).decode()
        received_digital_sign=conn.recv(1024).decode()   # verify received hash 

        decrypted_msg=Sym_decrypt(symmetric_key,msg)
        print("Recieved: ",decrypted_msg);print('Received Sign: ',received_digital_sign)

        msg_hash=hash(decrypted_msg)
        received_hash=Asym_decrypt(pub_keyclient,received_digital_sign)

        if msg_hash==int(received_hash):
            print ("Authentictiy verified, Valid Signature")
        else:
            print ("The signature is not valid.!!!!!") 
        
        # server will send msg
        msg = input(">")
        digital_sign=signature(pvt_keyserver,msg)
        encrypted_msg=Sym_encrypt(symmetric_key,msg)
        print('Digital Sign: ',digital_sign)

        conn.send(encrypted_msg.encode())
        conn.send(digital_sign.encode()) 
    conn.close()

def main():
    Threadcnt=0
    print("[STARTING] Server is starting...")
    server = socket.socket()
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    while True:
        conn,addr = server.accept()
        start_new_thread(handle_client, (conn, addr,))   # to make it tuppleh
        print('ThreadCount: ',Threadcnt+1)
main()