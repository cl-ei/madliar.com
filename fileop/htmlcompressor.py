#!/usr/bin/env python

"""
A unity script build for safely reducing the size of html code.

Not finished yet!
"""

import re


def _split(content):
    inside = False
    snap = list()
    tag_list = list()

    for c in content:
        if inside:
            snap.append(c)
            if c == ">":
                tag_list.append({
                    "i": inside,
                    "s": "".join(snap),
                })

                snap = list()
                inside = False
        else:
            if c == "<":
                tag_list.append({
                    "i": inside,
                    "s": "".join(snap),
                })
                inside = True
                snap = ["<"]

            else:
                snap.append(c)

    if snap:
        tag_list.append({
            "i": inside,
            "s": "".join(snap),
        })

    return True


def _generate_tag_list(content):
    pt_html_tag = re.compile(r'<\s*(/?)\s*([^>]*)>([^<]*)')
    compressd = []
    layers = []
    for _ in pt_html_tag.findall(content)[:20]:
        
        if _[0] != "/":
            pass

        print _


# test
if __name__ == '__main__':
    with open("test.html") as f:
        content = f.read()
    
    _generate_tag_list(content)
    x = content
    non_attr = re.compile(r'([A-Za-z0-9-_]+)\s|\b([A-Za-z0-9-_]+)$')

    print "________"
    for _ in non_attr.findall(x):
        print _

    des_attr = re.compile(r'([A-Za-z0-9-_]+=(["|\'])((?<=\\)\2|[^"])+\2)')
    print "________"
    for _ in des_attr.findall(x):
        print _[0]

