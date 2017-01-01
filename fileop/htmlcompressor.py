#!/usr/bin/env python

"""
A unity script build for safely reducing the size of html code.
"""

import re
html_tag = re.compile(r'hello')

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
    pt_html_tag = re.compile(r'<([^/>]*)/?>([^<]*)?')    
    for _ in pt_html_tag.findall(content)[:20]:
        print _

    # match = pattern.match(content)
    # if match:



# test
if __name__ == '__main__':
    with open("test.html") as f:
        content = f.read()
    
    _generate_tag_list(content)
    # import time
    # start = time.time()
    # content = Dom(content)
    # content._split()
    # end = time.time()

    # print end - start
