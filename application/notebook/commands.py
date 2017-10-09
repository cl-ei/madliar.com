import os
import pickle
import redis
from madliar.management import reg_command


@reg_command(name="clear_share_k")
def clear_share_k(*args, **kwargs):
    """
    Clear invalid sharing keys.
    """
    s = redis.Redis(db=8)
    print "\n" + "-" * 60
    skey_to_path_prefix = "memcache_SKEY_TO_PATH_*"
    path_to_skey_prefix = "memcache_PATH_TO_SKEY_*"

    need_delete_key = []
    still_using_key = []

    # delete skey_to_path
    all_share_key = s.keys(skey_to_path_prefix)
    for key in all_share_key:
        path = pickle.loads(s.get(key))
        if os.path.exists(path):
            still_using_key.append(key)
        else:
            print "Not existed: [%s]" % path
            need_delete_key.append(key)

    # dekete path_to_skey
    all_share_key = s.keys(path_to_skey_prefix)
    for key in all_share_key:
        path = key[len("memcache_PATH_TO_SKEY_"):]
        if os.path.exists(path):
            still_using_key.append(key)
        else:
            print "Not existed: [%s]" % path
            need_delete_key.append(key)

    print "\nNeed delete:"
    if need_delete_key:
        for key in need_delete_key:
            print "    %s" % key
    else:
        print "    None."

    print "\nStill using:"
    for key in still_using_key:
        print "    %s" % key

    if need_delete_key:
        r = raw_input("\nDelete invailed keys? (y/n)\n\t")
        if r == "y":
            s.delete(*need_delete_key)
    print "\nDone.\n" + "-"*60

