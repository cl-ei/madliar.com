import random
import string


def randstr(length=24):
    """
    Generate a new random string.

    """
    choices = string.letters + string.digits
    keylist = [random.choice(choices) for i in range(length)]
    return "".join(keylist)

