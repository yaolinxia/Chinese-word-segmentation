# -*- coding:utf-8 -*-
import json

with open("testJson3.json", encoding='utf-8') as f:
    #将json转化为字典
    temp = json.loads(f.read())
    print(temp)

    len1 = len(temp)
    i = 0
    print(len(temp))
    fopen = open("testWrite.txt", 'w')
    while i < len1:
        for case in temp:
            print(case['name'] + ' ' + str(case['count']))
            #with open("testWrite.txt", 'w', encoding='utf-8') as f2:
            fopen.write(case['name']+' ')
            fopen.write(str(case['count']))
            fopen.write('\n')
        i += 1

    #print(temp['id']+' '+temp['name'])
    #print(temp['name'])
    #print(temp['rule']['namespace'])