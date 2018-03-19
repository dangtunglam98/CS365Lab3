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

def attr_value_dict(data, attributes, resultattr):
	diction = {}
	newAttr = attributes[:]
	attri_hier = attr_hierarchy(attributes,data, resultattr)
	for item in attri_hier:
	 	values = get_value(data, newAttr, item)
	 	diction[item] = values
	#  	for val in values:
	#  		diction[item].append(val)
	return diction

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
    examples = []
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
    
    return examples

def make_tree(data, attributes, resultattr, parent_data = None):
	index_result = attributes.index(resultattr)
	result_vals = [row[index_result] for row in data]
	if not data:
		return decision_major(attributes,parent_data,resultattr)
	elif len(attributes) -1 <= 0:
		return decision_major(attributes,data,resultattr)
	elif result_vals.count(result_vals[0]) == len(result_vals):
		return result_vals[0]
	else:
		best = best_attribute(attributes,data,resultattr)
		tree = {best:{}}
		val_best = get_value(data,attributes,best)
		for values in val_best:
			example =  getExamples(data, attributes, best, values)
			newAttr = attributes[:]
			newAttr.remove(best)
			subtree = make_tree(example, newAttr, resultattr, data)
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
			
# def LOOCV(data,attributes,target):
#  	# for row in data:
#  	row = data[0]
#  	train_set = data
#  	train_set.remove(row)
#  	train_tree = make_tree(train_set,attributes,target)
#  	row = row[:len(row) - 1]
#  	prediction = predict(row,train_tree, attributes)
#  	return prediction

# def predict(row, tree, attributes):
# 	if isinstance(tree, str):
# 		return tree 
# 	for k, v in tree.items():
# 		if k in attributes:
# 			if isinstance(v, str):
# 				return v
# 			elif isinstance(v,dict):
# 				for key, value in v.items():
				 	                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
		 		# for key, value in v.items():
		 		# 	newkey = key
		 		# 	return newkey
		# 			predict(row, dic, attributes)
		# elif k in row:
		# 	predict(row, v, attributes)

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



dataset = txt_to_dataset('pets.txt')
attributes = dataset[0]
dataset.remove(attributes)
target = attributes[-1]
#best = str(best_attribute(attributes,dataset,target))
#best_val = get_value(dataset,attributes,best)
#print(attr_hierarchy(attributes,dataset,target))
print(attr_value_dict(dataset,attributes,target))

# print(dataset)
# print(attributes)
# print(best)
# print(best_val)
# print(get_index(attributes,best))
#print(getExamples(dataset,attributes,best,"gigantic"))
# diction = make_tree(dataset,attributes,target)
# tree_str = json.dumps(diction, indent=8)
# #print(LOOCV(dataset,attributes,target)) x

# tree_str = tree_str.replace("\n    ", "\n")
# tree_str = tree_str.replace('"', "")
# tree_str = tree_str.replace(',', "")
# tree_str = tree_str.replace("{", "")
# tree_str = tree_str.replace("}", "")
# tree_str = tree_str.replace("    ", " | ")
# tree_str = tree_str.replace("  ", " ")

#print(tree_str)
#print(diction)
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
