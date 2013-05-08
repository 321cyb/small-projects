#!/usr/bin/env  python
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: 

#See the format of pcap file here: http://wiki.wireshark.org/Development/LibpcapFileFormat


from scapy.all import *
import sys


def help():
    print "{0} pcap-file-name index(1 based)".format(sys.argv[0])
    sys.exit()

if len(sys.argv) != 3:
    help()

recs=rdpcap(sys.argv[1])
lrecs=len(recs)
index=int(sys.argv[2])-1

if (index >=lrecs):
    print "Index value greater than number of pcap records"
    sys.exit()
else:
    del recs[index]

wrpcap(sys.argv[1], recs)



# vim: ai ts=4 sts=4 et sw=4
