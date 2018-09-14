# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 20:18:54 2018

@author: ldk
"""

import codecs

#计算精确度
def caculate_precise_byfile(path):

    size = 0
    correct_size = 0
    
    input_data = codecs.open(path, 'r', 'utf-8',errors='ignore')
    for aline in input_data.readlines():
       
   
        if(len(aline)>5):
            line = aline.splitlines(False)
            print(line)
            cols = line[0].split("\t")

            if(len(cols)>2):
                preference = cols[1]
                test = cols[2]
            if(test == preference):
                correct_size += 1
            size += 1

        print(size)
    return correct_size/size
        