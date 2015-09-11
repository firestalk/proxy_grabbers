#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from requests.exceptions import ConnectTimeout, ReadTimeout, ConnectionError
from lxml import html

PROXY_SRC = 'http://www.sslproxies.org/'
CHK_SITE = 'http://docs.python-requests.org/en/latest/'
CHK_STR = 'Not in Python.'
TIMEOUT = 3


def main():
    proxylist = get_proxylist()
    print("Got {} proxies, checking them now..".format(len(proxylist)))
    good = []
    for i in proxylist:
        chk = check_proxy(i)
        if chk is True:
            good.append(i)
    print('Good proxies left: {}'.format(len(good)))
    return good


def check_proxy(pstr):
    proxy = {'http': pstr}
    try:
        req = requests.get(CHK_SITE, proxies=proxy, timeout=TIMEOUT)
    except ConnectTimeout:
        print("BAD: {}, REASON: Connection Timeout".format(pstr))
        return False
    except ReadTimeout:
        print("BAD: {}, REASON: Read Timeout".format(pstr))
        return False
    except ConnectionError:
        print("BAD: {}, REASON: Connection Error".format(pstr))
        return False
    body = req.text
    if CHK_STR not in body:
        print("BAD: {}, STATUS CODE: {}".format(pstr, req.status_code))
        return False
    else:
        print("GOOD: {}, STATUS CODE: {}".format(pstr, req.status_code))
        return True


def get_proxylist():
    req = requests.get(PROXY_SRC)
    htree = html.fromstring(req.text)
    plist = htree.xpath(".//*[@id='proxylisttable']/tbody/tr/td/text()")
    reslist = []
    while len(plist) > 0:
        ip = plist.pop(0)
        port = plist.pop(0)
        ccode = plist.pop(0)
        country = plist.pop(0)
        anon = plist.pop(0)
        google = plist.pop(0)
        https = plist.pop(0)
        lastchk = plist.pop(0)
        reslist.append('http://{}:{}'.format(ip, port))
    return reslist


if __name__ == '__main__':
    proxy_lst = main()
    if len(proxy_lst) > 0:
        with open('proxylist.txt', 'w') as f:
            f.write('\n'.join(proxy_lst))
