import collections
import os
import re

import requests as requests
from lxml import etree

nice_tree = collections.OrderedDict()
allTags = collections.OrderedDict()
xmlTagsAttr = collections.OrderedDict()
tagsDict = collections.OrderedDict()
initialTag = 'item'
url = 'https://www.thaiproperty.com/xmlfeed_hipflat'

r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
with open('data.xml', 'w') as f:
    f.write(r.text)
element = etree.parse('data.xml')

for tag in element.iter():
    path = re.sub('\[[0-9]+\]', '', element.getpath(tag))
    if path not in nice_tree:
        nice_tree[path] = []
    if len(tag.keys()) > 0:
        nice_tree[path].extend(attrib for attrib in tag.keys() if attrib not in nice_tree[path])

for path, attribs in nice_tree.items():
    finalPath = path.split(initialTag)
    if len(finalPath) > 1:
        if len(attribs) > 0:
            allTags[finalPath[1]] = [attribs]
        else:
            allTags[finalPath[1]] = []


def xml_tree_mapping(count, subCount):
    if count == 0:
        return key.replace("/", ">")
    elif subCount == 0:
        return key.replace("/", ">")


for key, val in allTags.items():
    key = key.replace('/', '', 1)
    count = 0
    subCount = 0
    for i, j in allTags.items():
        i = i.replace('/', '', 1)
        if key.startswith(i.split('/')[0]):
            if "/" in key:
                subCount += 1
            else:
                count += 1
    tagger = xml_tree_mapping(count, subCount)
    if len(val) > 0:
        xmlTagsAttr[tagger] = val
    else:
        xmlTagsAttr[tagger] = []

newXmlTags = xmlTagsAttr.copy()
for tag, attr in newXmlTags.items():
    found = tag.split('>')
    if len(found) > 1:
        if found[0] in xmlTagsAttr:
            xmlTagsAttr.pop(found[0])

for tag, attr in xmlTagsAttr.items():
    if tag != "":
        if len(attr) > 0:
            results_union = set().union(*attr)
            for a in results_union:
                mapper = '{}    string      `xml:"{}{}, attr"`'.format(tag.split('>')[-1], tag, a)
                print(mapper)
        else:
            mapper = '{}    string      `xml:"{}"`'.format(tag.split('>')[-1], tag)
            print(mapper)

os.remove('data.xml')
