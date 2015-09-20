#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
XROXY Parse Lib
v0.4
"""
from grab import Grab

STARTLINK = 'http://www.xroxy.com/proxylist.php?port=&type=All_http&ssl=&country=&latency=3000&reliability=9000&sort=latency'


class XroxyLib():
    def __init__(self):
        self.g = Grab()

    def main(self):
        pages = self.get_pages(STARTLINK)
        pg_list = []
        for i in pages:
            pg_list.extend(self.parsepage(i))
        return pg_list

    def print_lst(self, prefix=''):
        newlist = self.main()
        for i in newlist:
            print(prefix + i["ip"] + ":" + i["port"])

    def get_pages(self, link):
        self.g.go(link)
        # Getting total proxy count
        pcount = int(self.g.doc.select('/html/body/div/div[2]/table[2]/tr/td[1]/table/tr[2]/td/small/b').text())
        pagescount = pcount // 10 + 1
        pagelist = []
        for i in range(pagescount):
            pagelink = STARTLINK + '&pnum=' + str(i)
            pagelist.append(pagelink)
        return(pagelist)

    def parsepage(self, link):
        self.g.go(link)
        lst = self.g.doc.select('/html/body/div/div[2]/table[1]/tr[@class]/td')
        if len(lst) < 1:
            return []
        return self.parse_lst(lst)

    def parse_lst(self, lst):
        """
        0 - foxyproxy link -- deleting
        1 - ip
        2 - port
        3 - proxy type
        4 - SSL support
        5 - proxy location
        6 - latency
        7 - reliability
        8 - Details -- deleting
        """
        proxylist = []
        it = 1
        proxyd = {}
        for i in lst:
            stri = i.text().strip()
            if len(stri) < 2 or stri == 'Details':
                continue
            if it == 1:
                proxyd["ip"] = stri
            if it == 2:
                proxyd["port"] = stri
            if it == 3:
                proxyd["type"] = stri
            if it == 4:
                proxyd["ssl"] = stri
            if it == 5:
                proxyd["location"] = stri
            if it == 6:
                proxyd["latency"] = stri
            if it == 7:
                proxyd["reliability"] = stri
            it += 1
            if it > 7:
                proxylist.append(proxyd)
                proxyd = {}
                it = 1
        return proxylist

xl = XroxyLib()
xl.print_lst(prefix='http://')
