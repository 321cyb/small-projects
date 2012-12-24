#!/usr/bin/env  python3
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: 
#
#Problem Description: https://www.interviewstreet.com/challenges/dashboard/#problem/4efa210eb70ac

import sys
import logging

logging.basicConfig(level = logging.ERROR)

def set_of_a_string(string):
    s = set()
    for l in range(1, len(string) + 1):
        for i in range(0, len(string)):
            s.add(string[i:i+l])
    return s


if __name__ == "__main__":
    cases = int(sys.stdin.readline())
    s = set()
    for i in range(0, cases):
        s = s.union(set_of_a_string(sys.stdin.readline().strip()))
    l = list(s).sort()
    queries = int(sys.stdin.readline())
    for i in range(0, queries):
        index = int(sys.stdin.readline())
        if index <= len(l):
            print(l[index - 1])
        else:
            print("INVALID")





# vim: ai ts=4 sts=4 et sw=4
