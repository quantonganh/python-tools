#!/usr/bin/env python

import os
import sys
import urllib2
from BeautifulSoup import BeautifulSoup


def download(quickkey, dir):
    mediafire_url = "http://www.mediafire.com/?"
    get_info_api = "http://www.mediafire.com/api/file/get_info.php?quick_key="
    url = ''.join([mediafire_url, quickkey])
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
    
    file_info = urllib2.urlopen(''.join([get_info_api, quickkey]))
    file_soup = BeautifulSoup(file_info)
    filename = file_soup.find('filename').string

    u = urllib2.urlopen(dl_link)
    f = open(os.path.join(dir, filename), 'wb')
    print 'Downloading %s...' % filename
    f.write(u.read())
    f.close()
    print '%s was saved to the %s.' % (filename, dir)


def get_links():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print "Usage: %s <url> <directory>" % sys.argv[0]
        sys.exit(1)
    url = sys.argv[1]
    if len(sys.argv) == 3:
        dir = sys.argv[2]
    else:
        dir = os.getcwd()
    folder_key = url.split("?")[1]
    page = urllib2.urlopen("http://www.mediafire.com/api/folder/get_content.php?folder_key=%s&content_type=files" % folder_key)
    soup = BeautifulSoup(page)
    files = soup.findAll('file')
    for f in files:
        filename = f.find('filename').string
        quickkey = f.find('quickkey').string
        download(quickkey, dir)

if __name__ == '__main__':
    get_links()
