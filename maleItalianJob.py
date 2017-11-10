filename = "italianjobfemale.txt"
corpus = ""
lst = ['CHARLIE', 'BULLY', 'LYLE', 'STEVE', 'JOHN', 'ROB', 'RICHARD', 'VALET', 'DETECTIVE', 'MAKOV', 'DRIVER']
f = open(filename, "r").readlines()
for i in range(0,len(f)):
    for name in lst:    
        if name in f[i]:
            j = i+1
            while j < len(f) and f[j] != "\n" and '(' not in f[j]:
                corpus += f[j]
                j+= 1

f2 = open("maleItalianOutput.txt", "w")
f2.write(corpus)
f2.close()
