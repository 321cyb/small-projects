#!/usr/bin/env  python3
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: 

import math


#This is a dictionary of all the prime numbers less than 20.
primeDict = {2: 0, 3: 0, 5: 0, 7: 0, 11: 0, 13: 0, 17: 0, 19: 0}

def isPrime(n):
    if n == 2:
        return True
    else:
        for i in range(2, math.ceil(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
    return True

def updatePrimeDict(n):
    global primeDict
    localPrimeDict = {2: 0, 3: 0, 5: 0, 7: 0, 11: 0, 13: 0, 17: 0, 19: 0}
    prime = 2
    while not isPrime(n):
        for i in [x for x in range(prime, math.ceil(math.sqrt(n)) + 1) if isPrime(x)]:
            if n % i == 0:
                n = n / i
                prime = i
                localPrimeDict[i] += 1
                break
    localPrimeDict[int(n)] += 1
    #next, update the global prime dictionary with the local one.
    for i in primeDict:
        if localPrimeDict[i] > primeDict[i]:
            primeDict[i] = localPrimeDict[i]


if __name__ == "__main__":
    for i in range(3, 21):
       updatePrimeDict(i)
    #print(primeDict)
    mul = 1
    for i in primeDict:
        mul = mul * (pow(i, primeDict[i]))
    print(mul)



# vim: ai ts=4 sts=4 et sw=4
