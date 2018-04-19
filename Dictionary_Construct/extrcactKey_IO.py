import os
import json
import xlwt


# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath,outpath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        print(child)
        #writeToExcel(child)
        writeTotxt(child, outpath)

        # extractKey(child)
        # readFile(child)
        # print(child.decode('gbk'))
        # .decode('gbk')是解决中文显示乱码问题

# 读取文件内容并打印
def readFile(filename):
    fopen = open(filename, 'r', encoding='utf-8')  # r 代表read
    for eachLine in fopen:
        print("读取到得内容如下：", eachLine)

    fopen.close()
    return eachLine


# 读取json文件，并且提取出其中错所需的内容
def extractKey(jsonName):
    with open(jsonName, encoding='utf-8') as f:
        # 将json转化为字典
        temp = json.loads(f.read())
        print(temp)
        len1 = len(temp)
        i = 0
        print(len(temp))
        while i < len1:
            for case in temp:
                print(case['name'] + ' ' + str(case['count']))
            i += 1


# 写文件
def writeToExcel(fileName):
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet("fileName")

    with open(fileName, encoding='utf-8') as f:
        # 将json转化为字典
        temp = json.loads(f.read())
        print(temp)
        len1 = len(temp)
        i = 0
        print(len(temp))
        j = 0
        while i < len1:
            for case in temp:
                if j < len1 * len(case):
                    print(case['name'] + ' ' + str(case['count']))
                    worksheet.write(j, 0, label=case['name'])
                    worksheet.write(j, 1, label=case['count'])
                    j += 1
                else:
                    break
            i += 1
        workbook.save('judgement documents.xls')


# 获取文件夹中的名称eg:案由名称
def extractCaseName(path,caseName):
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet(caseName)
    #path = 'E:\法律文书集\\20180410_无讼_案由关键词频数集\\20180410_无讼_案由关键词频数集\\01_刑事案由_关键词_频数表'
    # path = 'E:\python_workspace\WenShu_Test'
    print(os.listdir(path))
    j = 0
    for case in os.listdir(path):
        print(os.listdir(path)[j])
        print('=======================================')
        worksheet.write(j, 0, label=os.listdir(path)[j])
        j += 1
        print(j)
    workbook.save('Judgment_documents0418.xls')

#将文书提取出来放在txt文本中，提取我们所需要的内容
def writeTotxt(fileName, outputFile):
    with open(fileName, encoding='utf-8') as f:
        #将json转化为字典
        temp = json.loads(f.read())
        print(temp)

        len1 = len(temp)
        i = 0
        print(len(temp))
        fopen = open(outputFile, 'a')
        while i < len1:
            for case in temp:
                print(case['name'] + ' ' + str(case['count']))
                #with open("testWrite.txt", 'w', encoding='utf-8') as f2:
                fopen.write(case['name']+' ')
                fopen.write(str(case['count'])+ ' ')
                fopen.write('key')
                fopen.write('\n')
            i += 1

if __name__ == '__main__':
    filePath = "E:\python_workspace\WenShu_Test\\"
    filePathI = "E:\python_workspace\\test-path\\testRead.txt"
    filePathI02 = "E:\python_workspace\WenShu_Test\C__Users_Administrator_Desktop_民事二审案件_民事二审案件_47.xml"
    filePath_xingshi = "E:\法律文书集\\20180410_无讼_案由关键词频数集\\20180410_无讼_案由关键词频数集\\01_刑事案由_关键词_频数表\\"
    filePath_minshi = "E:\法律文书集\\20180410_无讼_案由关键词频数集\\20180410_无讼_案由关键词频数集\\02_民事案由_关键词_频数表\\"
    filePath_xingzhen = "E:\法律文书集\\20180410_无讼_案由关键词频数集\\20180410_无讼_案由关键词频数集\\03_行政案由_关键词_频数表\\"
    filePath_peichang = "E:\法律文书集\\20180410_无讼_案由关键词频数集\\20180410_无讼_案由关键词频数集\\04_赔偿案由_关键词_频数表\\"
    filePath_zhixing = "E:\法律文书集\\20180410_无讼_案由关键词频数集\\20180410_无讼_案由关键词频数集\\05_执行案由_关键词_频数表\\"

    filePath_Json02 = "E:\python_workspace\Chinese-word-segmentation\Dictionary_Construct\\testJson.json"

    xingshiDic_outPut = "E:\python_workspace\\test-path\DicOutput\\xingshiDic.txt"
    minshi_outPut = "E:\python_workspace\\test-path\DicOutput\\minshi.txt"
    xingzhen_outPut = "E:\python_workspace\\test-path\DicOutput\\xingzhen.txt"
    peichang_outPut = "E:\python_workspace\\test-path\DicOutput\\peichang.txt"
    zhixing_outPut = "E:\python_workspace\\test-path\DicOutput\\zhixing.txt"

    # jsonFile = "E:\python_workspace\Chinese-word-segmentation\Dictionary_Construct\\testJson.json"
    # filePathC = "C:\\"
    eachFile(filePath_xingshi, xingshiDic_outPut)
    eachFile(filePath_minshi, minshi_outPut)
    eachFile(filePath_xingzhen, xingzhen_outPut)
    eachFile(filePath_peichang, peichang_outPut)
    eachFile(filePath_zhixing, zhixing_outPut)
    #writeTotxt(filePath_Json02, zhixing_outPut)
    #extractCaseName(filePath_Json, "01_刑事案由")
    # writeToExcel(filePath_Json02)
    # extractKey(jsonFile)
    # print(child01)
    # readFile(filePathI)
    # readFile(filePathI02)
    # writeFile(filePathI)
