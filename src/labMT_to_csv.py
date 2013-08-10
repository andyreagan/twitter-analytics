#!/usr/bin/python

# labMT_stopword_parser.py

# read in the labMT word set, print a new one with varying delta h

# center of valence
center=5.0

# different values to print
#delH=[.25*i for i in range(9)]
#print delH

# files to pring
#delH_files=['labMT1_' + i + '.txt' for i in ['000','025','050','075','100','125','150','175','200']]
#print delH_files

#for i in range(9):
tmplabMT=open('labMT1.txt','r')
#delta=delH[i]
tmplabMT_dump=open('labMT1.csv','w')
j=0
for line in tmplabMT:
  j+=1
  tmpline = line.split('\t')
  if len(tmpline) > 2:
    #if float(tmpline[2]) >= center+delta or float(tmpline[2]) <= center-delta:
    tmpstr=tmpline[1]+','+tmpline[2]+'\n'
    tmplabMT_dump.write(tmpstr)
  else:
    print j
tmplabMT.close()
tmplabMT_dump.close()
