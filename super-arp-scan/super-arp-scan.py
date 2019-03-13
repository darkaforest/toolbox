#!/usr/bin/env python
# _*_ coding: utf_8 _*_
import os
import commands
import re
import subprocess
import socket
import struct
import time
from scapy.all import *

#conf file that recoeded mac2map
mac2name_file = "./oui.txt"

#a map from mac address to hardware name
mac2name = {}

#a map from mac address to ip address
mac2ip = {}

#mac frame for ARP and Ether
mac_src = "00:00:00:00:00:01"
mac_dst = "ff:ff:ff:ff:ff:ff"

#ip frame for ARP
ip_src = ""
ip_dst = ""

def ans_cmp(x, y):
    if x.psrc > y.psrc:
        return 1
    if x.psrc < y.psrc:
        return -1
    return 0

def genAddrsFromChoose(oper):
    if (oper == "1"):
        return ["192.168.1.%d" % ip4 for ip4 in range(1, 255)]
    elif (oper == "2"):
        return ["192.168.0.%d" % ip4 for ip4 in range(1, 255)]
    elif (oper == "3"):
        return ["192.168.31.%d" % ip4 for ip4 in range(1, 255)]
    else:
        return None

def oper(oper, mip = None, mmac = None, ip3 = None):
    time_start = time.time()
    anslist = []
    addr = Ether() / ARP()
    addr.pdst = genAddrsFromChoose(oper)
    if addr.pdst is None:
        print "非法输入!"
        return
    if mip != None:
        addr.src = mac_src
    if mmac != None:
        addr.hwsrc = mac_src
    addr.dst = mac_dst
    addr.hwdst = mac_dst
    addr.op = "who-has"
    os.system("clear")
    print "正在扫描...\n视网络状况不同，可能花费较长时间"
    p = srp(addr, timeout = 0.001, retry = 0, verbose = False)
    ans, unans = p[0], p[1]
    if len(ans) != 0:
        for x in ans:
            anslist.append(x[1])
    os.system("clear")
    print "IP Addr\t\tMAC Addr\t\tHost Name"
    time_end = time.time()
    anslist = sorted(anslist, ans_cmp)
    for isat in anslist:
        psrc = isat.psrc
        hwsrc = isat.hwsrc.upper()
        name = "%s-%s-%s" % (hwsrc[0:2], hwsrc[3:5], hwsrc[6:8])
        print "%s\t%s\t%s" % (psrc, hwsrc, mac2name.get(name, "Unknown"))
    print "_________________________________"
    print "%d hosts found in %.2f seconds" % (len(anslist), time_end - time_start)

def init():
    if not os.path.exists(mac2name_file):
        print "oui.txt not exists, can't do map from mac to name!"
        return
    with open(mac2name_file, "r") as conf_file:
        lines = conf_file.readlines()
    for line in lines:
        line = line.strip()
        str_group = line.split(" ", 1)
        mac2name[str_group[0]] = str_group[1]

if __name__ == "__main__":
    init()
    print "choose network type : \n"
    print "    1) tp-link 默认家用 (192.168.1.0/24)"
    print "    2) tp-link 默认家用 (与网关冲突时) (192.168.0.0、24)"
    print "    3) mi 默认家用 (192.168.31/24)"
    choose = raw_input()
    oper(choose)
