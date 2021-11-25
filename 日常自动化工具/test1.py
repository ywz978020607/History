import csv

csv1=open('1.csv','r')
reader1=csv.reader(csv1)
dd={}
ii = 0
for line in reader1:
    if ii == 0:
        ii+=1
        continue
    else:
        dd[line[0]] = (float)(line[3])
csv1.close()


csv2=open('2.csv','r',encoding='utf-8')
reader2=csv.reader(csv2)
for line in reader2:
    if line[0] in dd.keys():
        dd[line[0]] += (float)(line[1])
    else:
        dd[line[0]] = (float)(line[1])
csv2.close()

out = open('out.csv','w',encoding='utf-8')
writer=csv.writer(out)
for (a,b) in dd.items():
    writer.writerow([a,b])
out.close()
