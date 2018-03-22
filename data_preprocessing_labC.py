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

def plurality_value(attributes,data,resultAttr):
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

def make_tree(data, attributes, resultattr, parent_data, original_attribute, old_data, parent_attribute):
	index_result = attributes.index(resultattr)
	result_vals = [row[index_result] for row in data]

	if not data:
		return plurality_value(parent_attribute,parent_data,resultattr)
	elif len(attributes) -1 <= 0:
		return plurality_value(attributes,data,resultattr)
		 
	elif result_vals.count(result_vals[0]) == len(result_vals):
		return result_vals[0]
	else:
		best = best_attribute(attributes,data,resultattr)
		tree = {best:{}}
		ins = original_attribute[:]
		old = old_data[:]
		val_best = attr_value_dict(old_data,ins,resultattr)
		for key, value in val_best.items():
			if key == best:
	 			for v in value:
	 				example =  getExamples(data, attributes, best, v)
	 				newAttr = attributes[:]
	 				newAttr.remove(best)
	 				subtree = make_tree(example, newAttr, resultattr, data, original_attribute,old_data,attributes)
	 				tree[best][v] = subtree

	return tree

def get_index(attributes, attr):
	index = attributes.index(attr)
	return index
			
def LOOCV(data,attributes,target):
	old_data = data[:]
	predict_num = 0
	total = 0
	for row in data:
		total += 1
		train_set = data[:]
		train_set.remove(row)
		train_tree = make_tree(train_set,attributes,target,None, attributes, old_data,attributes)
		prediction = predict(row,train_tree, attributes)
		if prediction == row[-1]:
			predict_num +=1
	accuracy = predict_num/total * 100
	return accuracy

			

def predict(row, tree, attributes):
	attributes = attributes[:len(attributes)]
	for k, v in tree.items():
		if isinstance(v, str):
			return v
		elif k in attributes:
			index_attr = attributes.index(k)
			for key, value in v.items():
				if key == row[index_attr]:
					if isinstance(value,str):
						return value
					elif isinstance(value,dict):
						return predict(row,value,attributes)

def accuracy_test(data,attributes,target):
	tree = make_tree(data, attributes, target, None, attributes, data,attributes)
	predict_num = 0
	total = 0
	for row in data:
		total += 1
		prediction = predict(row,tree, attributes)
		if prediction == row[-1]:
			predict_num +=1
	accuracy = predict_num/total * 100
	return accuracy





dataset = txt_to_dataset('pets.txt')
attributes = dataset[0]
dataset.remove(attributes)
target = attributes[-1]
#row = dataset[45]
diction = make_tree(dataset, attributes, target, None, attributes, dataset, attributes)
#print(row)


# diction = make_tree(dataset, attributes, target, None, attributes, dataset)
#print(diction)

tree_str = json.dumps(diction, indent=8)

tree_str = tree_str.replace("\n    ", "\n")
tree_str = tree_str.replace('"', "")
tree_str = tree_str.replace(',', "")
tree_str = tree_str.replace("{", "")
tree_str = tree_str.replace("}", "")
tree_str = tree_str.replace("    ", " | ")
tree_str = tree_str.replace("  ", " ")
#print(row)
#print(predict(row,diction,attributes))
print(tree_str)
# print(LOOCV(dataset,attributes,target)) 
#print(accuracy_test(dataset,attributes,target))
#print(diction)
#print(myprint(diction,attributes))
