#!/usr/bin/env python

import os
import sys
import urllib2
from BeautifulSoup import BeautifulSoup

url = sys.argv[1]
dir = sys.argv[2]
print 'Downloading the html...'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)
print 'Parsing the html to find the download_link class...'
func = soup.find('div', attrs={'class':'download_link'}).text
print 'Getting the direct link...'
for line in func.splitlines():
    if "kNO = " in line:
        import re
        dl_link = line.split('"')[1]

print dl_link

file_name = dl_link.split('/')[-1]
u = urllib2.urlopen(dl_link)
f = open(os.path.join(dir, file_name), 'wb')
print 'Downloading %s...' % file_name
f.write(u.read())
f.close()
print '%s was saved to the %s.' % (file_name, dir)
