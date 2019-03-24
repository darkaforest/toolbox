#!/usr/bin/env python

import fileinput
import sys
from sys import argv

print 'processing...'

maps = [{},{},{}]

def fillMap(map, strs):
    if map.get(strs) is None:
        map[strs] = 1
    else:
        map[strs] = map[strs] + 1

def fillMaps(maps, user, terminal, ip):
    fillMap(maps[0], user)
    fillMap(maps[1], terminal)
    fillMap(maps[2], ip)

total = 0

for line in fileinput.input(argv[1]):
    data = line.split()
    if len(data) != 10:
        continue
    try:
        fillMaps(maps, data[0], data[1], data[2])
        total += 1
    except IndexError:
        continue

print 'Centos7 lastb logs analyzer'
print 'choose item to display: [user]/[terminal]/[ip]'

operMap = {'user' : 0, 'terminal' : 1, 'ip' : 2 }

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