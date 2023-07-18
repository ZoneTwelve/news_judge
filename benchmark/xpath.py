#!/usr/bin/env python
from lxml import etree
import sys

# read from stdin
html = sys.stdin.read()
xpath = sys.argv[1]


# html = sys.argv[0]
# xpath= sys.argv[1]
# print(html)

# root = etree.fromstring(html)
print('xpath',xpath)
# root = etree.HTML(html)
# result = root.xpath(xpath)

# result = root.xpath(xpath)

# print(result)


