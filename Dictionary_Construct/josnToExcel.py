# -*- coding:utf-8 -*-
import json
import xlwt

workbook = xlwt.Workbook(encoding='ascii')
worksheet = workbook.add_sheet('My Worksheet')

with open("testJson3.json", encoding='utf-8') as f:
    #将json转化为字典

    temp = json.loads(f.read())
    print(temp)
    len1 = len(temp)
    i = 0
    print(len(temp))
    j = 0
    while i < len1:
        for case in temp:
            if j < len1*len(case):
                print(case['name'] + ' ' + str(case['count']))
                worksheet.write(j, 0, label=case['name'])
                worksheet.write(j, 1, label=case['count'])
                j += 1
            else:
                break
        i += 1
    workbook.save('Excel_Workbook1.xls')