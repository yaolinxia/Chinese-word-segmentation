#!/usr/bin/env python
# _*_ coding:utf-8 _*_


f = open("H:\python-workspace\\test-path\\test_QW_1-24.txt",encoding="utf-8");
count = {}
for line in f:
    line = line.strip()
    words = line.split(" ")
    for word in words:
        if word in count:
            count[word] +=1
        else:
            count[word] = 1

word_freq = []
#遍历字典转换为元组
for word,freq in count.items():
    word_freq.append((freq,word));
word_freq.sort(reverse = True);
#遍历前十个输出
for word,freq in word_freq:

    print(word,freq)