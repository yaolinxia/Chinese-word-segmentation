import re
import feature
import test
import train
import util

maxLength = 6
# 根据预处理标记切分法律文书
def seg_list(processed,content):
    list = []
    text = ""
    white_char = 0
    isNumber = False

    for i in range(0,len(processed)):
        character = processed[i]
        real_character = content[i-white_char]
        if character == '`':
            if text != "":
                if isNumber:
                    list.append((text,0))
                else:
                    list.append((text,1))
                isNumber = False
            list.append((real_character,0))
            text = ""
        elif character == '~':
            if isNumber:
                text += real_character
            else:
                if text != "":
                    list.append((text,1))
                text = real_character
            isNumber = True
        elif character == "/":
            white_char += 1
            list.append((text,0))
            isNumber = False
            text = ""
        else:
            if isNumber:
                list.append((text,0))
                text = real_character
            else:
                text += real_character
            isNumber = False
    if text != "":
        if not isNumber:
            list.append((text,1))
        else:
            list.append((text,0))
    return list

# 获得某一句话的pageRank得分
def get_data(string, data):
    array = {}
    for index in range(0, len(string) - 1):
        for word_len in range(2, min(maxLength + 1, len(string) - index + 1)):
            array[string[index:index + word_len]] = float(data[string[index:index + word_len]])
    return array

def write_segmentation(string, data,entrophies,mi_list,keywords):
    result = []
    if len(string) > 2:
        array = get_data(string, data)
        forward = forward_match(string,array,5)
        backward = backward_match(string,array,5)

        f_index = 0
        b_index = 0
        f_count = 0
        b_count = 0
        temp = ""
        while f_index < len(forward) and b_index < len(backward):
            f_word = forward[f_index]
            b_word = backward[b_index]
            if f_word == b_word:
                result.append(f_word)
                b_index += 1
                f_index += 1
            else:
                if f_count+len(f_word) > b_count+len(b_word):
                    b_index += 1
                    b_count += len(b_word)
                elif f_count+len(f_word) < b_count+len(b_word):
                    temp += f_word
                    f_index += 1
                    f_count += len(f_word)
                else:
                    temp += f_word
                        # 清空
                    write_max_match_array(temp,data,result)
                    temp = ""
                    f_count = 0
                    b_count = 0
                    f_index += 1
                    b_index += 1
    else:
        result.append(string)
    merge_term(result,entrophies,keywords)
    keyword = select_keyword(result,keywords,entrophies,mi_list,20)
    return result,keyword

# 合并与修正
def merge_term(seg,entrophies,keyword):
    e = 0.8
    length = len(seg)
    if(length<2):
        return
    i=0
    while i<length:
        word = seg[i]
        # 合并1字词
        if len(word) == 1:
            if i==0:
                next = seg[i+1]
                next_add = word+next
                next_add_right = entrophies[next_add]["右熵"]
                next_add_left = entrophies[next_add]["左熵"]
                if next_add_right+next_add_left > (entrophies[next]["左熵"] + entrophies[next]["右熵"])*e:
                    del(seg[i])
                    seg[i] = next_add
                    length -= 1
            elif i == length - 1:
                pre = seg[i-1]
                pre_add = pre+word
                pre_add_left = entrophies[pre_add]["左熵"]
                pre_add_right = entrophies[pre_add]["右熵"]
                if pre_add_left+pre_add_right > (entrophies[pre]["左熵"] + entrophies[pre]["右熵"])*e:
                    del(seg[i])
                    seg[i-1] = pre_add
                    length -= 1
            else:
                next = seg[i+1]
                next_add = word+next
                next_add_right = entrophies[next_add]["右熵"]
                next_add_left = entrophies[next_add]["左熵"]
                pre = seg[i-1]
                pre_add = pre+word
                pre_add_left = entrophies[pre_add]["左熵"]
                pre_add_right = entrophies[pre_add]["右熵"]
                if next_add_right+next_add_left > (entrophies[next]["左熵"] + entrophies[next]["右熵"])*e or pre_add_left+pre_add_right > (entrophies[pre]["左熵"] + entrophies[pre]["右熵"])*e:
                    # 向左合并
                    if pre_add_left+pre_add_right > next_add_right+next_add_left:
                        del(seg[i])
                        seg[i-1] = pre_add
                        length -= 1
                    # 向右合并
                    else:
                        del(seg[i])
                        seg[i] = next_add
                        length -= 1

        # 分裂2字词
        if len(word)==2 and i>0 and i < len(seg)-1:
            pre = seg[i-1]
            next = seg[i+1]
            if len(pre)==2 and len(next)==2:
                pre_add = pre + word[0]
                next_add = word[1] + next
                pre_add_left = entrophies[pre_add]["左熵"]
                pre_add_right = entrophies[pre_add]["右熵"]
                pre_left = entrophies[pre]["左熵"]
                pre_right = entrophies[pre]["右熵"]
                next_add_left = entrophies[next_add]["左熵"]
                next_add_right = entrophies[next_add]["右熵"]
                next_left = entrophies[next]["左熵"]
                next_right = entrophies[next]["右熵"]
                word_left = entrophies[word]["左熵"]
                word_right = entrophies[word]["右熵"]
                count = [pre_add_left,pre_add_right,next_add_left,next_add_right].count(0)
                if  pre_add_left+pre_add_right+next_add_left+next_add_right > (pre_left+pre_right+next_left+next_right +word_left+word_right):
                    seg[i-1] = pre_add
                    seg[i+1] = next_add
                    del(seg[i])
                    length -= 1
        i += 1
        # 合并长词
    merge_term_dic(seg,keyword)

    # 关键词抽取

# 关键词抽取
def select_keyword(seg,keywords,entrophies,mi_list,k):
    result = {}
    for word in seg:
        if len(word) > 1:
            result[word] = mi_list[word]+entrophies[word]['左熵']+entrophies[word]['右熵']*len(word)
    return result

# 辞典逆序合并
def merge_term_dic(seg,keyword):
    length = len(seg)
    if(length<2):
        return
    i=length - 1
    while i>0:
        word = seg[i]
        pre = seg[i-1]
        if pre+word in keyword:
            seg[i-1] = pre+word
            del(seg[i])
        i -= 1

def write_max_match_array(string,data,result):
    list = max_match(string,get_data(string,data))
    temp = string
    while(temp != ""):
        best_match = ""
        best_len = 0
        for word in list:
            if temp.find(word) == 0:
                if len(word) > best_len:
                    best_match = word
                    best_len = len(word)
        temp = temp.replace(best_match,'',1)
        # output.write(best_match+"/")
        result.append(best_match)

def find_max_word(array):
    word = max(array,key=lambda key:array[key])
    return word

def max_match(string,array):
    temp = string
    words = []
    array = dict(sorted(array.items(), key=lambda x: x[1], reverse=True))
    for key, value in array.items():
        if key in temp:
            words.append(key)
            temp = temp.replace(key, ' ')
    temp = re.sub(r'\s+', ' ', temp).strip(' ')
    characters = temp.split(' ')
    words.extend(characters)
    if '' in words:
        words.remove('')
    return words

def forward_match(string,array,window):
    temp = string
    words = []

    length = len(temp)
    index = 0

    while (index < length - 1):
        offset = min(window,length-index)
        temp_str = temp[index:index+offset]
        word = find_max_word(get_data(temp_str,array))
        begining = temp_str.find(word)
        if begining!=0:
            words.append(temp_str[0:begining])
        words.append(word)
        if begining+len(word) < offset:
            index += begining+len(word)
        else:
            index += offset
    if index == length - 1:
        words.append(temp[index])
    return words

def backward_match(string, array,window):
    temp = string
    words = []

    length = len(temp)
    index = length

    while (index > 1):
        offset = min(window,index)
        temp_str = temp[index-offset:index]
        word = find_max_word(get_data(temp_str,array))
        begining = temp_str.find(word)
        if begining+len(word) != offset:
            words.insert(0,temp_str[begining+len(word):offset])
        words.insert(0,word)
        if begining > 0:
            index -= offset-begining
        else:
            index -= offset
    if index == 1:
        words.insert(0,temp[0])
    return words

def substitute_word(list,string):
    result = string
    list.sort(key=lambda x:len(x),reverse=True)
    for item in list:
        temp = ""
        for i in range(0,len(item)):
            temp += "~"
        temp += "/"
        result = result.replace(item,temp)
    return result

def extract_word(dict):
    words = []
    for key in dict.keys():
        words.append(key)
    return words

def preprocess_content(content):
    processed = re.sub(
        r"[\.\^\$\*\+\?\{\}\[\]\\\|\(\);,/\'\"$#@!~`&\+：；‘“”’／=、）〈〉＊［］（……¥！～·】‰【「」？。，》《\s]",
        '`', content)
    processed = re.sub(r"[a-zA-Z]+[0-9×．\-%％]?",'~',processed)
    time_pattern = re.compile(r"[第]?[一二三四五六七八九十百千万亿〇零壹贰叁肆伍陆柒捌玖拾佰仟0-9]+[个]?[年月日天时分秒元]")
    statute_pattern = re.compile(r"第[一二三四五六七八九十百千万亿〇零壹贰叁肆伍陆柒捌玖拾佰仟0-9]+[条款项号]")

    time_words = time_pattern.findall(processed)
    statute_words = statute_pattern.findall(processed)

    processed = substitute_word(time_words,processed)
    processed = substitute_word(statute_words,processed)

    processed = re.sub(r"[0-9a-zA-Z×．\-%％]",'~',processed)
    return processed

def seg_output(s_list,output_file,data,entrophies,mi_list,keywords):
    seg = []
    keys = {}
    for text in s_list:
        if text[1] == 1:
            result,keyword = write_segmentation(text[0],data,entrophies,mi_list,keywords)
            seg += result
            keys = dict(keys,**keyword)
        else:
            seg.append(text[0])

    with open(output_file,"w") as output:
        output.write("/".join(seg))

    return seg,keys


def segment(text,keywords):
    output_file = "file/output.txt"
    maxLen = 6
    cycle = 10

    frequency,entrophies,mi_list = feature.calculate_features(text,maxLen)
    words = extract_word(entrophies)

    with open("file/feature.txt","w") as file:
        for i in range(0,len(words)):
            file.write(words[i]+"\t"+str(entrophies[words[i]])+"\t"+str(mi_list[words[i]])+"\n")

    data = train.pr_score(words, cycle, mi_list)

    content = text

    processed = preprocess_content(content)
    s_list = seg_list(processed,content)

    result,keyword = seg_output(s_list,output_file,data,entrophies,mi_list,keywords)
    keyword= sorted(keyword.items(), key=lambda d:d[1], reverse = True)
    return result,dict(keyword)

    # test.test(raw, output_file, test_file)
