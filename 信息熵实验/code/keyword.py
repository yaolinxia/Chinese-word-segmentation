import os
import jieba.analyse

rootdir = '/Users/nick/Documents/文件/毕业设计/文件/code/untitled/file/doc/unseg'
list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
text = ""
for i in range(0,len(list)):
    path = os.path.join(rootdir,list[i])
    if os.path.isfile(path):
        with open(path,"r",encoding='utf-8') as file:
            content = file.read()
            text += content
keywords = jieba.analyse.extract_tags(text,topK=100000,allowPOS=('n'))
with open("keyword.txt","w",encoding='utf-8') as output:
    for i in range(0,len(keywords)):
        keyword = keywords[i]
        print(i/len(keywords)*100)
        output.write(keyword+"\n")