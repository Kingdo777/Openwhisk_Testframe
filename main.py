# -*- coding: utf-8 -*-
import json
import os
import socket
import sys
import time
from urllib.request import urlopen
from zipfile import ZipFile

from utils import *

# 准备工作
zipped_code_path = make_zip_file('tmp.zip')

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
print(call_count, call_mode)

if call_mode == "same":
    for rId in range(1):
        func_name = "action" + str(int(time.time() * 1000))[-8:]
        fp = FuncOp(func_name)
        # 创建函数
        fp.create_function(zipped_code_path)
        # 调用函数
        send_request(fp, call_count, sync=True, rId=rId)
        # time.sleep((rId + 21) * 60)
        # 删除函数
        fp.delete_function()
else:
    create_trigger("trigger_test")
    for rId in range(call_count):
        func_name = "action" + str(rId)
        rule_name = "rule" + str(rId)
        fp = FuncOp(func_name)
        fp.create_function(zipped_code_path)
        fp.create_rule(rule_name, "trigger_test")
    fire_trigger("trigger_test")
    for rId in range(call_count):
        func_name = "action" + str(rId)
        rule_name = "rule" + str(rId)
        fp = FuncOp(func_name)
        fp.delete_function()
        fp.delete_rule(rule_name)
    delete_trigger("trigger_test")
