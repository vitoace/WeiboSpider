#!/usr/bin/python

import sys
import time
from WeiboImageSpider import WeiboImageSpider

def main():
    uuids = [#5650815551,# huangyaya
             #1781285433,# YoonJoo_Son
             #5607044619,# Catherine aili
             #6064712141,# ming mo shishang
             #2242047663,# iess
             #2268638705,# shiyi jia
             #3888497882,# xfybf1
             ]
    failed_uuids = []
    for uuid in uuids:
        try:
            weiboImageSpider = WeiboImageSpider(uuid)
            weiboImageSpider.getWeiboImageFactory(0, 100)
            time.sleep(240)
        except Exception as e:
            print e
            failed_uuids.append(uuid)
            print "failed to get uuid"


    if failed_uuids:
        print "The following uuids failed: {}".format(str(failed_uuids))
    return

if __name__ == "__main__":
    main()
