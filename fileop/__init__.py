#!/usr/bin/env python

import os

def search(path, f_type):
    """
    To find all files with certain file extension in a path.
    """
    f_type = f_type.lower()

    file_list = []
    for _ in os.listdir(path):
        full_path = os.path.join(path, _)

        if os.path.isfile(full_path):
            _, file_ext = os.path.splitext(full_path)
            if file_ext.lstrip(".").lower() == f_type:
                file_list.append(full_path)

        if os.path.isdir(full_path):
            file_list += search(full_path, f_type)

    return file_list
