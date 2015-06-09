#!/usr/bin/env python

import requests
import json

res = requests.get("https://bower-component-list.herokuapp.com/")
j = json.loads(res.text)

def mykey(item):
    return item["stars"]

# sort by star count
s = sorted(j, key=mykey, reverse=True)

# The best 10,000 repos.
for x in xrange(10000):
    print s[x]["stars"], s[x]["name"]
