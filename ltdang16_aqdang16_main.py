from ltdang16_aqdang16_decision_tree import *
import sys
def main(filename):
	#Data preprocessing
	dataset = txt_to_dataset(filename)
	attributes = dataset[0]
	dataset.remove(attributes)
	target = attributes[-1]
	#Build Tree
	diction = decision_tree_learning(dataset, attributes, target, None, attributes, dataset, attributes)
	accuracy = accuracy_test
	print_tree(diction,target)
	#Test Tree
	print("---------------------------------------------------------------------------------------")
	print("The accuracy of the training set is " + str(accuracy_test(dataset,attributes,target)) + "%")
	print("The LOOCV accuracy is " + str(LOOCV(dataset,attributes,target)) + "%")

if __name__ == '__main__':
	main(sys.argv[1])