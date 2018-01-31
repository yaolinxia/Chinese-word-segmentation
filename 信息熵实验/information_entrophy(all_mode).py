import information_entrophy as ie

# TODO 如“被判-判处”-->“被判处”的格式
def find_left_word(word_list,index):
	i = index
	name = word_list[i]
	i -= 1
	
	while word_list[i] in name:
		if name.find(word_list[i]) == 0:
			return find_left_word(word_list,i)
		else:
			i -= 1

	if name in word_list[i]:
		temp = word_list[i].find(name)
		return word_list[i][temp-1]
	elif name[0] == word_list[i][-1]:
		return word_list[i][-2]
	else:
		return word_list[i][-1]

def find_right_word(word_list,index):
	i = index
	name = word_list[i]
	i += 1

	while word_list[i] in name:
		if name.find(word_list[i])+len(word_list) == len(name):
			return find_right_word(word_list,i)
		else:
			i += 1

	if name in word_list[i]:
		temp = word_list[i].find(name)
		if len(word_list[i]) <= len(name) + temp:
			return word_list[i][0]
		else:
			return word_list[i][temp+len(name)]
	elif name[-1] == word_list[i][0]:
		return word_list[i][1]
	else:
		return word_list[i][0]




#   ------------------------------------------------------------------------------   #
#					         基于jieba全模式分词统计词的信息熵							 #
#								一词一行，词与词性用"\"分割   							 #
#				PS:分词模式不同导致数据格式不同，除数据处理其他计算函数并无区别   			 #
#   ------------------------------------------------------------------------------   #
if __name__ == '__main__':
	path = "10000+test_QW_1-29.txt"	#数据文件路径
	frequency = ie.Counter()		#频数词典
	total = 0					#总频数
	neighbors = {}				#临近字
	entrophies = {}				#每个词的信息熵
	left = {}					#左熵区间
	right = {}					#右熵区间
	words = []					#储存已经读过的词

	#读文件
	with open(path,"r") as divide:
		lines = divide.readlines()

	# 存储词
	for line in lines:
		if line != "\n" and line[0] != "/":			#去除空行和无意义行
			name = line.split("/")[0]
			words.append(name)
	
	for i in range(0,len(words)):
		name = words[i]
		if len(name) > 1:						#去除单个的词
			frequency[name] += 1
			total += 1
			if name not in neighbors.keys():
				neighbors[name] = ie.NearestWord(name)
			neighbor = neighbors[name]

			#左临近字
			left_word = find_left_word(words,i)
			neighbor.add_left(left_word)
			#右临近字
			right_word = find_right_word(words,i)
			neighbor.add_right(right_word)

	ie.save_data("result/10000",neighbors,entrophies,left,right)