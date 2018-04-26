import preprocess as pre
import mutual_information as mi
import information_entrophy_raw_text as ie
from time import time
# 计数器
class Counter(dict):
    def __missing__(self, key):
         return 0

# 计算每个不超过k的词的词频，返回总词数
def calculate_frequency(frequency,strings):
    total_num = 0
    ind = 1
    total = len(strings)
    maxLength = 6
    for string in strings:
        for i in range(1,min(maxLength+1,len(string)+1)):
            for index in range(0,len(string)-i+1):
                frequency[string[index:index+i]] += 1
                total_num += 1
        ind += 1
    return total_num

# 存储频率
def save_frequency(frequency,total,frequency_path):
    with open(frequency_path+".txt","w") as file:
        for key,value in frequency.items():
            file.write(key+" "+str(value/total)+"\n")

    with open(frequency_path+"_total.txt","w") as f:
        f.write(str(total))

def read_frequency(frequency_path):
    with open(frequency_path+"_total.txt","r") as f:
        total = f.read()
        total = int(total)
    list = {}

    with open(frequency_path+".txt","r") as file:
        strings = file.readlines()

    for string in strings:
        string = string.split(" ")
        key = string[0]
        value = float(string[1])
        list[key] = value
    return list


def save_data(entrophies,mi_list,path):
    with open(path,"w") as file:
        for key,value in entrophies.items():
            word_name = key
            mutual_information = mi_list[word_name]
            left_entrophy = value["左熵"]
            right_entrophy = value["右熵"]
            file.write(word_name+"\t"+str(left_entrophy)+"\t"+str(right_entrophy)+"\t"+str(mutual_information)+"\n")

def frequency2Frequency(frequency,total):
    for key,value in frequency.items():
        frequency[key] = value/total

# 输入文章路径进行分词
def calculate_features(text,maxLen):
    frequency = Counter()

    t0 = time()
    content = text

    strings = pre.cut_sentence(content)
    total = calculate_frequency(frequency,strings)

    frequency2Frequency(frequency,total)

    entrophies = ie.getEntrophy(strings,maxLen)
    mi_list = mi.calculate(frequency)

    print("feature finished:" + str(round(time() - t0, 3)), "s")
    return [frequency,entrophies,mi_list]
