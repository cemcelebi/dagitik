__author__ = 'cemcelebi'
import socket               # Import socket module
import threading
import random
import time
threadCounter=0
clients=[]

class myThread (threading.Thread):
    def __init__(self, threadCounter, clientSocket, clientAddr):
        threading.Thread.__init__(self)
        self.threadCounter = threadCounter
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
    def run(self):
        print "Starting Thread-" + str(self.threadCounter)
        #c.send("Peki from:" + str(self.clientAddr))
        myControl=False
        while myControl!=True:
            data = c.recv(1024)
            if data=="exiting client":
                myControl=True#cikis_yap
                print("client cikmak istedi, kendi bilir..")
            else:
                c.send("Peki from:" + str(self.clientAddr))
                #c.recv(1024)
                #for key in threads:
                    #if threads==:
                c.send("Merhaba, su an saat "+time.strftime("%H:%M:%S"))
                time.sleep(random.randrange(2,3))
        print "Ending Thread-" + str(self.threadCounter)



s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 5432               # Reserve a port for your service.
s.bind((host, port))
threads={} #dict of active threads,

print(host)
# Bind to the port
print("basladi")
#s.listen(5)                 # Now wait for client connection.
while True:
    s.listen(5)
    c, addr=s.accept()
    threadLO=myThread(threadCounter,c,addr)
    threadLO.start()
    #threads.append(threadLO)
    threading._sleep(0.00001)
    print ('Got connection from', threadLO.clientAddr)
    c.send('Thank you for connecting')
    threads[threadCounter]=threadLO
    threads[c]="Actif"
    threadCounter=threadCounter+1
    print("arr:",threads)

threadLO.close()                # Close the connection
