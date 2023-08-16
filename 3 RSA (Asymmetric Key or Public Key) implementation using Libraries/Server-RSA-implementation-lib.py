import socket
import threading
import wikipedia
import rsa

IP = socket.gethostbyname(socket.gethostname())
# 172.16.176.63:8085
PORT = 8085
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    privateKey = rsa.key.PrivateKey(8406422488038002834466942761566961071670485821351708215994036290962078623891582923624499222758629182472408657133426472724325163911173134187091483147187109, 65537, 6229041440165120369369725107759201116353542769069100727605816414570402397045105535749118794765585421758339545049756187291811096556743626809721836771324673, 4906675350221644148299681076700185110359795643211573152744685571514734815366349509, 1713262420685376758097574669793154917348026014810503314284136660028226401)

    client_key = rsa.key.PublicKey(9412330705965798665703097813066132790768966303411944846590440880658861990524651348476803393127126249346611522575737397964449653428653292192160655383534563, 65537)

    connected = True
    while connected:
        msg = conn.recv(SIZE)
        msg1 = rsa.decrypt(msg, privateKey).decode(FORMAT)
        if msg1 == DISCONNECT_MSG:
            connected = False

        print(f"[{addr}] {msg1}")
        print(msg)
        # msg = f"Msg received: {msg}"
        #msg = wikipedia.summary(msg, sentences=1)
        data = input("Enter message = ")
        data1 = rsa.encrypt(data.encode(FORMAT), client_key)
        conn.send(data1)

    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


main()