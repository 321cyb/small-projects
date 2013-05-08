#!/usr/bin/env  python
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: 

#See the format of pcap file here: http://wiki.wireshark.org/Development/LibpcapFileFormat


import sys
from scapy.all import *


def help():
    print "{0} pcap-file-name output-pcap-file start end(1 based)".format(sys.argv[0])
    sys.exit()

if len(sys.argv) != 5:
    help()

recs=rdpcap(sys.argv[1])
lrecs=len(recs)
orecs=[]
start=int(sys.argv[3])-1
end=int(sys.argv[4])-1

if (end >= lrecs) or (start >= end):
    print "Index value greater than number of pcap records or start is bigger than end." 
    sys.exit()
else:
    for i in xrange(start, end + 1):
        orecs.append(recs[i])


wrpcap(sys.argv[2], orecs)



# vim: ai ts=4 sts=4 et sw=4
