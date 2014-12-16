#!/usr/bin/env python
"""
Normalize the promoter prediction score to [0-1] interval on each chromosome. 
The resulting BED file will be used in pppBenchmark program to evaluate the 
promoter prediction status.

Usage:
python norm_pred_score.py in.bed > out.bed  
"""

import re
import sys 
from operator import itemgetter

def BEDreader(fname):
    """
    parse the bed file 
    """

    bed_score = dict() 
    bfh = open(fname)
    for line in bfh:
        line = line.strip('\n\r').split('\t')
        assert len(line) == 5, '\t'.join(line)
        bed_score[float(line[3])] = 1
    bfh.close()
    return bed_score.keys()


def __main__():
    
    try:
        plus_fname = sys.argv[1]
    except:
        print __doc__
        sys.exit(-1)

    score = BEDreader(plus_fname)
    score = list(set(score))
    score.sort()

    min_score = score[0] 
    max_score = score[-1]

    min_score = score[1] if score[0] == -42.0 else min_score  

    bfh = open(plus_fname)
    for line in bfh:
        line = line.strip('\n\r').split('\t')
        assert len(line) == 5, '\t'.join(line)

        if float(line[3]) == -42.0:
            line[3] = min_score
        norm_score=(float(line[3])-min_score)/(max_score-min_score)

        bline = [line[0],
            line[1],
            line[2],
            str(round(norm_score, 4)),
            line[-1]
            ]
        print '\t'.join(bline)
    bfh.close()


if __name__=="__main__":
    __main__()
