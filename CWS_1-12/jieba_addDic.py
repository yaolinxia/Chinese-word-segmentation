#!/usr/bin/env python
# _*_ coding:utf-8 _*_

#1.先分好词，存在一个字符数组里面
#2.遍历字符数组，然后遍历停用词数组，在停用词数组里面的，不保留，不在的就存下来
import sys
import glob
import os
import xml.dom.minidom
import jieba

jieba.load_userdict(u'E:\YanJiuSheng-download\\1a\python3.6.1\Lib\site-packages\jieba\\userdict.txt')
#遍历某个文件夹下所有xml文件，path为存放xml的文件夹路径
def read_XMLFile(path):
    # 判断路径是否存在
    n=0
    if(os.path.exists(path)):
        #用正则匹配得到该路径下的所有xml文件
        f = glob.glob(path + '\\*.xml')
        text = ''
        for file in f:
            n=n+1
            print(str(n) + ":" + file)
            #print(file)
            # 打开xml文档
            try:
                dom = xml.dom.minidom.parse(file)
                values = dom.getElementsByTagName('QW')
                text += values[0].getAttribute('value')
            except:
                continue
            #print(text)
        return text

def read_txt(path):


    f=open(path,'r',encoding='utf-8')
    text=f.read()
    return text

#对文章text进行分词

def stopwordlist(path):
    stopwords=[line.strip() for line in open(path,'r',encoding='utf-8').readlines()]
    return stopwords

def segment(text,path):
    textCut=jieba.cut(text,cut_all=True)
    stopwords=stopwordlist(path)
    result=''
    for w in textCut:
        if w not in stopwords:
            if w!='\t':
                result+=w+' '
    print('sucess segment')
    return result

def write_segmentFile(path,text):
    f=open(path,'w',encoding='utf-8')
    f.write(text)
    f.close()
    print('success')

if __name__=='__main__':
    path1=r'G:\研究生\法律文书\刑事一审文书测试集 (2)'
    path2=r'H:\python-workspace\1-11-testWenShu\TestResult\\test_QW_addDic.txt'
    path3=r'H:\python-workspace\\1-5-testWenShu\\stopword.dic'
    #path4=r'C:\Users\LFK\Desktop\1.txt'
    text=read_XMLFile(path1)
    # text=read_txt(path4)
    result=segment(text,path3)
    write_segmentFile(path2,result)

