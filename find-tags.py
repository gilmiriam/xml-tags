import collections
import os
import re

import requests as requests
from lxml import etree

url = 'https://www.thaiproperty.com/xmlfeed_hipflat'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
with open('data.xml', 'w') as f:
    f.write(r.text)
element = etree.parse('data.xml')
nice_tree = collections.OrderedDict()

for tag in element.iter():
    path = re.sub('\[[0-9]+\]', '', element.getpath(tag))
    if path not in nice_tree:
        nice_tree[path] = []
    if len(tag.keys()) > 0:
        nice_tree[path].extend(attrib for attrib in tag.keys() if attrib not in nice_tree[path])

allTags = collections.OrderedDict()
initialTag = 'item'

for path, attribs in nice_tree.items():
    finalPath = path.split(initialTag)
    if len(finalPath) > 1:
        if len(attribs) > 0:
            allTags[finalPath[1]] = [attribs]
        else:
            allTags[finalPath[1]] = []
xmlTags = []
xmlTagsAttr = collections.OrderedDict()
found = allTags.items()
for key, val in allTags.items():
    count = 0
    subCount = 0
    for i, j in found:
        if key.startswith(i.split('/')[0]):
            if "/" in key:
                subCount += 1
            else:
                count += 1
    if count == 1 and subCount == 0:
        xmlTags.append(key)
        xmlTagsAttr[key.replace("/", ">")] = []
        if len(val) > 0:
            xmlTagsAttr[key.replace("/", ">")] = val

    if count == 0 and subCount >= 1:
        xmlTags.append(key.replace("/", ">"))
        xmlTagsAttr[key.replace("/", ">")] = []
        if len(val) > 0:
            xmlTagsAttr[key.replace("/", ">")] = val

for tag, attr in xmlTagsAttr.items():
    if len(attr) > 0:
        results_union = set().union(*attr)
        for a in results_union:
            mapper = '{}    string      `xml:"' + initialTag + '{}>{}, attr"`'.format(tag, tag, a)
            print(mapper)
    else:
        mapper = '{}    string      `xml:"' + initialTag + '{}"`'.format(tag, tag)
        print(mapper)

os.remove('data.xml')
