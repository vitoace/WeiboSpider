#!/usr/bin/python

import sys
import re

url = 'http://ww2.sinaimg.cn/large/6a2c4239gw1ex6h4tdfh7j20yi0ovwjq.jpg'
m = re.search('.*/(.*)', url)
print m.group(1)

