import threading
import socket
import Queue
import time

"""
CPL icin cok degisik veri tipleri dusundum. nested dict, ip/port:tuple key olacak sekilde,
veya baska bir dict olarak. C_P_L'in oyle bir verisi olsun istedim ki, ip'yi "key" olarak girdigimde,
bana port/time/type/SW dondursun istedim. ama, send(tupleX) durumu gibi hatalar almamak adina,
adi iki boyutlu liste ile devam etmeye karar verdim:
C_P_L[0][0]:ip
C_P_L[0][1]:port
C_P_L[0][2]:time
C_P_L[0][3]:type
C_P_L[0][4]:SW
bu konu uzerinde calistigimi http://github.com/cemcelebi/connection_point_list.py
isimli dosyadan gorebilirsiniz
"""

 #C_P_L critic bir veri. bir suru thread'imiz ayni anda onun uzerinde
    #degisiklik yapabileceginden, girerken mutexLock, cikarken mutexUnlock
    #yapmakta fayda var.
    #^^self.tLock.acquire()


class NegServerThread (threading.Thread):
    def __init__(self,name,CONNECTION_POINT_LIST,cSocket,tQueue,tLock):
        threading.Thread.__init__(self)
        self.name=name
        self.CONNECTION_POINT_LIST=CONNECTION_POINT_LIST
        self.cSocket=cSocket
        self.tQueue=tQueue
        self.tLock=tLock
        self.regIterator=0
    #def synChecker(self,):
    def isPresentInCPL(self,ip,port): #returns True if present,False sinon
        if(self.CONNECTION_POINT_LIST[0].__contains__(ip)==True):
            return True
        else:
            return False
    def ConnectionTester(self):
        while True:
            toGet=self.tQueue.get()
            ip=toGet[0]
            port=toGet[1]
            tSock=socket.socket()
            tSock.connect(ip,port)
            tSock.send("HELLO")
            data=tSock.recv(1024)
            tSock.send("CLOSE")
            try:
                tSock.close()
            except:
                print("THAT HAS NOT GONE WELL! couldn't close connection")
            if (data[0:5]=="SALUT P"):
                connectionType=data[6:]
                self.tLock.acquire()
                #zamani bir sekilde alip buradaki 00:00 yerine koymak gerek.
                self.CONNECTION_POINT_LIST.append([ip,port,"00:00",connectionType,"W"])
                self.tLock.release()
            if data[0:5]=="BUBYE":
                print("CLOSING ConnectionTester Thread!")
                break
        print("ConnectionTester Thread ended without EXCEPTION!")
    def NegServerParser(self,data,ip,port):
        if (data[0:5]=="SALUT"):
            self.cSocket.send("SALUT N")
            return
        if (data[0:5] == "CLOSE"):
            self.cSocket.send("BUBYE")
        if (data[0:5]=="REGME"):
            dataSplitted=data.split(":")
            dataSplitted[0]=dataSplitted[0].strip("REGME ")
            ip=dataSplitted[0]
            port=dataSplitted[1]
            self.tLock.acquire()
            nowTime=time.time()
            if(self.isPresentInCPL(ip,port)==True):
                self.cSocket.send("REGOK"+str(nowTime))
                return #aradigin ip zaten listede var, if'i terket.
            self.tLock.release()
            self.cSocket.send("REGWA") #aradigin ip listede yok, REGWA at ve HELLO prosedurunu baslat.
            toSend=(ip,port)
            self.tQueue.put(toSend)
            print("NegServerParser ending, starting ConnectionTester")
            self.ConnectionTester()
        if (data[0:5]=="GETNL"):
            nlsize=data[6:]
            cplToSend=""
            self.cSocket.send("NLIST BEGIN")
            for i in range(0,nlsize):
                for j in range(0,4):
                     cplToSend+=self.CONNECTION_POINT_LIST[i][j]
                     cplToSend+=":"
                cplToSend+="\n"
            self.cSocket.send("NLIST END")
    def run(self):
        print "Starting NegServerThread"
        while True:
            data = self.cSocket.recv(1024)
            self.serverParser(data)


def main():
    tLock=threading.Lock()
    tQueue=Queue.Queue()
    CONNECTION_POINT_LIST=[]
    host="127.0.0.1"
    port=59999
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)
    tc=1
    print("NegServerThread baslatiliyor")
    while True:
        print("connection bekleniyor..")
        c, addr=sock.accept()
        serverThread=NegServerThread("NegServerThread"+tc,CONNECTION_POINT_LIST,c,tQueue,tLock)
        serverThread.setDaemon(True)
        serverThread.start()
        tc=tc+1

if __name__ == '__main__':
    main()

