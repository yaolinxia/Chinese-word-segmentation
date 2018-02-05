# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 19:21:47 2018
@author: ldk
"""
import xlrd
import codecs
import crf 

#change word likes   人民法院-n    to    人民法院
def getFormat1Word(word):
    split_word = word.split("-")
    return  split_word[0]

#change word likes   人民法院 5000 key    to    人民法院
def getFormat2Words(word):
    split_word = word.split(" ")
    return  split_word[0]

def getFormat1POS(word):
    split_word = word.split("-")
    return  split_word[1]

def get_krywords_from__excel(path):

    result_list=[]
#文件位置
    ExcelFile=xlrd.open_workbook(path)
    print (path)
    sheet=ExcelFile.sheet_by_name('民事大于50w')

#打印sheet的名称，行数，列数
    print (sheet.name)

#获取整行或者整列的值
    cols=sheet.col_values(3)#第二列内容
    cols_value = cols[1:len(cols)-1]
    
    for col in cols_value:
        entrys = col.split(",")
        for entry in entrys:
            keyword = entry.split("(")[0]  
            if keyword not in result_list:
                result_list.append(keyword)
               
    print(len(result_list))
    return result_list

def write_keywords_with_tag(keywords,path):
     output_data = codecs.open(path, 'w', 'utf-8')
     
     for keyword in keywords:
         
         output_data.write( crf.wordsTagging(keyword))
         output_data.write( "\r\n")
     
     output_data.close()
 