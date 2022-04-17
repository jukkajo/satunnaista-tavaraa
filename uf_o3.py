import random


#ei kai toimi tim-konsolissa tämä
#perusjoukko = ["\033[93mbanaani\033[0m", "\033[92mluumu\033[0m", "\033[92momena\033[0m", "\033[91mpersikka\033[0m", "\033[#93msitruuna\033[0m"]

perusjoukko = ["Banaani", "Luumu", "Omena", "Persikka", "Sitruuna"]

class varit:
    KE = '\033[93m'
    LI = '\033[95m'
    VI = '\033[92m'
    PE = '\033[91m'
    FONTTI = '\033[96m'
    
    VAK = '\033[0m'

print(varit.FONTTI + "Perusjoukkomme:" + varit.VAK)
print(*perusjoukko)

#======puun luonti=========
lkm = len(perusjoukko)+1
puu = [0]*(lkm)

for i in range(1,lkm):
    puu[i] = -1
#=========================
print(varit.FONTTI + "puu:" + varit.VAK)
print(*puu)   
#perusjoukolle mielivaltaiset yhdisteet
solmu1 = ""
solmu2 = ""

def etsiIndeksi(lkm, etsitty_alkio):
    if etsitty_alkio is None or len(etsitty_alkio) == 0:
        return 0
    for i in range(lkm):
        if perusjoukko[i] == etsitty_alkio:
            return i + 1
    return 0

def etsi(puu, etsitty_alkio):
    lkm = len(puu)-1
    if puu is None or len(puu) == 0:
        return 0
    indeksi = etsiIndeksi(lkm, etsitty_alkio)
    sailo = indeksi
    while puu[sailo] > 0:
        sailo = puu[sailo]
    while puu[indeksi] > 0:
        sailo2 = indeksi
        indeksi = puu[indeksi]
        puu[sailo2] = sailo
    return sailo
    

def union(puu, a, b):
    if puu is None or len(puu) == 0:
        return
    sailo = puu[a] + puu[b]
    if puu[a] <= puu[b]:
        puu[a] = sailo
        puu[b] = a
    else:
        puu[b] = sailo
        puu[a] = b
        

def yhdiste(puu, str1, str2):
    a = etsi(puu, str1)
    b = etsi(puu, str2)
    if(a == b):
        print(varit.FONTTI + "Ei yhdistettä/unioni, syy: sama puu" + varit.VAK)
        return
    union(puu, a, b)

paikka2T = 0
for i in range(lkm):
    paikkaT = random.randint(0,lkm-2)
    while paikkaT == paikka2T:
        paikka2T = random.randint(0,lkm-2)
        
    alkio1 = perusjoukko[paikkaT]
    alkio2 = perusjoukko[paikka2T]
    print("Alkioiden ", alkio1, " ja ", alkio2, " yhdiste (paikat: ", (paikkaT+1), " ", (paikka2T+1),"):" )
    yhdiste(puu, alkio1, alkio2)
    print(*puu)
