__author__ = 'cemcelebi'
import socket               # Import socket module
import threading
threadCounter=0
class myThread (threading.Thread):
    def __init__(self, threadCounter, clientSocket, clientAddr):
        threading.Thread.__init__(self)
        self.threadCounter = threadCounter
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
    def run(self):
        print "Starting Thread-" + str(self.threadCounter)

        print "Ending Thread-" + str(self.threadCounter)



s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 5432               # Reserve a port for your service.
s.bind((host, port))
threads=[]
print(host)
# Bind to the port
print("basladi")
#s.listen(5)                 # Now wait for client connection.
while True:
    s.listen(5)
    c, addr=s.accept()
    threadLO=myThread(threadCounter,c,addr)
    threadLO.start()
   # c, addr = s.accept()     # Establish connection with client.
    threads.append(threadLO)
    threading._sleep(0.00001)
    print 'Got connection from', threadLO.clientAddr
    c.send('Thank you for connecting')
    threadCounter=threadCounter+1

threadLO.close()                # Close the connection
