import os
import sys


def analysis(*args, **kwargs):
    with open("nginx_access.log") as f:
        recoreds = f.readlines()

    domain_rec = []
    for i, rec in enumerate(recoreds):
        try:
            status, time_, ip, _, domain, proc_time, ua = rec.split("^@")
            domain = domain.lower()
            ua = ua.lower()

            if int(status) in [200]:
                if domain not in domain_rec \
                        and "/static/" not in domain\
                        and "spider" not in ua \
                        and "bot" not in ua:
                    domain_rec.append(domain)
        except Exception as e:
            sys.stderr.write("line %s: %s\n" % (i, str(e)))

    return domain_rec
