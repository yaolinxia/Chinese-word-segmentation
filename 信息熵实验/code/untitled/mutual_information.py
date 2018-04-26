import math

def calculate(frequency):
	mi = {}
	index1 = 1
	total1 = len(frequency)

	for key,value in frequency.items():
		if len(key) > 1:
			length = len(key)
			index1 += 1
			mutual_information = 0

			possiblity = 0
			for sublen in range(1,length):
				possiblity += 1
				prefrequency = frequency[key[:sublen]]
				postfrequency = frequency[key[sublen:]]
				mutual_information += value/(prefrequency*postfrequency)
			mi[key] = math.log2(mutual_information)/possiblity

	return mi

		