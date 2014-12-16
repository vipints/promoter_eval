#!/usr/bin/env python
"""
program to filter out the N (repeat masked region in the genome) region prediction score

usage: 
python discard_mask_region.py in.fasta in.bz2 > out.bed 
"""

import sys
import itertools 
import collections 
from Bio import SeqIO
from gfftools import helper
from operator import itemgetter

def pred_score(BZF, DIScod):
    """
    reading through the arts prediction file  
    """

    for rec in BZF:
        rec = rec.strip("\n\r").split('\t')
        cnt = 0
        if rec[0] in DIScod:
            for ent in DIScod[rec[0]]:
                if (ent[0] <= int(rec[1]) and int(rec[1]) <= ent[1]):
                    cnt=1
                    break
        if cnt:
            continue 
        print '\t'.join(rec)


def fasta_reader(fname):
    """
    reading a FASTA file 
    """

    regions_removed = collections.defaultdict(list)
    for rec in SeqIO.parse(fname, "fasta"):
        #rec.id = 'chr'+rec.id
        Nindex = [item for item in range(len(rec.seq)) if rec.seq[item]=="N"] ##index of the desired nucleotide 
        for xn, xp in itertools.groupby(enumerate(Nindex), lambda (i,x):i-x): ## 
            cod_range = map(itemgetter(1), xp)
            regions_removed[rec.id].append((cod_range[0], cod_range[-1]))
    return regions_removed


try:
    ffa=sys.argv[1]
    fbz=sys.argv[2]
except:
    print __doc__
    sys.exit(-1)

dis_cod = fasta_reader(ffa)

bzh = helper.open_file(fbz)

pred_score(bzh, dis_cod)
