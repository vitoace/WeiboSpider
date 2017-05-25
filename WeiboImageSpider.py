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
    _cookie = {"Cookie": "_T_WM=c49032e6861cf848dcf56dfab45c9668; M_WEIBOCN_PARAMS=featurecode%3D20000180%26oid%3D4110344157372113%26luicode%3D20000061%26lfid%3D4110344157372113; SUB=_2A250Jw3dDeThGeNM4lUZ9ivIyTSIHXVX65OVrDV6PUJbkdBeLXX8kW2ZCDutsECFNPcYaPMKwSD8mgKvcQ..; SUHB=0U1Zmga_cBjBtz; SCF=ApDTCcjcEyoZE18BJi-WIVglDsbZ-C0Q-8lgFrpfLpb0raNLEn0dBQBvUKaioGz-9gm8eQU7R0mK7_bb4Tctwto.; SSOLoginState=1495498125"}
    pageNum = 0
    _id = 0
    _image_count = 0
    _offset = 10
    _trunk_size = 50
    _lock = threading.Lock()

    def __init__(self, id):
        self._id = id
        url = 'http://weibo.cn/u/%d?filter=1&page=1'%id
        html = requests.get(url, cookies = self._cookie).content
        selector = etree.HTML(html)
        self.pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
        print "There are {} pages in total".format(self.pageNum)

    def getWeiboImageFactory(self, start, end):
        if not start:
            start = 0
        if not end:
            end = self.pageNum

        for i in range((self.pageNum-1) / 50):
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
            url = 'http://weibo.cn/u/%d?filter=1&page=%d'%(self._id,page)
            print url
            lxml = requests.get(url, cookies = self._cookie).content
            time.sleep(3)
            soup = BeautifulSoup(lxml, "lxml")

            urllist = soup.find_all('a',href=re.compile(r'http.?://weibo.cn/mblog/oripic',re.I))
            for imgurl in urllist:
                urllist_set.add(requests.get(imgurl['href'], cookies = self._cookie).url)

        link = ""
        fo = open("/Users/Vito/Documents/picCatcher/%s_imageurls%d"%(self._id, start), "wb")
        for eachlink in urllist_set:
            link = link + eachlink +"\n"
        fo.write(link)

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
