#!/usr/bin/env  python3
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: 
#See the description of problem here:
#http://blog.zhaojie.me/2012/11/how-to-generate-typoglycemia-text.html
#
#Here's a version from Internet, only one line:
#' '.join(map(lambda w:w if len(w)<4 else w[0]+''.join((lambda l:random.shuffle(l)or l)(list(w[1:-1]))) +w[-1], text.split(' ')))
#or this one:
#" ".join(["".join([t[0],"".join(random.sample(list(itertools.permutations(t[1:-1],len(t)-2)),1)[0]),t[-1]]) for t in text.split(" ")])

import random
import sys

def process_a_word(word):
    if len(word) > 3:
            first = word[0]
            last  = word[-1]
            middle = list(word[1:-1])
            #random.shuffle always return None.
            result = first + "".join(random.shuffle(middle) or middle) + last
            sys.stdout.write(result)
    elif word is not "":
        sys.stdout.write(word)




def typoglycemia(p):
    seg = ""
    for c in p:
        if not c.isalpha():
            process_a_word(seg)
            seg = ""
            sys.stdout.write(c)
        else:
            seg = seg + c
    process_a_word(seg)
    print("")


text = "According to a research at Cambridge University, it doesn't matter in what order the letters in a word are, the only important thing is that the first and last letter be at the right place, the reset can be a total mess and you can still read it without problem. This is because the human mind does not read every letter by itself, but the word as a whole. Amazing!"


if __name__ == "__main__":
    print(text)
    print("")
    typoglycemia(text)





# vim: ai ts=4 sts=4 et sw=4
