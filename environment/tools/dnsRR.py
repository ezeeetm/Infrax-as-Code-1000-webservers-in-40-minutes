#!/usr/bin/env python
import dns.resolver
import urllib2
import threading
from time import sleep

def worker(url):
    """thread worker function"""
    try:
        resp = urllib2.urlopen(url).read()
    except:
        pass
    return

# 205.251.199.68 is ns-1860.awsdns-40.co.uk for app.neudemo.net domain
resolver = dns.resolver.Resolver()
resolver.nameservers = ['205.251.199.68']

while True:
    sleep(0.01) #100ms buffer to keep from getting throttled
    answer = resolver.query('somedomain.com', 'CNAME')
    for rdata in answer:
        url = ("http://%s" % rdata)[:-1]
        print url
        threads = []
        for i in range(1): # this is the # of threads
            t = threading.Thread(target=worker, args=(url,))
            threads.append(t)
            t.start()

# pip install dnspython