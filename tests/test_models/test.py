#!/usr/bin/python3

import re
string = '2017-09-28T21:03:54.052302'
arr = re.split(':|-|T', string)
sec = arr[-1].split('.')
arr.remove(arr[-1])
arr.extend(sec)
print(arr)
print(sec)
