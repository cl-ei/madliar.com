#!/usr/bin/env python

"""
A unity script build for safely reducing the size of html code.
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

def conpress():
    pass


# test
if __name__ == '__main__':
    with open("test.html") as f:
        content = f.read()
    

    import time
    start = time.time()
    #_generate_tag_list(content)
    end = time.time()

    print end - start


x = """meta name="viewport" content="width=device-width, in\"itial-scale=1" /"""
pt_html_tag = re.compile(r'(\w+(=\"(?!")\")?)')
print pt_html_tag.findall(x)