__author__ = 'cemcelebi'
import socket               # Import socket module
import threading
import time

sock = socket.socket()         # Create a socket object
class fromServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):

        while True:
            data=sock.recv(1024)
            if(data!= ""):
                print("bosluk")
            else:
                print ("Server says: \""+data+"\"")

host = socket.gethostname() # Get local machine name
port = 5432                # Reserve a port for your service.
sock.connect((host, port))
print("Client servisi..")
#print s.recv(1024)
threadLO=fromServer()
#bu satiri oguz eroglu'ndan aldim. cok garip bir sekilde,
#bu satir olmadan "bad file descriptor" hatasi aliyorum.
threadLO.setDaemon(True)
threadLO.start()
sock.send("exiting client")
sock.close()
