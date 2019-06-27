# -*- coding: utf-8 -*-
import json
import os
import socket
import time
from urllib.request import urlopen
from zipfile import ZipFile

from utils import *

# 准备工作
zipped_code_path = make_zip_file('tmp.zip')

for rId in range(1):
    func_name = "test" + str(int(time.time() * 1000))[-8:]
    fp = FuncOp(func_name)
    # 创建函数
    fp.create_function(zipped_code_path)
    # 调用函数
    send_request(fp, 10, sync=True, rId=rId)
    # time.sleep((rId + 21) * 60)
    # 删除函数
    fp.delete_function()
