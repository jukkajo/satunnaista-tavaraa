import sys
import random
import string
import timeit

mjono1 = ""
mjono2 = ""
#ascii:ta ja numeroita
for i in range(50):
    mjono1=mjono1 + random.choice(string.ascii_letters + string.digits)
    mjono2=mjono2 + random.choice(string.ascii_letters + string.digits)
    
print("Jonot, joita vertaillaan:\n", mjono1, "\n", mjono2)

#pass = setup details
# vakio -> timer
#timeit(koodi/exc_time, pass, timer, numero)

iteraatiot = 1
raja = 1000000
#aikasama, aikaeri, iteraatiot
#:float    :float   :int -> dec-integer->d
listaus_formaatti = "{:1.1f} {:1.1f} {:1d}"
#tänne laitetaan mjonot myöhemmin
testattava = """
if "{:50.50s}" == "{:50.50s}":
   pass
else:
   pass
"""

def vertailu(testattava,iteraatiot,raja):
    
    while iteraatiot < raja: 
        #vertaillaan samaa jonoa
        vert1tulos = timeit.timeit(testattava.format(mjono1,mjono1),number=iteraatiot)
        #vertailleen epäidenttisiä jonoja"
        vert2tulos = timeit.timeit(testattava.format(mjono1,mjono2),number=iteraatiot)
        iteraatiot += 5000
        print(listaus_formaatti.format(vert1tulos, vert2tulos, iteraatiot))

print("VrtTulos(M-jonot yhtäsuuret):  VrtTulos(M-jonot erisuuret):   Iteraatiot:")
vertailu(testattava,iteraatiot,raja)
