filename = "italianjob.txt"
corpus = ""
f = open(filename, "r").readlines()
for i in range(0,len(f)):
    if 'CHRISTINA' in f[i] or 'KAREN' in f[i] or 'STELLA' in f[i]:
        j = i+1
        while j < len(f) and f[j] != "\n":
            corpus += f[j]
            j+= 1

f2 = open("femaleItalianOutput.txt", "w")
f2.write(corpus)
f2.close()
