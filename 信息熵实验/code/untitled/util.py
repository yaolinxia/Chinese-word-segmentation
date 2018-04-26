import glob
import os
import xml.dom.minidom
#遍历某个文件夹下所有xml文件，path为存放xml的文件夹路径
def traversalDir_XMLFile(path):
    # 判断路径是否存在
    if(os.path.exists(path)):
        #用正则匹配得到该路径下的所有xml文件
        f = glob.glob(path + '/*.xml')
        text = ''
        for file in f:
            name = file.split("/")
            name = name[-1].split(".")
            name = name[0]
            print(name)
            dom = xml.dom.minidom.parse(file)
            values = dom.getElementsByTagName('QW')
            text = values[0].getAttribute('value')
            with open("/Users/nick/Documents/文件/毕业设计/文件/code/untitled/file/doc/unseg/"+name+".txt","w",encoding='utf-8') as output:
                output.write(text)

def float2percentage(score):
    percentage = float("%.2f" % (score*100))
    return str(percentage)+"%"

def load_dic(path):
    keywords = {}
    with open(path,"r") as dic:
        lines = dic.readlines()
        for line in lines:
            line = line.strip()
            keyword = line.split(" ")[0]
            count = int(line.split(" ")[1])
            keywords[keyword] = count
    return keywords

def load_keyword(path):
    keywords = []
    with open(path,"r") as dic:
        lines = dic.readlines()
        for line in lines:
            line = line.strip()
            keywords.append(line)
    return keywords


