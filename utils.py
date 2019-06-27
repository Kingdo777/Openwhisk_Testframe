# -*- coding: utf-8 -*-
import decimal
import json
import os
import time
from threading import Thread
from zipfile import ZipFile


def fstr(f):
    """
    Convert a float number to string
    """

    ctx = decimal.Context()
    ctx.prec = 20
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')


def fix_str_len(string, length):
    """
    限定字符串的长度，不足则补全空格，超过则裁剪
    :param string: 要操作的字符串
    :param length: 要固定的字符串的长度
    :return: 返回限定好长度的字符串
    """
    string_len = len(string)
    if string_len < length:
        string += " " * (length - string_len)
    else:
        string = string[0:length]
    return string


def make_zip_file(zip_filename):
    """
    生成上传到AWS的压缩文件
    :return:
    """
    with ZipFile(zip_filename, 'w') as myzip:
        for root, dirs, files in os.walk("code"):
            for file in files:
                abs_path = os.path.join(root, file)
                file = abs_path[5:]
                myzip.write(abs_path, file)  # 第一个参数是绝对路径，第二个参数是命名再压缩文件中的命名，也就是砍掉多余的路径
    return os.path.join(os.getcwd(), zip_filename)


def send_request(fp, task_num, sync, rId):
    """
    发起调用请求
    :param
        task_num: 并发度
        fp: FuncOp对象
        sync:是否同步发起调用请求
        rId:roundId
    :return:
    """

    def invoke_func(rId, sub_rId):
        # tm_st = time.time() * 1000
        tm_st, tm_end, respond = fp.invoke_function()
        # tm_end = time.time() * 1000
        tm_invoke = fix_str_len(fstr(tm_end - tm_st), 18)
        tm_st = fix_str_len(fstr(tm_st), 18)
        tm_end = fix_str_len(fstr(tm_end), 18)
        with open("logfile", "a+") as f:
            f.write(str(rId) + "-" +
                    fix_str_len(str(sub_rId), 2) + "-" +
                    fp.action_name +
                    ":" +
                    tm_st + "#" +
                    tm_end + "#" +
                    tm_invoke + "#" +
                    str(respond)
                    + "\n")

    list_task = []
    for i in range(task_num):
        t = Thread(target=invoke_func, args=(rId, i))
        t.start()
        if sync:
            list_task.append(t)
        else:
            t.join()
    for t in list_task:
        t.join()


def wsk(cmd):
    print(cmd)
    return os.popen("wsk " + cmd).read().strip("\n")


def create_trigger(trigger_name):
    wsk("-i trigger create " + trigger_name)


def fire_trigger(trigger_name):
    wsk("-i trigger fire " + trigger_name)


def delete_trigger(trigger_name):
    wsk("-i trigger delete " + trigger_name)


class FuncOp:
    def __init__(self,
                 action_name):
        self.action_name = action_name

    def dump_meta(self):
        """
        The basic information to record
        """
        return "{}".format(
            self.action_name)

    def delete_function(self):
        try:
            wsk(" action delete " + self.action_name + " -i")
            print("successfully delete function：" + self.action_name)
            return True
        except Exception as e:
            print("wrongly delete function：" + self.action_name)
            print(str(e))
            return False

    def create_function(self, src_file):
        """
        Create a new function
        :param src_file: 要上传的在lambda上执行的代码，是一个压缩的zip文件
        :return:
        """
        try:
            wsk("action create " + self.action_name + " --kind python:3  -m 128 -i " + src_file)
            print("successfully create function：" + self.action_name)
            return True
        except Exception as e:
            print("wrongly create function：" + self.action_name)
            print(str(e))
            return False

    def invoke_function(self):
        try:
            tm_st = time.time() * 1000
            resp = wsk("action invoke " + self.action_name + " -bi ")
            tm_end = time.time() * 1000
            resp = resp[69:]
            resp = json.loads(resp)
            try:
                resp = "{}#{}#{}".format(resp["start"], resp["end"], resp["duration"])
            except Exception as e:
                print(str(e), resp)
            if not resp:
                resp = "ERROR"
            out = "{}#{}".format(self.dump_meta(), resp)
            print("successfully invoke function：" + self.action_name)
            return tm_st, tm_end, out
        except Exception as e:
            print("wrongly invoke function：" + self.action_name)
            print(e)
            return False

    def create_rule(self, rule_name, trigger_name):
        wsk("-i rule create " + rule_name + " " + trigger_name + " " + self.action_name)

    @staticmethod
    def delete_rule(rule_name):
        wsk("-i rule delete " + rule_name)
