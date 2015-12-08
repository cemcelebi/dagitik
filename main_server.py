__author__ = 'cemcelebi'
import threading
import Queue
import socket
import random
import time

global CONNECT_POINT_LIST
global clients
clients={}
global UPDATE_INTERVAL
UPDATE_INTERVAL=7
class sendThread (threading.Thread):
    def __init__(self, name, cSocket, address, threadQueue, logQueue ):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.address = address
        self.lQueue = logQueue
        self.tQueue = threadQueue
    def run(self):
        exitFlag=False
        while not exitFlag:
            print("!!!!!helloWriteThread!!!!! \n")
            queue_message = self.tQueue.get(True)
            message_to_send = "CPL " + queue_message[1]+" "+str(queue_message[2])
            self.cSocket.sendall(message_to_send)


class randSend(threading.Thread):
	 def __init__(self):
            threading.Thread.__init__(self)

	 def run(self):
            global CONNECT_POINT_LIST
            print("RAND'A GIRDIN!!?!?!?!?!")
            while True:
                toSend=""
                for keys in CONNECT_POINT_LIST.keys():
                    temp =[keys]
                    toSend=toSend+str(temp[0][0])+"/"+str(temp[0][1])+" "
                message_to_send="CPL "+str(toSend)
                for key in clients:
				    if clients[key]=="Active":
                                        key.send(message_to_send)
                time.sleep(UPDATE_INTERVAL)

class recvThread (threading.Thread):
    def __init__(self, name, cSocket, address, threadQueue,logQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.address = address
        self.logQueue = logQueue
        self.CONNECT_POINT_LIST = CONNECT_POINT_LIST
        self.threadQueue = threadQueue
        self.connectorIp=""
    def parser(self,data):
         print("parser'dasin")
         if data[0:3] == "USR":
            dataSplitted=data.split("/")
            dataSplitted[0]=dataSplitted[0].strip("USR ")
            connectorIp=dataSplitted[0]
            connectorPort=dataSplitted[1]
            connector=(connectorIp,connectorPort)
            if (self.CONNECT_POINT_LIST.iterkeys()!=connectorIp):
                #CONNECT_POINT_LIST'e ekle: nickname:threadqueueN biciminden
                self.connectorIp=connectorIp
                CONNECT_POINT_LIST[connector]=self.threadQueue
                self.cSocket.send("HEL")
                #Tum CONNECT_POINT'LERI KULLANICIYA YOLLAMA:
                toSend=[]
                for key, value in CONNECT_POINT_LIST.iteritems():
                    temp = [key]
                    toSend.append(temp)
                yollanacakTuple=(connector,self.connectorIp,toSend)
                self.CONNECT_POINT_LIST[connector].put(yollanacakTuple)
                self.cSocket.send("MOK"+connector[0])
                return 0
            else:
                self.cSocket.send("REJ")
                self.cSocket.close()
                return 1
                print("USR:return -1")
            print("end of USR")
         else:
            print("ERR durumu")

    print("parser bitti")
    def run(self):
        while True:
            print("data bekliyorum")
            data=self.cSocket.recv(1024)
            print("data is "+data)
            retVal=self.parser(data)
            if retVal:
                print("retval'in icindeyim \n")
                return
"""
-*-KULLANILACAK MUTLAKA:
    data="USR 192.168.2.117/54487"
    dataSplitted=data.split("/")
    dataSplitted[0]=dataSplitted[0].strip("USR ")
    print(dataSplitted[0],dataSplitted[1])
"""
def main():
    global logLock
    global queueLock
    global CONNECT_POINT_LIST
    logQueue = Queue.Queue()
    port=60000+1
    threadCounter=0
    threads=[]
    s=socket.socket()
    host="127.0.0.1"
    s.bind((host,port))

    queueLock = threading.Lock()
    CONNECT_POINT_LIST = {}
    #while True'ya eklenecek

    s.listen(5)
    randSendd=randSend()
    randSendd.daemon=True
    randSendd.start()
    while True:
        print("connection bekleniyor \n")



        c,addr=s.accept()
        print("connection geldi \n")
        threadQueue = Queue.Queue()
        threadWrite=sendThread("WriterThread",c,addr,threadQueue,logQueue)
        threadWrite.daemon=True
        clients[c] = "Active"
        #threads.append(thread)
        #threadCounter+=1
        threadRead=recvThread("Reader Thread",c,addr,threadQueue,logQueue)
        threadRead.daemon=True


        threadRead.start()
        threadWrite.start()

        #threads.append(thread)
        #threadCounter+=1
if __name__ == '__main__':
    main()