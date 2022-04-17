import random as ra
def reppuOngelma(pr, p, arvot, lkm):
    #r->rivi s->sarake
    #pr+1 lkm+1
    #r,s = ((pr+1), (lkm+1))
    #t = [[0]*s]*r
    #2d taulukko
    t = [[0 for x in range(pr + 1)] for x in range(lkm + 1)] 
    #täytetään: loppu->alku
    for i in range(lkm+1):
        for j in range(pr+1):
            
            if i == 0 or j == 0: 
                t[i][j] = 0
                
            elif p[i-1] <= j:
                
                t[i][j] = max(arvot[i-1] + t[i-1][j-p [i-1]], t[i-1][j]) 
            else: 
                t[i][j] = t[i-1][j] 
   
    return t[lkm][pr] 
   
koko = 15

#arvot, joku suhdeluku   
arvot = [0] * koko
#painot, grammoina    
p = [0] * koko

#testiarvoja mielivaltaisesti    
for i in range(0,koko):
    arvot[i] = ra.randint(10,150)
    p[i] = ra.randint(30,2000)
print("Painot: ", p, "\n", "Arvot: ", arvot) 

#painoraja, vaikka 10kg
pr = 10000
#tavaroiden lkm
lkm = len(arvot) 
print("Repun hyötyarvo parhaassa konfiguraatiossa: ",reppuOngelma(pr, p, arvot, lkm)) 
