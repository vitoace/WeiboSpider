#!/usr/bin/python

import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree
import threading
import uuid
import time

class WeiboImageSpider:
    _cookie = {"Cookie" : "_T_WM=c49032e6861cf848dcf56dfab45c9668; SCF=ApDTCcjcEyoZE18BJi-WIVglDsbZ-C0Q-8lgFrpfLpb0rAz2W340C0xfpDTmOg7dHSotozqnTgVxFExoXMu4-aI.; SUB=_2A250TYDGDeThGeNM4lUZ9ivIyTSIHXVXsSCOrDV6PUJbkdBeLUbgkW0xX_eAf3HrON2fc0zH6BWEjeXXWw..; SUHB=0C1SR0Sy0h_WHO; SSOLoginState=1498017942"}
    pageNum = 0
    _id = 0
    _image_count = 0
    _offset = 10
    _trunk_size = 50
    _lock = threading.Lock()

    def __init__(self, uid):
        self._id = uid
        url = 'http://weibo.cn/u/{}?filter=1&page=1'.format(uid)
        html = requests.get(url, cookies = self._cookie).content
        selector = etree.HTML(html)
        self.pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
        print "There are {} pages in total".format(self.pageNum)

    def getWeiboImageFactory(self, start=0, end=0):
        if end == 0:
            end = self.pageNum

        for i in range((end-1) / 50 + 1):
            start = i*50
            end = (i+1)*50 if self.pageNum > (i+1)*50 else self.pageNum
            threads = []
            while (start < end):
                t = threading.Thread(target=self._getWeiboImageWithPageRange, args=(start,))
                threads.append(t)
                t.start()

                start += self._offset
                
            for t in threads:
                t.join()

            time.sleep(20)

    def _getWeiboImageWithPageRange(self, start):
        print threading.currentThread().getName(), 'Starting'
        urllist_set = set()

        # Get image urls
        for page in range(start+1, start+self._offset-1):
            url = 'http://weibo.cn/u/{}?filter=1&page={}'.format(self._id, page)
            print url
            lxml = requests.get(url, cookies = self._cookie).content
            time.sleep(3)
            soup = BeautifulSoup(lxml, "lxml")

            urllist = soup.find_all('a',href=re.compile(r'http.?://weibo.cn/mblog/oripic',re.I))
            for imgurl in urllist:
                urllist_set.add(requests.get(imgurl['href'], cookies = self._cookie).url)

        #link = ""
        #fo = open("/Users/Vito/Documents/picCatcher/{}_imageurls{}".format(self._id, start), "wb")
        #for eachlink in urllist_set:
        #    link = link + eachlink +"\n"
        #fo.write(link)
        #fo.close()

        # Download images and save them
        if not urllist_set:
            print 'No pictures in the url'
        else:
            image_path=os.getcwd()+'/'+str(self._id)
            if os.path.exists(image_path) is False:
                os.mkdir(image_path)
            for imgurl in urllist_set:
                self._lock.acquire()
                try:
                    self._image_count += 1
                finally:
                    self._lock.release()

                print(imgurl)
                m = re.search('.*/(.*)', imgurl)
                imageName = m.group(1)
                temp= image_path + '/%s' % imageName
                print temp
                print 'Downloading picture: %s' % self._image_count
                try:
                    urllib.urlretrieve(urllib2.urlopen(imgurl).geturl(),temp)
                    time.sleep(3)
                except:
                    print "Failed to download this pic:%s"%imgurl

        print threading.currentThread().getName(), 'Exiting'
