__author__ = 'cemcelebi'
import socket               # Import socket module
import threading
import time
global sock
sock = socket.socket()         # Create a socket object
class fromServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global sock
        while True:
            data=sock.
            if(data!= ""):
                print("bosluk")
            else:
                print ("Server diyor ki \""+data+"\"")

host = socket.gethostname() # Get local machine name
port = 5432                # Reserve a port for your service.
sock.connect((host, port))
print("Client servisi..")
#print s.recv(1024)
threadLO=fromServer()
threadLO.start()
sock.send("exiting client")
sock.close()
