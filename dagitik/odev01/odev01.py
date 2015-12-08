__author__ = 'cemcelebi'
import numpy as np
import matplotlib.pyplot as plt

plt.switch_backend('MacOSX')
cift1 = [-5, 1.5]
cift2 = [0, 1.5]

list1 = []
list2 = []
histo1 = [0.0 for u in range(40)]
histo2 = [0.0 for u in range(40)]
histoo1= [0.0 for u in range(40)]
histoo2= [0.0 for u in range(40)]
# indekslerimiz:
tit = [i for i in range(-20, 20)]
#randomlari atayacaklarimiz+
list1 = np.random.normal(cift1[0], cift1[1], 10000)
list2 = np.random.normal(cift2[0], cift2[1], 10000)

for x in range(0, 9999):
    #+20 negatif degerler ve -20/20 arasinda ortalamak icin
    histo1[int(round(list1[x])) + 20] = histo1[int(round(list1[x])) + 20] + 1
    histo2[int(round(list2[x])) + 20] = histo2[int(round(list2[x])) + 20] + 1
flag=0
for x in range(0, 39):
    float(histo1[x])
    histo1[x] = histo1[x] / 10000
    if flag==0 :
        if histo1[x]!=0.0:
            histo1_ilk_histo=x
            flag=1
flag=0
for x in range(0, 39):
    float(histo1[x])
    histo2[x] = histo2[x] / 10000
    if flag==0 :
        if histo2[x]!=0:
             histo2_ilk_histo=x
             flag=1


#her indekse dusen degeri console'da gormek icin
#print(tit)
print(histo1)
print(histo2)

for x in range(0, 39):
    histoo1[x]=histo1[x]
    histoo2[x]=histo2[x]



#wasserstein
i=0
j=0
wasss=0.0
#ilk histogramlar arasindaki mesafe hesaplanmasi:
#print(histo1_ilk_histo)
#print(histo2_ilk_histo)
d=abs(abs(histo1_ilk_histo)-abs(histo2_ilk_histo))
print(d)
wass1=0.0#her dongude hesaplanacak ve sonunda buyuk sonuc olan wasss degiskenine atanacak degiskenler
wass2=0.0
wass3=0.0
while 1:   #while i<39 or j<39 : syntax'i calismiyor.
    if (histo1[i] == histo2[j]):  #eger bu durumsa iki histo degeri esittir
        histo2[j] = 0
        histo1[i] = 0
        i = i + 1
        j = j + 1
        wass1=histo1[i]*d
    if (histo1[i] < histo2[j]):   #eger bu durumsa histo2 nin degeri histo1den buyuktur
        histo2[j] = histo2[j] - histo1[i]
        histo1[i]=0
        i = i + 1
        wass2=histo2[j]*d
        d=d-1 # her dongu sonrasi d'nin update edilmesi kritik!
    if (histo1[i] > histo2[j]): #eger bu durumsa histo1in degeri histo2 den buyuktur
        histo1[j] = histo1[j] - histo2[i]
        histo2[j]=0
        j = j + 1
        wass3=histo1[i]*d
        d=d+1

    wasss=wass1+wass2+wass3 #son sonucun hesaplanmasi
    if i > 39 or j > 39:
        break



print('wasserstein metric:',wasss)

#graf cizimiyle alakali
plt.bar(tit, histoo1, width=1, color='Blue')
plt.bar(tit, histoo2, width=1, color='Red')
plt.axis([-20, 20, -0.3, 0.3])
plt.title("Odev1-Histogramlar")
plt.xlabel("Index")
plt.ylabel("Frequency")
plt.show()
