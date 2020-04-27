#!/usr/bin/env python
import os
import sys

def rec():
    for sub in os.listdir('.'):
        if os.path.isdir(sub):
            os.chdir(sub)
            rec()
            os.chdir('..')
        else:
            global count
            count += 1
            print os.path.abspath(sub)

os.chdir(sys.argv[1])
global count
count = 0
rec()
print 'Total Files:', count
