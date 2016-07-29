#!/usr/bin/env python
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

while True:
    sleep(0.01) #100ms buffer to keep from getting throttled
    url = 'http://dns.hostname.here.com' #be sure to include http://
    print url
    threads = []
    for i in range(1): # this is the # of threads
        t = threading.Thread(target=worker, args=(url,))
        threads.append(t)
        t.start()