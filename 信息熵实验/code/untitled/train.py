from time import time
import numpy as np

def read_file(path):
    features = []
    labels = []
    with open(path) as file:
        for line in file.readlines():
            list = []
            line = line.strip("\n")
            feature = line.split("\t")
            list.append(len(feature[0]))  # 字长
            list.append(float(feature[1]))  # 左熵
            list.append(float(feature[2]))  # 右熵
            list.append(float(feature[3]))  # 凝固程度
            features.append(list)
            labels.append(int(feature[4]))  # y值

    return features, labels

def read_word(path):
    words = []
    with open(path) as file:
        for line in file.readlines():
            list = []
            line = line.strip("\n")
            feature = line.split("\t")
            words.append(feature[0])

    return words

def count(test_label, predict_label):
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    coverage = 0

    for i in range(0, len(test_label)):
        t = test_label[i]
        p = predict_label[i]
        if p == 1 and t == 1:
            tp += 1
            coverage += 1
        elif t == 0 and p == 1:
            fp += 1
            coverage += 1
        elif t == 1 and p == 0:
            fn += 1
        else:
            tn += 1

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f = 2 * precision * recall / (precision + recall)
    coverage = coverage / len(test_label)
    print("precision:" + str(precision * 100) + "%")
    print("recall:" + str(recall * 100) + "%")
    print("f-value:" + str(f))
    print("coverage:" + str(coverage))

def pr_score(words,cycle,mi_list):
    big2small = 1
    small2big = np.mat(np.zeros(len(words)))

    t0 = time()

    num = len(words)
    score = np.mat(list(mi_list.values()))
    In = np.mat(np.zeros((num, num)))
    for i in range(0,num):
        word = words[i]
        n = len(word)
        if n>2:
            small2big[0,i] = 2/((n+1)*(n-2))
        for p in range(2,min(6,len(word))):
            for index in range(0,len(word)-p+1):
                string = word[index:index+p]
                j = words.index(string)
                In[j,i] = 1
    print("initialize finished:" + str(round(time() - t0, 3)), "s")
    t0 = time()

    for i in range(0,cycle):
        big_bonus = In*score.T*big2small
        small_bonus = np.multiply(score*In,small2big)
        score += big_bonus.T+small_bonus


    data = {}
    for i in range(0,len(words)):
        data[words[i]] = score[0,i]

    print("training finished:" + str(round(time() - t0, 3)), "s")

    return data