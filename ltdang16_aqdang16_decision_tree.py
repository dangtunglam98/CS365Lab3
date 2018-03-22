from math import log
def txt_to_dataset(txtfile):
	"""Return list of list of data"""
	dataset = open(txtfile, 'r')
	dataset = [line.split() for line in dataset.readlines()]
	return dataset

def get_frequency(attributes, data, targetAttr):
	"""Return a dictionary of the frequency of value in attributes"""
	valFreq = {}
	i = attributes.index(targetAttr)
	for entry in data: 
	    if ((entry[i]) in valFreq):
	    	valFreq[entry[i]] += 1.0
	    else:
	    	valFreq[entry[i]]  = 1.0
	return valFreq

def plurality_value(attributes,data,resultAttr):
	"""Return the predicted decision of example""" 
	major_freq = get_frequency(attributes,data,resultAttr)
	maximum = 0
	major = ""
	for key in major_freq.keys():
		if major_freq[key] > maximum:
			maximum = major_freq[key]
			major = key
	return major

def entropy(attributes, data, targetAttr):
	"""Return the entropy"""
	entropy_freq = get_frequency(attributes,data,targetAttr)
	dataEntropy = 0.0
	for freq in entropy_freq.values():
		dataEntropy += (-freq/len(data)) * log(freq/len(data), 2)
	return dataEntropy 

def information_gain(attributes, data, targetAttr, resultAttr):
	"""Return the information gain"""
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
	"""Return the best attribute of the data"""
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
	"""Return the list of attributes in an importance order"""
	hierarchy = []
	poten_attr = attributes
	while poten_attr != [resultAttr]:
		best = best_attribute(poten_attr,data,resultAttr)
		hierarchy.append(best)
		poten_attr.remove(best)
	return hierarchy

def get_value(data, attributes, bestattr):
	"""Return the values in an attribute"""
	index_attr = attributes.index(bestattr)
	values = []
	for entry in data:
		if entry[index_attr] != bestattr:
			if entry[index_attr] not in values:
				values.append(entry[index_attr])
	return values

def attr_value_dict(data, attributes, resultattr):
	"""Return A dictionary that contain attributes as keys and list of values of the attribute"""
	diction = {}
	newAttr = attributes[:]
	attri_hier = attr_hierarchy(attributes,data, resultattr)
	for item in attri_hier:
	 	values = get_value(data, newAttr, item)
	 	diction[item] = values
	return diction


def getExamples(data, attributes, best, val):
    """Return examples that contain a certain value of attribute"""
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

def decision_tree_learning(data, attributes, resultattr, parent_data, original_attribute, old_data, parent_attribute):
	"""Return the decision tree in a dictionary form"""
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
	 				subtree = decision_tree_learning(example, newAttr, resultattr, data, original_attribute,old_data,attributes)
	 				tree[best][v] = subtree

	return tree

def get_index(attributes, attr):
	index = attributes.index(attr)
	return index
			
def LOOCV(data,attributes,target):
	"""Return the accuracy level with the LOOCV"""
	old_data = data[:]
	predict_num = 0
	total = 0
	for row in data:
		total += 1
		train_set = data[:]
		train_set.remove(row)
		train_tree = decision_tree_learning(train_set,attributes,target,None, attributes, old_data,attributes)
		prediction = predict(row,train_tree, attributes)
		if prediction == row[-1]:
			predict_num +=1
	accuracy = predict_num/total * 100
	return accuracy

			

def predict(row, tree, attributes):
	"""Return the predicted result value of a row in data"""
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
	"""Return the accuracy of the dataset"""
	tree = decision_tree_learning(data, attributes, target, None, attributes, data,attributes)
	predict_num = 0
	total = 0
	for row in data:
		total += 1
		prediction = predict(row,tree, attributes)
		if prediction == row[-1]:
			predict_num +=1
	accuracy = predict_num/total * 100
	return accuracy

def print_tree(tree,target, tab=""):
	"""Return a tree in a visualizable format"""
	for k, v in tree.items():
		if isinstance(v, str):
			print(k + ":" + v)
		else:
			for key, value in v.items():
				print(tab + k + ":" + key)
				if isinstance(value, str):
					print(tab + "	"+ target+ ":" + value)
				else:
					tabNew = tab + "	"
					print_tree(value, target, tabNew)
		



# dataset = txt_to_dataset('titanic2.txt')
# attributes = dataset[0]
# dataset.remove(attributes)
# target = attributes[-1]
# #row = dataset[45]
# diction = decision_tree_learning(dataset, attributes, target, None, attributes, dataset, attributes)
# #print(row)

# print_tree(diction,target)

