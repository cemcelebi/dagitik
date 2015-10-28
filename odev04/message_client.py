__author__ = 'cemcelebi'
import socket               # Import socket module
import threading
import time
s = socket.socket()         # Create a socket object
class fromServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            data=s.recv(1024)
            if(data!= ""):
                print("bosluk")
            else:
                print("server'in mesaji:"+data)
                               
    

host = socket.gethostname() # Get local machine name
port = 5432                # Reserve a port for your service.
s.connect((host, port))
print("Client servisi..")
#print s.recv(1024)
threadLO=fromServer()
threadLO.start()
s.close()
