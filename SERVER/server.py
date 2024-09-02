import socket
import threading 
# way of multiple threads within python
# when one peice f code is not running (e.g waiting someting like if timer is set) makes the peice of code run
# e.g.  # import time
        # print("zahra")
        # time.sleep(2)
        # print("qaisar")

# length of bytes in msg
HEADER = 64
PORT = 5050
# SERVER = "192.168.42.103"
SERVER = socket.gethostbyname(socket.gethostname())
# print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# socket.socket = make a new socket
# socket.AF_INET = (over the internet)category that picks the ipv4 addresses
# socket.STOCK_STREAM = stream/sends data through the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bounded the socket to this(ADDR) address
server.bind(ADDR)

# this function handle the (conversation) connection b/w the individual; one client and one server
def handle_client(conn, addr):
    # tells who connected
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        # waits for the msg from the client
        # convert the bytes into string using utf-8
        # then convert that into int 
        # then receive the next msg
        msg_length = conn.recv(HEADER).decode(FORMAT)
        
        # what happens here is 1st time we receive kinda blank msg
        # so blank msg cannot be directly converted to int it will show error
        # so it is checked 1st that there is a valid msg received
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr} {msg}]")
            conn.send("Msg received".encode(FORMAT))
    conn.close()

# this function distributes the connections to where it needs to go
# this start thread is always running to check to listen for new connections
def start():
    #listening for new connections
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True: # will continue to listen until turnoff or we don't want listen
        # when a new connection occurs 
        # pass that connection to handle_clients 
        # with the arguments conn, addr
        # then start the thread
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        # tells the amount of active threads
        # when 2 threads running it will show 1 
        # because start thread is already & always running
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        

print("[STARTING] server is starting...")
start()