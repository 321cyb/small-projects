#!/usr/bin/env  python3
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: Sat Dec 8  CST 2012
#Problem Description: http://cplus.about.com/od/programmingchallenges/a/programming-challenge-64-Sum-Some-Numbers.htm

import itertools
import functools
import logging

logging.basicConfig(level=logging.INFO)

def read_input():
    '''
    read input data from Numbers.txt.
    '''
    with open("Numbers.txt", "r") as f:
        input_data = f.read().split()
    return input_data


def solve(input_data):
    '''
    This is my naive implementation.
    '''
    sum_of_subarrays = []
    for i in range(0, 999):
        nest_list = [(input_data[i] + input_data[i+1], i, i+1)]
        for j in range(i+2, 1000):
            nest_list.append((nest_list[-1][0] + input_data[j], i, j))
        sum_of_subarrays.append(nest_list)
    #Now that we have a list of list to represent all the sub arrays.
    #We can just get the biggest number
    biggest = max(itertools.chain(*sum_of_subarrays))
    print(biggest)


def solve2(input_data):
    '''
    This one is from Programming Pearls, Chapter 8.
    But it doesn't remember the starting and ending positions,
    and it also accepts one element array.
    '''
    max_ending_here = 0
    max_so_far = 0
    for i in range(0, 1000):
        max_ending_here = max(max_ending_here + input_data[i], 0)
        max_so_far = max(max_ending_here, max_so_far)
    print(max_so_far)


if __name__ == "__main__":
    input_data = read_input()
    for i in range(0, 1000):
        input_data[i] = int(input_data[i])
    solve(input_data)
    solve2(input_data)

# vim: ai ts=4 sts=4 et sw=4
