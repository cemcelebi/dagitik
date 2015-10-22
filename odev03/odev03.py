__author__ = 'cemcelebi'
from itertools import izip
import threading

i2=0
alfabe="abcdefghijklmnopqrstuvwxyz"
key={}
text="Okula git. Eve gel. Son."


exitFlag = 0
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        


def kaydir(l,n):
        return l[-n:] + l[:-n]

def anahtarUretici(n):
        key={}
        key=kaydir(alfabe,n)
        med = iter(key)
        retval=dict(izip(alfabe,key))
        return retval
def bolucu(text,n):
    mylist = [text[i:i+n] for i in range(0, len(text), n)]
    return mylist

l=5
myfile = open("metin.txt","r")
control = True
altmetin=[]
#control dogru oldukca 5byte 5byte okuyup subtexts'in append'ini
# kullanarak sona ekleme yap.
while control:
	chunk = myfile.read(l)
	if chunk=='':
		control=False
	else:
		altmetin.append(chunk.lower())


