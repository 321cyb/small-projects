#!/usr/bin/env  python3
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: Fri Sep 21 09:17:19 CST 2012
#This is written to get a snapshot of all SPRs 
#that I care in Tektronix.

import os
import sys
import json
import re
import csv

try:
    import httplib2
    import bs4
except ImportError:
    sys.exit(1)

SCM_URL = "http://www.example.com/view.php?"

h = None
spanWriter=None


def get_printable(s):
    new_s = ""
    for i in s:
        if i.isprintable():
            new_s = new_s + i
    return new_s

def get_one_SPR(spr):
    '''
    argument spr: a string like "NA_SPR_23123"
    '''
    if not re.match(r"(NA|IRIS)_(SPE|SPR)_(\d+)", spr, re.IGNORECASE):
        return 

    scm_url = SCM_URL + spr
    s = h.request(scm_url)[1].decode()
    soup = bs4.BeautifulSoup(s)
    number = get_printable(soup.find("td", text="SPR Number").findNext("td").string.strip())
    title = get_printable(soup.find("b", text="Title:").parent.findNext("td").contents[0].string.strip())
    status = get_printable(soup.find("td", text="Current SPR Status").findNext("td").string.strip())
    severity = get_printable(soup.find("td", text="Severity").findNext("td").string.strip())
    loggedBy = get_printable(soup.find("td", text="Logged By").findNext("td").string.strip())
    print( number+ '\t' + title + '\t' + status + '\t' + severity + '\t' + loggedBy) 
    spanWriter.writerow([number, title, status, severity, loggedBy])
    


if __name__ == "__main__":
    h = httplib2.Http("/home/ychen6/.cache")

    with open("config.json") as f:
        j = json.load(f)
        spanWriter = csv.writer(open("SPR-Status.csv", "w", newline=""), quoting=csv.QUOTE_MINIMAL)

        for spr in j:
            get_one_SPR(spr)


# vim: ai ts=4 sts=4 et sw=4
