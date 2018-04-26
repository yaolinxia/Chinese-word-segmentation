import information_entrophy as ie
import json




def getEntrophy(strings,maxLength):
	frequency = ie.Counter()		#频数词典
	total = 0					#总频数
	neighbors = {}				#临近字
	entrophies = {}				#每个词的信息熵
	left = {}					#左熵区间
	right = {}					#右熵区间

	ind = 1
	total = len(strings)
	for string in strings:
		for i in range(2,min(maxLength+1,len(string)+1)):
			for index in range(0,len(string)-i+1):
				name = string[index:index+i]
				frequency[name] += 1
				if name not in neighbors.keys():
					neighbors[name] = ie.NearestWord(name)

				neighbor = neighbors[name]
				#增加左临近字
				if index > 0:
					left_name = string[index-1]
					neighbor.add_left(left_name)	
				#增加右临近字
				if index + i < len(string) - 1:
					right_name = string[index+i]
					neighbor.add_right(right_name)

		ind += 1

	ind1 = 1
	total1 = len(neighbors)
	# 计算信息熵
	for name in neighbors:
			
		nearest_word = neighbors[name]
		entrophy = {}
		entrophy["左熵"] = ie.calculate_entrophy(nearest_word.left,nearest_word.total_left)
		entrophy["右熵"] = ie.calculate_entrophy(nearest_word.right,nearest_word.total_right)
		entrophies[name] = entrophy

		ind1 += 1

	# # 保存临近词json
	# with open("result/combined/neighbors.json","w") as file:
	# 	jsObj = json.dump(neighbors,file,default=ie.obj2Json,indent=2,ensure_ascii=False)

	# # 保存熵json
	# with open("result/combined/entrophies.json","w") as file:
	# 	jsObj = json.dump(entrophies,file,default=ie.obj2Json,indent=2,ensure_ascii=False)

	return entrophies