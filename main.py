#!/usr/bin/python

import sys
from WeiboImageSpider import WeiboImageSpider

#3888497882 5650815551 1781285433 6064712141
def fetchImageByGivenID(id):
    weiboImageSpider = WeiboImageSpider(id)
    weiboImageSpider.getWeiboImageFactory()

def fetchImageByGivenIDWithRange(id, start, end):
    weiboImageSpider.getWeiboImageFactory(start, end)

def main():

    return

if __name__ == "__main__":
    main()




