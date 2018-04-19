# -*- coding:utf-8 -*-
import json

with open("testJson.json", encoding='utf-8') as f:
    #将json转化为字典
    temp = json.loads(f.read())
    print(temp)
    len1 = len(temp)
    i = 0
    print(len(temp))
    while i < len1:
        for case in temp:

            print(case['name'] +' '+ str(case['count']))
        i += 1

    #print(temp['id']+' '+temp['name'])
    #print(temp['name'])
    #print(temp['rule']['namespace'])