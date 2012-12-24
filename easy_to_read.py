#!/usr/bin/env  python3
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: 
#This program is very simple, it does this transform:
#"1234"   -->   "1,234"
#"12345"   -->   "12,345"
#"123456"   -->   "123,456"
#"1234567"   -->   "1,234,567"

# I read a simple solution on "Mastering Regular Expressions."
# re.sub(r"(?<=\d)(?=(\d\d\d)+$)", r"," , "123456")

import os
import sys


def iter_to_str(iterable):
    s = ""
    for x in iterable:
        s = s + x
    return s


def slice_every(n, s):
    rs = iter_to_str(reversed(s))
    rs_comma = ""
    for i in range(0, len(s)):
        rs_comma = rs_comma + rs[i]
        if i % n == (n - 1):
            rs_comma = rs_comma + ','

    if rs_comma[len(rs_comma) - 1] == ',':
        rs_comma = rs_comma[:-1]

    return iter_to_str(reversed(rs_comma))


if __name__ == "__main__":
    print(slice_every(int(sys.argv[1]), sys.argv[2]))


# vim: ai ts=4 sts=4 et sw=4
