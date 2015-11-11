__author__ = 'cemcelebi'
import threading
import Queue
import socket
class WriteThread (threading.Thread):
    def __init__(self, name, cSocket, address, threadQueue, logQueue ):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.address = address
        self.lQueue = logQueue
        self.tQueue = threadQueue
def run(self):
    #logQueue
    exitFlag=False
    while not exitFlag:
        #olmayan seyi gondermemizi engellemis olacak:
        if self.threadQueue.qsize()>0:
            queue_message = self.tQueue.get()
            # gonderilen ozel mesajsa
            if queue_message[2]=="MSG":
                message_to_send = "MSG " + queue_message[1]+" "+queue_message[3]
            # genel mesajsa
            elif queue_message[2]=="SAY":
                message_to_send = "SAY "+queue_message[1]+" "+queue_message[3]
            # hicbiri degilse sistem mesajidir
            elif queue_message[2]=="QUI":
                break
            else:
                message_to_send = "SYS "+queue_message[3]
            self.cSocket.sendall(message_to_send)
        """
                mesaj yollama
        """
class ReadThread (threading.Thread):
    def __init__(self, name, cSocket, address, logQueue,threadQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.address = address
        self.logQueue = logQueue
        self.fihrist = fihrist
        self.threadQueue = threadQueue
        self.nickname=""
    def parser(self,data):
        print("parser'dasin")
        data = data.strip()
        # henuz login olmadiysa
        if not self.nickname and not data[0:3] == "USR":
            self.cSocket.send("ERL")
        if data[0:3] == "USR":
            nickname=data[4:]
            #bundan sonra ikiye dallanacak,
            #ilkinde kullanicinin fihriste eklenmesi
            #ikincide de reject edilmesi
            if (self.fihrist.iterkeys()!=nickname):
                #fihrist'e ekle: nickname:threadqueueN biciminden
                self.nickname=nickname
                fihrist[nickname]=self.threadQueue
                self.cSocket.send("HEL")
                return 0
            else:
                self.cSocket.send("REJ")
                self.cSocket.close()
                return 1
                print("USR:return -1")
        elif data[0:3] == "QUI":
            self.cSocket.send("BYE"+self.nickname)
            #fihristten sil
            del self.fihrist[self.nickname]
            self.cSocket.close()
            return 1
        elif data[0:3] == "LSQ":
            self.cSocket.send("LSA")
            for key, value in self.fihrist.iteritems():
                self.cSocket.send(key)
                print(":")
            return 0
        elif data[0:3] == "TIC":
            self.cSocket.send("TOC")
            return 0
        elif data[0:3] == "SAY":
             sayMessage="SAYING: SOK"
             #buradan direkt send'lemiyoruz, threadQueue'ya ekliyoruz:
             self.threadQueue.put((None,None,sayMessage))
             sayMessage=data[4:]
             print sayMessage
             #threadQueue'nun put methodu'yla tum fihrist'i dolasip hepsine sayMessag'i iletmek:
             for key in self.fihrist.keys():
                self.fihrist[key].put((None,self.nickname,sayMessage))
             return 0
        elif data[0:3] == "MSG":
            rawData = data[4:].split(':')
            nicknameRcver=rawData[0]
            msgMessage=rawData[1]
            #once nickRcver'in olmadigi durum, sonra oldugu:
            if nicknameRcver not in self.fihrist.keys():
                self.cSocket.send("MNO"+nicknameRcver)
            else:
                yollanacakTuple=(nicknameRcver,self.nickname,msgMessage)
                self.fihrist[nicknameRcver].put(yollanacakTuple)
                self.cSocket.send("MOK"+nicknameRcver)
                return 0
        else:
            #ornek parser kodunda ERR case'inin en basta olmasi sacma
            # cunku ERR case'i zaten hicbiri olmazsa durumu.
            # bundan dolayi ERR en sonda olmali
            print("ERR durumu")
            self.cSocket.send("ERR")
            return 0
    def run(self):
        while True:
            print("data bekliyorum")
            data=self.cSocket.recv(1024)
            print("data is"+data)
            retVal=self.parser(data)
            if retVal:
                return
            return 0
def main():
    global logLock
    global queueLock
    global fihrist
    logQueue = Queue.Queue()
    port=59998
    threadCounter=0
    threads=[]
    s=socket.socket()
    host="127.0.0.1"
    s.bind((host,port))
    
    queueLock = threading.Lock()
    fihrist = {}
    #while True'ya eklenecek
    threadQueue = Queue.Queue()
    s.listen(5)
    while True:
        print("connection bekleniyor")
        c,addr=s.accept()
        print("connection geldi")
        thread=WriteThread("WriterThread",c,addr,threadQueue,logQueue)
        thread.daemon=True
        thread.start()
        threads.append(thread)
        threadCounter+=1
        thread=ReadThread("Reader Thread",c,addr,threadQueue,logQueue)
        thread.daemon=True
        thread.start()
        threads.append(thread)
        threadCounter+=1
if __name__ == '__main__':
    main()
