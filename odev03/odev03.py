import threading
import random
import string as str
n=5
sentence = "Eve gel. Okula git. Son."
def splitter(words):

    mylist = [words[i:i+n] for i in range(0, len(words), n)]
    #mystring = ''.join(mylist)
    #mystring=mystring.upper()
    newList = []
   # while mylist:
    #    newList.append(mylist.pop(random.randrange(0, len(mylist))))
    print(mylist[1])
    return mylist
def kaydir(l,n):
    return l[-n:] + l[:-n]

def cipherMethod(mylist,kaydMiktar):
    alfabe="abcdefghijklmnopqrstuvwxyz"
    kaydAlfabe=kaydir(alfabe,kaydMiktar)


class Cipher:
    def ___init___(self):
        self.parcalar=splitter(sentence)
    def run(self):
        global queue
        while splitter(sentence):
            queue.put(cipherMethod(splitter(sentence)))

def main():

    num_threads = n
    threads = []
    splitter(sentence)
    print("Starting...\n")
    """for i in range(num_threads):
        t = threading.Thread(target=splitter, args=(sentence,))
        t.start()
        threads.append(t)
"""
    #print("Thread count: {}".format(threading.active_count()))
    print("\nExiting")

if __name__ == "__main__":
    main()
