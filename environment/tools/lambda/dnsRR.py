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

def lambda_handler(event, context):
    request_count = 0
    while True:
        request_count += 2
        #sleep(0.01) #100ms buffer to keep from getting throttled
        answer = resolver.query('somedomain.net', 'CNAME')
        for rdata in answer:
            url = ("http://%s" % rdata)[:-1]
            #print url
            #threads = []
            for i in range(1): # this is the # of threads, from 0 (e.g. 1 = 2 threads)
                t = threading.Thread(target=worker, args=(url,))
                #threads.append(t)
                t.start()
                
        #if request_count%1000 == 0:
            #print request_count

    # pip install dnspython