# Single Client
import socket
import sys


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999 # uncommon port no.
        s = socket.socket() # checking whether the socket is created or not

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding (connecting port and host) the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5) # 5 is no of bad connection allowed

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Establish connection with a client (socket must be listening)
def socket_accept():
    conn, address = s.accept() # s.accept() is returning two parts where, conn is connection (object) and address(list) can be ip address or port 
    print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
    send_commands(conn)
    conn.close()

# Send commands to client
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit': # to close the connection
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024),"utf-8")  # 1024 is chunk size
            print(client_response, end="") # to move cursor to next line 


def main():
    create_socket()
    bind_socket()
    socket_accept()

# calling main function
main()







