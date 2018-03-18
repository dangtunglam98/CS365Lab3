from math import log
import json
def txt_to_dataset(txtfile):
	dataset = open(txtfile, 'r')
	dataset = [line.split() for line in dataset.readlines()]
	return dataset

# print(txt_to_dataset('pets.txt'))
def get_frequency(attributes, data, targetAttr):
	valFreq = {}
	i = attributes.index(targetAttr)
	# Calculate the frequency of each of the values in the target attr
	for entry in data: 
	    if ((entry[i]) in valFreq):
	    	valFreq[entry[i]] += 1.0
	    else:
	    	valFreq[entry[i]]  = 1.0
	return valFreq

def decision_major(attributes,data,resultAttr):
	major_freq = get_frequency(attributes,data,resultAttr)
	maximum = 0
	major = ""
	for key in major_freq.keys():
		if major_freq[key] > maximum:
			maximum = major_freq[key]
			major = key
	return major

def entropy(attributes, data, targetAttr):
	entropy_freq = get_frequency(attributes,data,targetAttr)
	dataEntropy = 0.0
	for freq in entropy_freq.values():
		dataEntropy += (-freq/len(data)) * log(freq/len(data), 2)
	return dataEntropy 

def information_gain(attributes, data, targetAttr, resultAttr):
	total = 0.0
	gain_freq = get_frequency(attributes,data,targetAttr)
	attr_index = attributes.index(targetAttr)
	for element in gain_freq.keys():
		prob_elem = gain_freq[element] / sum(gain_freq.values())
		datasubset = [row for row in data if row[attr_index] == element]
		total = total + prob_elem * entropy(attributes,datasubset,resultAttr)
	gain = entropy(attributes,data,resultAttr) - total
	return gain

def best_attribute(attributes, data, resultAttr):
	best_attr = attributes[0]
	max_gain = 0
	for attr in attributes:
		if attr == resultAttr:
			pass 
		else:
			pos_gain = information_gain(attributes, data, attr, resultAttr)
			if pos_gain > max_gain:
				max_gain = pos_gain
				best_attr = attr
	return best_attr
def attr_hierarchy(attributes,data,resultAttr):
	hierarchy = []
	poten_attr = attributes
	while poten_attr != [resultAttr]:
		best = best_attribute(poten_attr,data,resultAttr)
		hierarchy.append(best)
		poten_attr.remove(best)
	return hierarchy

def get_value(data, attributes, bestattr):
	index_attr = attributes.index(bestattr)
	values = []
	for entry in data:
		if entry[index_attr] != bestattr:
			if entry[index_attr] not in values:
				values.append(entry[index_attr])
	return values


# def get_example(data, attributes, bestattr, val):
# 	index_best = attributes.index(bestattr)
# 	examples = []
# 	for row in data:
# 		if row[index_best] == val:
# 			newRow = []
# 			for i in range (len(row)):
# 				if i != index_best:
# 					newRow.append(row[i])
# 			examples.append(newRow)
# 	return examples
def getExamples(data, attributes, best, val):
    examples = [[]]
    list_attr = attributes
    index = get_index(list_attr,best)
    #index = 0
    for entry in data:
        #find entries with the give value
        if (entry[index] == val):
            newEntry = []
            #add value if it is not in best column
            for i in range(0,len(entry)):
                if(i != index):
                    newEntry.append(entry[i])
            examples.append(newEntry)
    examples.remove([])
    return examples

def make_tree(data, attributes, resultattr):
	best = best_attribute(attributes,data,resultattr)
	tree = {best:{}}
	val_best = get_value(data,attributes,best)
	if len(attributes) - 1 <= 0:
		return decision_major(attributes,data,resultattr)
	else:
		for values in val_best:
			example =  getExamples(data, attributes, best, values)
			newAttr = attributes[:]
			newAttr.remove(best)
			subtree = make_tree(example, newAttr, resultattr)
			tree[best][values] = subtree

	return tree

def get_index(attributes, attr):
	index = attributes.index(attr)
	return index

def myprint(dictionary,attributes): 
	for key, value in dictionary.items():
		if key in attributes:
			if isinstance(value, dict):
				for k in value.keys():
					print(key + ":" + k)
					myprint(value,attributes)
			else:
				print(key + ":" + str(value))
		elif isinstance(value,bool):
			print("	LOL" + ": " + str(value))		
		else:
			myprint(value,attributes)
			

# def information_gain(result, attr):
# 	total = 0
# 	for element in attr:
# 		total = total + sum(element)/ sum(result) * entropy(element)
# 	gain = entropy(result) - total
# 	return gain

# def get_result(dataset):
# 	Yes = 0
# 	No = 0
# 	result = []
# 	dataset_no_headings = dataset[1:]
# 	for row in dataset_no_headings:
# 		if row[len(row)-1] in ["yes","Yes","True","true"]:
# 			Yes += 1
# 		else:
# 			No += 1
# 	result = [Yes , No]
# 	return result



dataset = txt_to_dataset('tennis.txt')
attributes = dataset[0]
dataset.remove(attributes)
target = attributes[-1]
best = str(best_attribute(attributes,dataset,target))
best_val = get_value(dataset,attributes,best)
#print(attr_hierarchy(attributes,dataset,target))
# print(dataset)
# print(attributes)
# print(best)
# print(best_val)
# print(get_index(attributes,best))
diction = make_tree(dataset,attributes,target)
tree_str = json.dumps(diction, indent=8)
tree_str = tree_str.replace("\n    ", "\n")
tree_str = tree_str.replace('"', "")
tree_str = tree_str.replace(',', "")
tree_str = tree_str.replace("{", "")
tree_str = tree_str.replace("}", "")
tree_str = tree_str.replace("    ", " | ")
tree_str = tree_str.replace("  ", " ")

print(tree_str)
#print(myprint(diction,attributes))
#dict_to_tree(diction)	
# print(attr_hierarchy(attribute,dataset,target))
# print(make_tree(dataset,attribute,target))
# print(get_value(dataset,attribute,best))
# print(information_gain(attributes,dataset,"outlook", "playtennis"))
# print(information_gain(attributes,dataset,"temperature", "playtennis"))
# print(information_gain(attributes,dataset,"humidity", "playtennis"))
# print(information_gain(attributes,dataset,"wind", "playtennis"))
# print(attr_hierarchy(attributes,dataset,target))
# print(getExamples(dataset,attributes,"wind","weak"))
