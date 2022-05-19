      	.text
        .globl  useimmiten
useimmiten:
        #-----Pinokehyksen synty------------
        pushq   %rbp #aiempi kanta pinon paalle
        movq    %rsp, %rbp #uuden kannan kiinnitys
        subq    $1072, %rsp #varataan tarvittava tila
        movq    %rdi, -1064(%rbp) #param1 osoite
        movl    %esi, -1068(%rbp) #param2 osoite
        #----Varsinainen ohjelma------------
        #======taulukon alustus alku=======
        movq    %fs:40, %rax
        movq    %rax, -8(%rbp)
        xorl    %eax, %eax
        leaq    -1040(%rbp), %rdx
        #----------------------------------
        movq    $0, %rax #indeksi
nollaus:
        movl    $0, -1040(%rbp,%rax,4) # nolla taulukkoon indeksin kohdalle
        addq    $1, %rax               # indeksi += 1
        cmpq    $256, %rax             # jos pienempi kuin taul.pituus, jatketaan
        jl      nollaus                # alkuun
        #======taulukon alustus loppu=======
        jmp     .while_ehto
.while_sisalto:
        movl    -1044(%rbp), %eax
        cltq    		#eax -> 64 bittiin
        movl    -1040(%rbp,%rax,4), %eax #muistista eax:siin
        leal    1(%rax), %edx #kasvatus
        movl    -1044(%rbp), %eax
        cltq
        movl    %edx, -1040(%rbp,%rax,4)
.while_ehto:
        movq    -1064(%rbp), %rax
        movq    %rax, %rdi
        call    fgetc
        movl    %eax, -1044(%rbp) #paluuarvo sailoon
        movl    -1044(%rbp), %eax
        cmpl    -1068(%rbp), %eax #dest, src
        jne     .while_sisalto #jos erisuuri, niin uutta looppia
        movl    -1040(%rbp), %eax
        movl    %eax, -1052(%rbp)

        movl    $0, -1048(%rbp) #indeksi, joka palautetaan=> rax tai eax
        movl    $0, -1056(%rbp) #for-loopin i
        jmp     .for

.if:
        movl    -1056(%rbp), %eax #i eaxiin
        cltq   			  #eax -> 64 bittiin
        movl    -1040(%rbp,%rax,4), %eax #alkio eaxiin
        cmpl    %eax, -1052(%rbp)  #vertailu
        jge     .iplusplus #jos suurempi kuin ed. suurin
        movl    -1056(%rbp), %eax
        cltq
        movl    -1040(%rbp,%rax,4), %eax
        movl    %eax, -1052(%rbp)
        movl    -1056(%rbp), %eax
	movl	%eax, -1048(%rbp)
.iplusplus:
        addl    $1, -1056(%rbp) #kasvatetaan iteraattorin arvoa
.for:
        cmpl    $253, -1056(%rbp)
        jle     .if #jos pienempi, niin jump
        movl    -1048(%rbp), %eax #indeksi paluuarvoksi
        movq    -8(%rbp), %rdx
        subq    %fs:40, %rdx
        je      .break #jos i == taulukon pituus
	#-------------pinokehyksen tuho-------------------
.break:
        leave #kehyksen purku
        ret #palataan main:iin
	
