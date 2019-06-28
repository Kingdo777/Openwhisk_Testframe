#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

argv = sys.argv
argv_count = len(argv)
if argv_count < 2:
    call_mode = "same"
    call_count = 10
else:
    if argv_count < 3:
        call_mode = argv[1]
        call_count = 10
    else:
        call_mode = argv[1]
        call_count = argv[2]

print(call_count,call_mode)
