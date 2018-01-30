#!/usr/bin/env python
# _*_ coding:utf-8 _*_

#1.先分好词，存在一个字符数组里面
#2.遍历字符数组，进行词性标注
import sys
import glob
import os
import xml.dom.minidom
import jieba
import jieba.posseg as pseg
#遍历某个文件夹下所有xml文件，path为存放xml的文件夹路径

#词性标注
def WorkMark(path):
    #textCut=jieba.cut(text,cut_all=False)
    #词性标注
    with open(path, encoding="utf-8") as file_object:
        contents = file_object.read()
    textCut = pseg.cut(contents)
    for ele in textCut:
        print(ele)

    result = ''
    for word in textCut:
        result +=word+' '
        print('%s' % (word))

    print('sucess WorkMark')

    return result

#路径path下的内容写入进text中
def write_WorkMark(path,text):
    f=open(path,'w',encoding='utf-8')
    f.write(text)
    f.close()
    print('success write_WorkMark')

if __name__=='__main__':
    #path1 = r'G:\研究生\法律文书\民事一审测试集\民事一审测试集'
    #输出的结果路径
    path2 = r'H:\python-workspace\test-path\test_QW_1-29.txt'
    #path3 = r'H:\python-workspace\\1-5-testWenShu\\stopword.dic'
    #path4:提取的字段路径
    path4 = r'H:\python-workspace\1-12-testWenShu\test_QW_addDic.txt'
    #path4=r'C:\Users\LFK\Desktop\1.txt'
    #text = read_XMLFile(path1)

    #write_segmentFile(path4, text)
    # text=read_txt(path4)
    result = WorkMark(path4)
    write_WorkMark(path2,result)


"""
import jieba.posseg as pseg
words = pseg.cut("我爱北京天安门")
for word,flag in words:
    print('%s %s' % (word, flag))
"""