#!/usr/bin/env  python
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: 

#See the format of pcap file here: http://wiki.wireshark.org/Development/LibpcapFileFormat


import sys
import argparse
from scapy.all import *


def exchange(recs, index_list):
    assert len(index_list) == 2
    lrecs=len(recs)
    index1=int(index_list[0])-1
    index2=int(index_list[1])-1

    if (index1 >= lrecs) or (index2 >= lrecs):
        print "Index value greater than number of pcap records" 
        sys.exit()
    else:
        recs[index1], recs[index2] = recs[index2], recs[index1]
        recs[index1].time, recs[index2].time = recs[index2].time, recs[index1].time
        return recs


def remove(recs, index_list):
    assert len(index_list) == 1
    lrecs=len(recs)
    index=int(index_list[0])-1

    if (index >= lrecs):
        print "Index value greater than number of pcap records"
        sys.exit()
    else:
        del recs[index]
        return recs


def slice(recs, index_list):
    assert len(index_list) == 2
    lrecs=len(recs)
    index1=int(index_list[0])-1
    index2=int(index_list[1])-1

    if (index1 >= lrecs) or (index2 >= lrecs) or (index1 > index2):
        print "Index value greater than number of pcap records or start is bigger than end." 
        sys.exit()
    else:
        orecs=[]
        for i in xrange(index1, index2 + 1): 
            orecs.append(recs[i])
        return orecs



def copyto(recs, index_list):
    """
    index_list has 2 items, the first index is the one that will be copied,
    the second index is the place that will be pasted before, so this could be [1, len(recs) + 1].
    """
    assert len(index_list) == 2
    lrecs=len(recs)
    index1=int(index_list[0])-1
    index2=int(index_list[1])-1
    
    if index2 > lrecs:
        index2 = lrecs

    if (index1 >= lrecs):
        print "Index value greater than number of pcap records or start is bigger than end." 
        sys.exit()
    else:
        import copy
        rec = copy.deepcopy(recs[index1])
        #give it an appropriate value based the previous and the next packet time.
        if index2 ==0:
            rec.time = recs[index2-1].time - 0.1
        elif index2 == lrecs:
            rec.time = recs[index2].time + 0.1
        else:
            rec.time = (recs[index2-1].time + recs[index2].time)/2
        recs.res.insert(index2, rec)
        return recs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="manipulate pcap files")
    parser.add_argument("command", choices=["exchange", "remove", "slice", "copyto"])
    parser.add_argument("-i", dest="infile", required=True)
    parser.add_argument("-o", dest="outfile", required=True)
    parser.add_argument("index", type=int, nargs="+")
    args = parser.parse_args()


    recs = rdpcap(args.infile)
    result = getattr(sys.modules[__name__], args.command)(recs, args.index)
    wrpcap(args.outfile, result)




# vim: ai ts=4 sts=4 et sw=4
