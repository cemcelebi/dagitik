import sys
import socket
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Queue
import time

class ReadThreadd (threading.Thread):
    def __init__(self, name, cSocket, threadQueue, app, exitFlag):
        threading.Thread.__init__(self)
        self.name=name
        self.cSocket=cSocket
        self.threadQueue=threadQueue
        self.app=app
        self.exitFlag=exitFlag
    def incoming_parser(self,data):
        if len(data)>3:
            print("ilk hata if'i")
            response="ERR"
            self.cSocket.send(response)
        rest = data[4:]
        if data[0:3]=="BYE":
            print("BYE'dasin..")
            self.exitFlag=True
            print("closing server..")
            self.cSocket.close()
        if data[0:3]=="ERL":
            response="SERVER IS SAYING: REGISTER FIRST"
            self.app.cprint(response)
            return
        if data[0:3]=="HEL":
            response="SERVER IS SAYING: REGISTERED AS *_*"+data[4:]+""
            self.app.cprint(response)
            return
        if data[0:3]=="REJ":
            response="SERVER IS SAYING: gtfo server is closing"
            self.cSocket.close()
            self.app.cprint(response)
            return
        if data[0:3]=="MNO":
            response="SERVER IS SAYING: MSG FAILED!"
            self.app.cprint(response)
            return
        if data[0:3]=="MSG":
            response=rest
            self.app.cprint("CLIENT IS SAYING:"+response)
            return
        if data[0:3]=="SAY":
            response=rest
            self.app.cprint("BROADCAST MESSAGE:"+response)
            return
        if data[0:3]=="SYS":
            response=rest
            self.app.cprint("SYS:"+rest)
            return
    def run(self):
        while not self.exitFlag:
            #tum while, try/catch bloguna alinmadiginda, programi
            #ilk calistirdigimda gariplikler oluyor.
            try:
                data=self.cSocket.recv(1024)
                print("incoming:.."+data)
                self.incoming_parser(self,data)
            except:
                print("exception'lardasin")
                pass

class WriteThreadd(threading.Thread):
     def __init__(self, name, cSocket, threadQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.threadQueue = threadQueue
     def run(self):
         exitFlag=False
         while True:
             queue_message=self.threadQueue.get()
             try:
                 self.cSocket.send(queue_message)
             except:
                 print("WriteThread patlar")
                 print("WriteThread is closing server...")
                 self.cSocket.close()
                 break
             if queue_message=="QUI":
                 print("WriteThread is closing server with QUI..")
                 self.cSocket.close()
                 break

class ClientDialog(QDialog):
    ''' An example application for PyQt. Instantiate
    and call the run method to run. '''
    def __init__(self, threadQueue):
        self.threadQueue = threadQueue
        # create a Qt application --- every PyQt app needs one
        self.qt_app = QApplication(sys.argv)
        # Call the parent constructor on the current object
        QDialog.__init__(self, None)
        # Set up the window
        self.setWindowTitle('IRC Client')
        self.setMinimumSize(500, 200)
        # Add a vertical layout
        self.vbox = QVBoxLayout()
        # The sender textbox
        self.sender = QLineEdit("", self)
        # The channel region
        self.channel = QTextBrowser()
        # The send button
        self.send_button = QPushButton('&Send')
        # Connect the Go button to its callback
        self.send_button.clicked.connect(self.outgoing_parser)
        # Add the controls to the vertical layout
        self.vbox.addWidget(self.channel)
        self.vbox.addWidget(self.sender)
        self.vbox.addWidget(self.send_button)
        # A very stretchy spacer to force the button to the bottom
        # self.vbox.addStretch(100)
        # Use the vertical layout for the current window
        self.setLayout(self.vbox)
    def cprint(self, data):
        self.channel.append(data)
    def outgoing_parser(self):
        data = self.sender.text()
        if data[0]=="/":
            command=data[1:5]
            if command == "list":
                self.threadQueue.put("LSQ")
            elif command == "quit":
                self.threadQueue.put("QUI")
            elif command=="msg ":
                tete=data.split(" ")
                nickRcver=tete[1]
                msg=tete[2]
                #string casting yapilmadiginda kod patlamaktadir
                toQueue="MSG "+str(nickRcver)+":"+str(msg)
                self.threadQueue.put(toQueue)
            else:
                self.cprint("LOCAL IS SAYING: ERR")
        else:
            response=str(data)
            self.threadQueue.put(response)
        self.sender.clear()
    def run(self):
        '''Run the app and show the main form. '''
        self.show()
        self.qt_app.exec_()

def main():
    print("baglaniliyor \n")
    host = "127.0.0.1"
    port = 60000
    s = socket.socket()
    s.connect((host,port))
    threadQueue = Queue.Queue()
    app = ClientDialog(threadQueue)
    ReadThread = ReadThreadd("read thread",s,threadQueue,app,False)
    ReadThread.setDaemon(True)
    ReadThread.start()
    WriteThread = WriteThreadd("WriteThread", s, threadQueue)
    WriteThread.setDaemon(True)
    WriteThread.start()
    try:
        app.run()
    except:
        print("QT4 has crashed")
    ReadThread.join()
    WriteThread.join()
    s.close()
if __name__ == '__main__':
    main()