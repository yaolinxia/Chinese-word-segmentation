# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 18:24:18 2018

@author: ldk
"""
import codecs
import jieba.posseg as pseg

import formator
import analyse

def crfTagging(input_file, output_file):

    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    
    for line in input_data.readlines():
        formated_words = formator.getFormat2Words(line)       
        output_data.write( wordsTagging(formated_words)) 
        
        output_data.write("\r\n")
    
    input_data.close()
    output_data.close()

# tag word likes 人民法院 to 人 B      民M       法 M            院E
def wordTagging(word):
    
    result=""
    word_POS = ""
    
    if len(word) == 1:
        result = word +  word_POS + "\tS\r\n"
    else:
        result = word[0] +  word_POS + "\tB\r\n"
        for w in word[1:len(word)-1]:
            result += w +  word_POS + "\tM\r\n"
        result += word[len(word)-1] + word_POS +  "\tE\r\n"
                
    return result

# tag word likes 人民法院 to 人民 B-N      法院E-N
def wordsTagging(formated_words):
    
#   print(formated_words)
    result=""
    temp = ""
    words = pseg.cut(formated_words)

    for word , flag in words:
        temp += word+" "+flag+"e"
    pairs = temp.split("e")
    
    size = len(pairs) -1
    if(size==1):
        splited_pair = pairs[0].split(" ")
        word = splited_pair[0]
        flag = splited_pair[1].upper()
        result = word + "\tS-" + flag +"\r\n"
    else: 
        splited_pair = pairs[0].split(" ")
        word = splited_pair[0]
        flag = splited_pair[1].upper()
        result = word + "\tB-" + flag +"\r\n"
        for pair in pairs[1:size-1]:
            splited_pair = pair.split(" ")
            word = splited_pair[0]
            flag = splited_pair[1].upper()
            result += word + "\tI-" + flag +"\r\n"
        splited_pair = pairs[size-1].split(" ")
        word = splited_pair[0]
        flag = splited_pair[1].upper()
     
        result += word + "\tE-" + flag +"\r\n"

        
    return result


         
'''
import CRFPP

def crf_segmenter(input_file, output_file, tagger):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        tagger.clear()
        for word in line.strip():
            word = word.strip()
            if word:
                tagger.add((word + "\to\tB").encode('utf-8'))
                tagger.parse()
                size = tagger.size()
                xsize = tagger.xsize()
                for i in range(0, size):
                    for j in range(0, xsize):
                        char = tagger.x(i, j).decode('utf-8')
                        tag = tagger.y2(i)
                        if tag == 'B':
                            output_data.write(' ' + char)
                        elif tag == 'M':
                            output_data.write(char)
                        elif tag == 'E':
                            output_data.write(char + ' ')
                        else: # tag == 'S'
                            output_data.write(' ' + char + ' ')
                        output_data.write('\n')
    input_data.close()
    output_data.close()
 '''

if __name__ == '__main__':

    #test_keywords = formator.get_krywords_from__excel(r'E:\python_workspace\Chinese-word-segmentation\条件随机场\TestResult\案由 关键词统计表 20180105v2.xlsx')
    #formator.write_keywords_with_tag(test_keywords,r'E:\python_workspace\Chinese-word-segmentation\条件随机场\testResult_0321\judge_keywords挑选案由.txt')
    precise = analyse.caculate_precise_byfile(
        r'E:\python_workspace\Chinese-word-segmentation\条件随机场\testResult_0321\test_result_0331.txt.utf8')
    print(precise)
