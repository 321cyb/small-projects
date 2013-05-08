#!/usr/bin/env  python
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: 

#See the format of pcap file here: http://wiki.wireshark.org/Development/LibpcapFileFormat


import sys
from scapy.all import *


def help():
    print "{0} pcap-file-name index1 index2(1 based)".format(sys.argv[0])
    sys.exit()

if len(sys.argv) != 4:
    help()

recs=rdpcap(sys.argv[1])
lrecs=len(recs)
index1=int(sys.argv[2])-1
index2=int(sys.argv[3])-1

if (index1 >= lrecs) or (index2 >= lrecs):
    print "Index value greater than number of pcap records" 
    sys.exit()
else:
    recs[index1], recs[index2] = recs[index2], recs[index1]
    recs[index1].time, recs[index2].time = recs[index2].time, recs[index1].time


wrpcap(sys.argv[1], recs)



# vim: ai ts=4 sts=4 et sw=4
