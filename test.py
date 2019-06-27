import json
import os
import subprocess

test = 'ok: invoked /_/test26690631 with id 0038642c8d4641ebb8642c8d4671eb17{\"activationId\":\"0038642c8d4641ebb8642c8d4671eb17\",\"annotations\":[{\"key\":\"path\",\"value\":\"guest/test26690631\"},{\"key\":\"waitTime\",\"value\":1080},{\"key\":\"kind\",\"value\":\"python:3\"},{\"key\":\"timeout\",\"value\":false},{\"key\":\"limits\",\"value\":{\"concurrency\":1,\"logs\":10,\"memory\":128,\"timeout\":60000}},{\"key\":\"initTime\",\"value\":310}],\"duration\":312,\"end\":1561626692176,\"logs\":[],\"name\":\"test26690631\",\"namespace\":\"guest\",\"publish\":false,\"response\":{\"result\":{\"greeting\":\"Hello stranger!\"},\"status\":\"success\",\"success\":true},\"start\":1561626691864,\"subject\":\"guest\",\"version\":\"0.0.1\"}'
print(json.loads(test[68:])['start'])