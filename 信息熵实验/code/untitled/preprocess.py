import re

def term_preprocess(content,stopword_path):
	stopwords = stopwordlist(stopword_path)

	for word in stopwords:
		content = content.replace(word,' ')

	return cut_sentence(content)

def cut_sentence(content):

	content = re.sub(r"[0-9a-zA-Z\.\^\$\*\+\?\{\}\[\]\\\|\(\);,/\'\"$#@!~`％&\-\+：；‘“”’／=、×）〈〉＊［］（……¥！～·】【「」？。，》《．]+",' ',content)
	content = re.sub(r'\s+', ' ', content)
	strings = content.split(' ')

	strings = filter(lambda x: len(x) > 1, strings)
	strings = [i for i in strings]

	return strings

def stopwordlist(path):
    stopwords=[line.strip() for line in open(path,'r',encoding='utf-8').readlines()]
    return stopwords