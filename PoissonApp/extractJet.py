import re

f = open("newfile",'w')
f.write("[")

jet = open("jet.txt",'r')

jetlines = jet.readlines()

for line in jetlines:
    color = re.search('(?<=fill:).......',line).group(0)
    f.write('\''+color+'\',')

f.write(']')
f.close()

