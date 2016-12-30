#!/usr/bin/env python

"""
A unity script build for safely reducing the size of html code.
"""

# situation table
# 0: normal
# 1: in a left labal
# 2: in 
_SITUATION_TABLE = {
    "": {

    },
    "":{

    }
}


def _calc(c, situation):
    decision = _SITUATION_TABLE.get(situation).get(c, True)
    return (c if decision else ""), situation

# 0 < 1 > 0
def _split(content):
    snaps = []
    pos = 0
    local = []

    for c in content:
        if pos == 0:
            if c == "<":
                pos = 1
                snaps.append("".join(local))
                local = ["<"]

            else:
                local.append(c)

        elif pos == 1:
            local.append(c)
            if c == ">":
                pos = 0                
                snaps.append("".join(local))
                local = []

    return snaps



def compress(content):
    pure = []
    situation = 0

    for c in content:
        _, situation = _calc(c, situation)
        pure.append(_)

    return "".join(pure)

# test
if __name__ == '__main__':
    with open("test.html") as f:
        content = f.read()

    content = _split(content)

    print content