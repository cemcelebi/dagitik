import threading
import random
import string as str
n=5
def splitter(words):

    mylist = [words[i:i+n] for i in range(0, len(words), n)]
    mystring = ''.join(mylist)
    mystring=mystring.upper()

    newList = []
   # while mylist:
    #    newList.append(mylist.pop(random.randrange(0, len(mylist))))
    print(mystring)
    return mystring
#def cipher(mystring):





def main():
    sentence = "Eve gel. Okula git. Son."
    num_threads = n
    threads = []
    splitter(sentence)
    print("Starting...\n")
    """for i in range(num_threads):
        t = threading.Thread(target=cipher, args=(sentence,))
        t.start()
        threads.append(t)
"""
    #print("Thread count: {}".format(threading.active_count()))
    print("\nExiting")

if __name__ == "__main__":
    main()
