#!/bin/python

import sys
import csv
from nltk.tokenize import wordpunct_tokenize
from dataset import *
import optparse

gold_dir = 'gold-data/gold'
datafile = 'mturk-data/esl.tsv'

dir = sys.argv[1]

optparser = optparse.OptionParser()
optparser.add_option("-d", "--data", dest="results", default="result.txt", help="Data filename prefix (default=data)")
(opts, args) = optparser.parse_args()
data = "%s" % (opts.results)




#S The cat sat at mat .
#A 3 4|||Prep|||on|||REQUIRED|||-NONE-|||0
#A 4 4|||ArtOrDet|||the||a|||REQUIRED|||-NONE-|||0
#A <start offset> <end offset>|||<error type>|||<correction1>||<correction2||..||correctionN|||<required>|||<comment>|||<annotator id>

gold = {s.line : s for s in DataSet(gold_dir)}

ref = open('%s/gold.m2'%dir, 'w')
systm = open('%s/system.m2'%dir, 'w')

errs = 0

result = [list(line.strip().split("\t")) for line in open(data).readlines()]
lines = [int(ele[0]) for ele in result]
listlength = len(lines)
selectedLines30 = lines[:int(listlength * 0.3)]

for num, line in enumerate(csv.DictReader(open(datafile), delimiter='\t'), 0):
	if(num in lines or num == 0):
		gs = gold[line['Translation']]
		try : ref.write('S %s\n'%' '.join(wordpunct_tokenize(gs.line)).encode('ascii'))
		except : errs +=1; continue;
		for c in gs.corrections:
			ref.write(('A %d %d|||%s|||%s|||REQUIRED|||-NONE-|||0\n'%(c.i(), c.j(), c.code, c.corrected_text)).encode('ascii'))
		ref.write('\n')
		systm.write('%s\n'%' '.join(wordpunct_tokenize(line['Corrected'])).encode('ascii'))

#print errs

ref.close()
systm.close()

