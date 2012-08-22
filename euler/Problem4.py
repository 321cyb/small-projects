#!/usr/bin/env  python3
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: 


def isPalindromic(n):
    digitsList = []
    while n > 9:
        n, r = divmod(n,10)
        digitsList.append(r)
    digitsList.append(n)
    #Now we have all the digits in a list.
    digitsListCopy = digitsList[:]
    digitsListCopy.reverse()
    if digitsList == digitsListCopy:
        return True
    else:
        return False


def getAnswer():
    l = []
    for x in range(999, 99, -1):
        for y in range(999, 99, -1):
            if isPalindromic(x * y):
                l.append(x*y)
    return max(l)


if __name__ == "__main__":
    print(getAnswer())


# vim: ai ts=4 sts=4 et sw=4
