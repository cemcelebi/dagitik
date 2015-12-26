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
    def peerConnectionTester(self):
        while True:
            toGet=self.tQueue.get()
            ip=toGet[0]
            port=toGet[1]
            tSock=socket.socket()
            tSock.connect(ip,port)
            tSock.send("HELLO")
            data=tSock(1024)
            tSock.send("CLOSE")
            try:
                tSock.close()
            except:
                print("THAT HAS NOT GONE WELL!")
            if data[0:5]=="SALUT"
                connectionType=data[6:]
                self.tLock.acquire()
                self.CONNECTION_POINT_LIST.append([ip,port,"00:00",connectionType,"W"])
                self.tLock.release()
            if data[0:5]=="BUBYE":
                print("CLOSING peerConnectionTester Thread!")
                break
        print("peerConnectionTester Thread ended without EXCEPTION!")
    def NegServerParser(self,data,ip,port):
        if (data[0:5]=="HELLO"):
            self.cSocket.send("SALUT")
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
            print("NegServerParser ending, starting peerConnectionTester")
            self.peerConnectionTester()
        if (data[0:5]=="GETNL"):
            nlsize=data[6:]
            self.tQueue.put("NLIST BEGIN")









