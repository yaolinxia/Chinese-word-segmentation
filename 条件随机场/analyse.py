# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 20:18:54 2018

@author: ldk
"""

import codecs


def caculate_precise_byfile(path):
    
   
    size = 0
    correct_size = 0
    
    input_data = codecs.open(path, 'r', 'utf-8' ,errors='ignore')
    for aline in input_data.readlines():
       
   
        if(len(aline)>3):
            line = aline.splitlines(False)
         
            cols = line[0].split("\t")
         
            preference = cols[1]
            test = cols[2]
            if(test == preference):
                correct_size += 1
            size += 1
        
    return correct_size/size
        