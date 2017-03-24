# -*- coding:utf-8 -*-
import os
import re
import hashlib


def search(path, f_type):
    """
    To find all files with certain file extension in a path.
    """
    f_type = map(lambda x: x.lstrip(".").lower(), [f_type] if isinstance(f_type, str) else f_type)

    file_list = []
    for _ in os.listdir(path):
        full_path = os.path.join(path, _)

        if os.path.isfile(full_path):
            _, file_ext = os.path.splitext(full_path)
            if file_ext.lstrip(".").lower() in f_type:
                file_list.append(full_path)

        if os.path.isdir(full_path):
            file_list.extend(search(full_path, f_type))

    return file_list


def force_str(text, charset="utf-8"):
    return {
        str: lambda (t, c): t,
        unicode: lambda (t, c): t.encode(c)
    }.get(type(text))((text, charset))


def get_md5(text):
    _ = hashlib.md5()
    _.update(force_str(text))
    return _.hexdigest()


def _split(content):
    """
    A unity script build for safely reducing the size of html code.

    Not finished yet!
    """
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
    return pt_html_tag


if __name__ == '__main__':
    """Just for testing."""
    pass

