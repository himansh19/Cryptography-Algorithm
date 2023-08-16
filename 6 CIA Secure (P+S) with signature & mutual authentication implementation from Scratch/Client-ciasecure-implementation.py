import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 8084
ADDR = (IP, PORT)
DISCONNECT_MSG = "!DISCONNECT"
pub_keyclient=(997,323);pvt_keyclient=(13,323);pub_keyserver=(997,899)
symmetrickey=4729   # client know sym key and will send to server server get diff sym key from diff client

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
    return Asym_encrypt(pvt_keyclient,str(msg_hash))  # bcz hash int value 

def main():
    client = socket.socket()
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
    # sending new symmetric key to server 
    keysend=Asym_encrypt(pub_keyserver,str(symmetrickey))
    client.send(keysend.encode())
    connected=True
    while connected:
        msg = input(">>>")
        digital_sign=signature(pvt_keyclient,msg)   # sign the msg i.e hash & encrypt with priv key
        encrypted_msg=Sym_encrypt(symmetrickey,msg)  # encrypt msg using sym key
        print('Digital Sign: ',digital_sign)  

        client.send(encrypted_msg.encode())
        client.send(digital_sign.encode())

        msg=client.recv(1024).decode()
        received_digital_sign=client.recv(1024).decode()    # verify the received sign by computing msg hash

        decrypted_msg=Sym_decrypt(symmetrickey,msg)
        print("Recieved msg: ",decrypted_msg);print('Received Sign: ',received_digital_sign)

        msg_hash=hash(decrypted_msg)  
        received_hash=Asym_decrypt(pub_keyserver,received_digital_sign)

        if msg_hash==int(received_hash):    # received hash is string
            print ("Authentictiy verified, Valid Signature")
        else:
            print ("The signature is not valid.!!!!!") 
        if msg=="DISCONNECT":
            connected=False
            client.close()
            
main()
