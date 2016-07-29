#!/usr/bin/env python
import dns.resolver
import urllib2

# 205.251.199.104 is ns-1896.awsdns-45.co.uk
resolver = dns.resolver.Resolver()
resolver.nameservers = ['205.251.199.104']

answer = resolver.query('jenkins.trycatchfinally.fail')
for rdata in answer:
    url = "http://%s" % rdata
    print url
    resp = urllib2.urlopen(url).read()
    print resp




# on lambda AMI, do sudo pip install dnspython