#include <stdio.h>
#include <string>
#include <sstream>
#include <iostream>
using namespace std;


bool testaa(const string jono) {
   for(char const merkki : jono) {
      if(isdigit(merkki) == 0) { return false; }
   }
   return true;
}

void keoksi(int ta[], int n, int i) {
   int juuri = i;
   int vasen_l = 2 * i + 1;
   int oikea_l = 2 * i + 2;
   
   if(vasen_l < n && ta[vasen_l] > ta[juuri]) {
      juuri = vasen_l;
   }
   if(oikea_l < n && ta[oikea_l] > ta[juuri]) {
      juuri = oikea_l;
   }
   if(juuri != i) {
     /* int sailo = ta[i];
      ta[i] = ta[juuri];
      ta[juuri] = sailo; */
     swap(ta[i], ta[juuri]);
     keoksi(ta, n, juuri);
   }
}

void tulostaOutput(int ta[], int pituus) {
   cout << "Kekolajiteltuna:\n";
   for(int i = 0; i < pituus; i++) {
      cout << ta[i] << " ";
   }
}

void kekolajittelu(int ta[], int lkm2) {

   int pituus, n;
   /*
   int alkup = sizeof(ta)/sizeof(ta[0]);
   for(int i = 0; i < alkup; i++) {

      if(ta[i] != 0) {
         pituus += 1;
      }
   }
   */
   pituus = lkm2;
   int uusi[pituus];

   for(int i = 0; i < pituus; i++) {
      uusi[i] = ta[i];
   }
   n = sizeof(uusi) / sizeof(uusi[0]);
   
   for(int i = n / 2 - 1; i >= 0; i--) {
      keoksi(uusi, n, i);
   }
   
   for(int i = n - 1; i > 0; i--) {
     /* int sailo = ta[0];
      ta[0] = ta[i];
      ta[i] = sailo; */
      swap(uusi[0], uusi[i]);
      keoksi(uusi, i, 0);
   }
   tulostaOutput(uusi, pituus);
}

int main(int argc, char **argv) {
  
  cout << "Syötä kokonaislukuja ohjelmalle, vähintään 8, enintään 40. Anna mahd. nollat (0), ennen lukua 8. Kun olet valmis, syötä: seis\n";
  string syote, seis;
  seis = "seis";
  int lkm = 0;
  int lkm2 = 0;
  int ta[40];
  while(lkm < 40) {
    stringstream ss;
    string tmp;
    ss << lkm + 1;
    ss >> tmp;
    ss.str("");
    cout << "Syötä luku " + tmp + ": ";
    char temppi[10];
    scanf("%9s", temppi);
    syote = temppi;
    
    if(syote == seis) {
       if(lkm < 9) { cout << "Ei tarpeeksi lukuja\n"; }
       else { 
       lkm2=lkm;
       lkm=40;       
       }
    }
    
    if(testaa(syote) == true) {
       ta[lkm] = stoi(syote);
    }
    //t[lkm] = stoi(seis);
    lkm += 1;
    
  }
  
  kekolajittelu(ta, lkm2);
  
  
}
