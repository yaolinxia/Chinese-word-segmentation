import math
import json
import operator

# 计数器
class Counter(dict):
    def __missing__(self, key):
         return 0

# 临近字统计
class NearestWord(object):
	def __init__(self,name):
		self.left = Counter()
		self.right = Counter()
		self.name = name
		self.total_left = 0
		self.total_right = 0

	def add_left(self,name):
		self.left[name] += 1
		self.total_left +=1

	def add_right(self,name):
		self.right[name] += 1
		self.total_right += 1


# 计算信息熵
def calculate_entrophy(neighbors,total):
	entrophy = 0.0
	for name in neighbors:
		count = neighbors[name]
		p = count * 1.0 / total
		entrophy -= p * math.log2(p)
	return entrophy

# 对象转json
def obj2Json(obj):
	return{
		"左临近字":obj.left,
		"右临近字":obj.right
	}

# 信息熵区间统计
# name: 词名
# neighbors: 临近词列表
# entrophy: 熵值
# isLeft: 左熵还是右熵
# array: 存储列表
def add_entrophy_interval(name,neighbors,entrophy,isLeft,array):
	if entrophy == 0:
		if isLeft:
			if "0" in array.keys():
				dict = array["0"]
			else:
				dict = {}
				array["0"] = dict
			dict[name] = neighbors[name].left
		else:
			if "0" in array.keys():
				dict = array["0"]
			else:
				dict = {}
				array["0"] = dict
			dict[name] = neighbors[name].right
	else:
		index = int(entrophy)
		key = str(index)+"~"+str(index+1)
		if isLeft:
			if key in array.keys():
				dict = array[key]
			else:
				dict = {}
				array[key] = dict
			dict[name] = neighbors[name].left
		else:
			if key in array.keys():
				dict = array[key]
			else:
				dict = {}
				array[key] = dict
			dict[name] = neighbors[name].right

def save_data(path,neighbors,entrophies,left,right):
	# 计算信息熵
	for name in neighbors:
		nearest_word = neighbors[name]
		entrophy = {}
		entrophy["左熵"] = calculate_entrophy(nearest_word.left,nearest_word.total_left)
		entrophy["右熵"] = calculate_entrophy(nearest_word.right,nearest_word.total_right)
		add_entrophy_interval(name,neighbors,entrophy["左熵"],True,left)
		add_entrophy_interval(name,neighbors,entrophy["右熵"],False,right)
		entrophies[name] = entrophy

	# 保存临近词json
	with open(path+"/neighbors.json","w") as file:
		jsObj = json.dump(neighbors,file,default=obj2Json,indent=2,ensure_ascii=False)

	# 保存熵json
	with open(path+"/entrophies.json","w") as file:
		jsObj = json.dump(entrophies,file,default=obj2Json,indent=2,ensure_ascii=False)

	# excel文件数据统计
	# 词-左熵值-右熵值-min{左熵，右熵}-（右熵-左熵）
	with open(path+"/熵数据统计.txt","w") as file:
		for key,value in entrophies.items():
			word_name = key
			left_entrophy = value["左熵"]
			right_entrophy = value["右熵"]
			freedom_degree = min(left_entrophy,right_entrophy)
			R_L = right_entrophy - left_entrophy
			file.write(word_name+"\t"+str(left_entrophy)+"\t"+str(right_entrophy)+"\t"+str(freedom_degree)+"\t"+str(R_L)+"\n")


	left = sorted(left.items(),key=operator.itemgetter(0))#按照item中的第一个字符进行排序，即按照key排序
	right = sorted(right.items(),key=operator.itemgetter(0))#按照item中的第一个字符进行排序，即按照key排序


	# 统计左熵区间json
	with open(path+"/left_entrophy_interval.json","w") as file:
		jsObj = json.dump(left,file,indent=2,ensure_ascii=False)

	# 统计右熵区间json
	with open(path+"/right_entrophy_interval.json","w") as file:
		jsObj = json.dump(right,file,indent=2,ensure_ascii=False)


	left_simplified = {}
	right_simplified = {}

	for item in left:
		range = item[0]
		left_simplified[range] = []
		for key in item[1]:
			left_simplified[range].append(key)

	for item in right:
		range = item[0]
		right_simplified[range] = []
		for key in item[1]:
			right_simplified[range].append(key)

	# 左熵区间简便格式json
	with open(path+"/simplified_left_entrophy_interval.json","w") as file:
		jsObj = json.dump(left_simplified,file,indent=2,ensure_ascii=False)

	# 右熵区间简便格式json
	with open(path+"/simplified_right_entrophy_interval.json","w") as file:
		jsObj = json.dump(right_simplified,file,indent=2,ensure_ascii=False)

#   ------------------------------------------------------------------------------   #
#							基于jieba精确模式分词统计词的信息熵  						 #
#								一句一行，词与词性用"-"分割							     #
#   ------------------------------------------------------------------------------   #
if __name__ == '__main__':
	path = "divide_result_1000.txt"	#数据文件路径
	frequency = Counter()		#频数词典
	total = 0					#总频数
	neighbors = {}				#临近字
	entrophies = {}				#每个词的信息熵
	left = {}					#左熵区间
	right = {}					#右熵区间

	#读文件
	with open(path,"r") as divide:
		lines = divide.readlines()

	# 统计频数
	for line in lines:
		words = line.split(" ")
		for index in range(0,len(words)):
			word = words[index]
			name = word.split("-")[0]
			frequency[name] += 1
			if name not in neighbors.keys():
				neighbors[name] = NearestWord(name)
			total += 1

			neighbor = neighbors[name]
			#增加左临近字
			if index > 0:
				left_word = words[index-1]
				left_name = left_word.split("-")[0]
				neighbor.add_left(left_name[-1])	
			#增加右临近字
			if index < len(words) - 1:
				right_word = words[index+1]
				right_name = right_word.split("-")[0]
				neighbor.add_right(right_name[0])

	save_data("result/1000",neighbors,entrophies,left,right)

