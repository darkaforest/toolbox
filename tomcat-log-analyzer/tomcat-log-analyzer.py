#!/usr/bin/env python

import fileinput
import sys
from sys import argv

print 'processing...'

maps = [{},{},{},{},{},{},{}]
errorItems = []

def fillMap(map, strs):
    if map.get(strs) is None:
        map[strs] = 1
    else:
        map[strs] = map[strs] + 1

def fillMaps(maps, ip, time, method, url, protocal, code, length):
    fillMap(maps[0], ip)
    fillMap(maps[1], time)
    fillMap(maps[2], method)
    fillMap(maps[3], url)
    fillMap(maps[4], protocal)
    fillMap(maps[5], code)
    fillMap(maps[6], length)

total = 0

for line in fileinput.input(argv[1]):
    data = line.split()
    try:
        #for particular record like : 192.168.1.111 - - [02/Mar/2019:19:41:41 +0800] "-" 400 2244
        if '+0800] "-" 400 2244' in line:
            fillMaps(maps, data[0], data[3][1:], 'null', "'-'", 'null', '400', '2244')
        else:
            fillMaps(maps, data[0], data[3][1:], data[5][1:], data[6], data[7], data[8], data[9])
    except IndexError:
        errorItems.append(line)
        continue
    total = total + 1

print 'warnning: only support default tomcat log currently'
print 'choose item to display: [ip]/[time]/[method]/[url]/[protocal]/[code]/[length]'

operMap = {'ip' : 0, 'time' : 1, 'method' : 2, 'url' : 3, 'protocal' : 4, 'code' : 5, 'length' : 6}

choose = raw_input().lower()

if operMap.get(choose) is None:
    print 'illegal input!'
    sys.exit()

for item in sorted(maps[operMap[choose]].items(), key = lambda d : d[1]):
    percent = float(item[1]) / total
    if percent < 0.0001:
        print '%s : tiny' % item[0]
    else:
        print '%s : %.2f%%' % (item[0], (percent) * 100)

if errorItems:
    print '\n\n---------------------------------------------------------------------'
    print 'following records can not be processed because of wrong format (%d)\n' % len(errorItems)
    for record in errorItems:
        print record.strip('\n')