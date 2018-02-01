import re
import jieba.posseg as pseg

    
def preprocess(content,intermediate_path):
	# content = re.sub(r"[0-9a-zA-Z\.\^\$\*\+\?\{\}\[\]\\\|\(\);,/\'\"$#@!~`％\-\+：；‘“”’／=、×）〈〉＊［］（……¥！～·】【「」？。，》《．]+",' ',content)

	index = 1
	length = len(content)
	words = pseg.cut(content)
	with open(intermediate_path,"w") as inter_file:
		for word, flag in words:
			print(str(index * 1.0 / length * 100)[0:15]+"%")
			index += 1
			if flag == "nr" or flag == "m" or flag == "x" or flag == "uj" or flag == "eng":
				inter_file.write(" ")
			else:
				inter_file.write(word)


if __name__ == '__main__':
	path = "test_YQSCD2.txt"
	intermediate_path = "intermediate_product/intermiate_"+path

	with open(path,"r") as file:
		content = file.read()



	preprocess(content,intermediate_path)