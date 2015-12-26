"""data="REGME 192.168.2.117:54487"
dataSplitted=data.split(":")
dataSplitted[0]=dataSplitted[0].strip("REGME ")
ip=dataSplitted[0]
port=dataSplitted[1]
print(dataSplitted[0],dataSplitted[1])

CONNECT_POINT_LIST={}
connector1=("192.168.2.117",54487)
connector2=("192.168.2.3",54999)
CONNECT_POINT_LIST[connector1]="tQ1"
CONNECT_POINT_LIST[connector2]="tQ2"

toSend=""
for keys in CONNECT_POINT_LIST.keys():

    temp =[keys]
    toSend=toSend+str(temp[0][0])+":"+str(temp[0][1])+" "

message_to_send="CPL "+str(toSend)
"""
#print(message_to_send)
#print(CONNECT_POINT_LIST.keys())

ip1="192.168.2.1"
ip2="192.168.2.117"
port1="59999"
port2="60001"
time1="14:53"
time2="16:42"
type1="N"
type2="P"
status1="S"
status2="W"

dict1={}
dict2={}

l=[]
CONNECTION_POINT_LIST=[]
CONNECTION_POINT_LIST.append(l)
CONNECTION_POINT_LIST[0].append(ip1)
CONNECTION_POINT_LIST[0].append(port1)
CONNECTION_POINT_LIST[0].append(time1)
CONNECTION_POINT_LIST[0].append(type1)
CONNECTION_POINT_LIST[0].append(status1)
print(CONNECTION_POINT_LIST[0].__contains__(ip1))

"""
ip1="192.168.2.1"
ip2="192.168.2.117"
port1="59999"
port2="60001"
time1="14:53"
time2="16:42"
type1="N"
type2="P"
status1="S"

C_P_L={}
dict1={}
dict2={}
dict3={}

dict1[port1]=time1
dict2[type1]=status1

C_P_L[ip1]=dict1

#C_P_L.update(dict1)
#C_P_L.update(dict2)


print(C_P_L)"""










