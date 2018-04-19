#!/usr/bin/env python
# _*_ coding:utf-8 _*_

#1.先分好词，存在一个字符数组里面
#2.遍历字符数组，然后遍历停用词数组，在停用词数组里面的，不保留，不在的就存下来
import sys
import glob
import os
import xml.dom.minidom
import jieba

#添加自定义词典userdict.txt
jieba.load_userdict(u'E:\python_workspace\Chinese-word-segmentation\CWS_1-12\\userdict.txt')
jieba.load_userdict(u'E:\python_workspace\\test-path\DicOutput\\minshi.txt')
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

#读取path下的文件
def read_txt(path):
    f=open(path, 'r', encoding='utf-8')
    text=f.read()
    return text

#对文章text进行分词

#停用词路径
def stopwordlist(path):
    stopwords = [line.strip() for line in open(path,'r',encoding='utf-8').readlines()]
    return stopwords

#分词path:指定停用词路径，text:要分词的文本
#cut_all=True全模式
#cut_all=False全模式
def segment(text,stopwordsPath):
    textCut=jieba.cut(text,cut_all=False)
    stopwords=stopwordlist(stopwordsPath)
    result=''
    for w in textCut:
        if w not in stopwords:
            if w!='\t':
                result+=w+' '
    print('sucess segment')
    return result

#将text内容写入进path路径中
def write_segmentFile(path,text):
    f=open(path,'w',encoding='utf-8')
    f.write(text)
    f.close()
    print('success')

if __name__=='__main__':
    path1 = r'E:\python_workspace\WenShu_Test'
    path2 = r'E:\python_workspace\test-path\test_dic_0419.txt'
    path5 = r'E:\python_workspace\test-path\test_dicSeg_0419.txt'
    path3 = r'E:\python_workspace\Chinese-word-segmentation\CWS_1-12\\stopword.dic'
    #path4=r'C:\Users\LFK\Desktop\1.txt'
    text=read_XMLFile(path1)
    #提取文书内容，写到path2中
    write_segmentFile(path5, text)
    # text=read_txt(path4)
    result=segment(text,path3)
    write_segmentFile(path2,result)

