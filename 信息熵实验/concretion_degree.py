import information_entrophy as ie
import re

def calculate_concretion(frequency,concretion):
	index1 = 1
	total1 = len(frequency)
	print("----------------------concretion started-----------------------")

	for key,value in frequency.items():

		print(str(index1 * 1.0 / total1 * 100)[0:10]+"%")
		index1 += 1

		if len(key) > 1:
			max_sub_frequency = -1.0
			length = len(key)
			totalfrequency = frequency[key] * 1.0 / len(frequency)

			for sublen in range(1,length):
				prefrequency = frequency[key[:sublen]] * 1.0 / len(frequency)
				postfrequency = frequency[key[sublen:]] * 1.0 / len(frequency)
				if max_sub_frequency < prefrequency * postfrequency:
					max_sub_frequency = prefrequency * postfrequency
			concretion[key] = totalfrequency / max_sub_frequency

	print("----------------------concretion finished-----------------------")

def save_data(concretion,output_path):
	with open(output_path,"w") as file:
		for key,value in concretion.items():
			file.write(key+"\t"+str(value))


if __name__ == '__main__':
	frequency = ie.Counter()
	concretion = {}
	path = "intermediate_product/intermiate_test_YQSCD2.txt"
	output_path = "result/130000/concretion(preprocessed).txt"
	maxLength = 6

	with open(path,"r") as file:
		content = file.read()
	content = re.sub(r'\s+', ' ', content)

	strings = content.split(' ')

	print("----------------------frequency started-----------------------")
	ind = 1
	total = len(strings)
	for string in strings:
		for i in range(1,min(maxLength+1,len(string))):
			for index in range(0,len(string)-i+1):
				frequency[string[index:index+i]] += 1

		print(str(ind * 1.0 / total * 100)[0:10]+"%")
		ind += 1

	print("----------------------frequency finished-----------------------")

	calculate_concretion(frequency,concretion)
	
	save_data(concretion,output_path)
