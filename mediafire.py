#!/usr/bin/env python

import os
import sys
import urllib2
import time
from BeautifulSoup import BeautifulSoup


def download(filename, quickkey, dir):
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
    
    u = urllib2.urlopen(dl_link)
    f = open(os.path.join(dir, filename), 'wb')
    print 'Downloading %s...' % filename
    f.write(u.read())
    f.close()
    print '%s was saved to the %s.' % (filename, dir)


def get_links(url, dir):
    folder_key = url.split("?")[1]
    page = urllib2.urlopen("http://www.mediafire.com/api/folder/get_content.php?folder_key=%s&content_type=files" % folder_key)
    soup = BeautifulSoup(page)
    files = soup.findAll('file')
    for f in files:
        filename = f.find('filename').string
        quickkey = f.find('quickkey').string
        download(filename, quickkey, dir)
        time.sleep(3)


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print "Usage: %s <url> <directory>" % sys.argv[0]
        sys.exit(1)
    if len(sys.argv) == 3:
        dir = sys.argv[2]
    else:
        dir = os.getcwd()
    if sys.argv[1].startswith("http://www.mediafire.com/?"):
        url = sys.argv[1]
        get_links(url, dir)
    else:
        file = sys.argv[1].encode('string-escape')
        with open(file) as f:
            for url in f:
                get_links(url.strip(), dir)


if __name__ == '__main__':
    main()
