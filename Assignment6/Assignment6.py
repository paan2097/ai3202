#Patrick Andresen paan2097 CSCI3202 Assignment 6

import getopt, argparse, itertools, sys

def calcConditional(arg1,arg2):
	if len(arg2) == 1:
		if arg1 == arg2[0]:
			return 1.0
		elif priorIndependence(arg1,arg2[0]):
			return arg1.probability

		#Probability of pollution given X
		elif arg1.label == "pollution" and arg2[0].label == "cancer":
			value = calcConditional(arg2[0],[arg1]) * arg1.probability
			var_1 = .05 * arg2[0].parents[1].probability
			var_2 = .02 * (1 - arg2[0].parents[1].probability)
			var_sum = var_1 + var_2
			amount = (calcConditional(arg2[0],[arg1]) * arg1.probability) + (var_sum * (1 - arg1.probability))
			return value/amount
		elif arg1.label == "pollution" and arg2[0].label == "dyspnoea":
			value = calcConditional(arg2[0],[arg1]) * arg1.probability
			prob_s = arg2[0].parents[0].parents[1].probability
			var_1 = .65 * ((prob_s * .05) + ((1-prob_s) * .02))
			var_2 = .3 * ((prob_s * .95) + ((1-prob_s) * .98))
			var_sum = var_1 + var_2
			amount = (calcConditional(arg2[0],[arg1]) * arg1.probability) + (var_sum * (1 - arg1.probability))
			return value/amount
		elif arg1.label == "pollution" and arg2[0].label == "xray":
			value = calcConditional(arg2[0],[arg1]) * arg1.probability
			prob_s = arg2[0].parents[0].parents[1].probability
			var_1 = .9 * ((prob_s * .05) + ((1-prob_s) * .02))
			var_2 = .2 * ((prob_s * .95) + ((1-prob_s) * .98))
			var_sum = var_1 + var_2
			amount = (calcConditional(arg2[0],[arg1]) * arg1.probability) + (var_sum * (1 - arg1.probability))
			return value/amount

		#Probability of smoker given X
		elif arg1.label == "smoker" and arg2[0].label == "cancer":
			value = calcConditional(arg2[0],[arg1]) * arg1.probability
			var_1 = .001 * arg2[0].parents[0].probability
			var_2 = .02 * (1 - arg2[0].parents[0].probability)
			var_sum = var_1 + var_2
			amount = (calcConditional(arg2[0],[arg1]) * arg1.probability) + (var_sum * (1 - arg1.probability))
			return value/amount
		elif arg1.label == "smoker" and arg2[0].label == "dyspnoea":
			value = calcConditional(arg2[0],[arg1]) * arg1.probability
			prob_p = arg2[0].parents[0].parents[0].probability
			var_1 = .65 * ((prob_p * .001) + ((1-prob_p) * .02))
			var_2 = .3 * ((prob_p * .999) + ((1-prob_p) * .98))
			var_sum = var_1 + var_2
			amount = (calcConditional(arg2[0],[arg1]) * arg1.probability) + (var_sum * (1 - arg1.probability))
			return value/amount

		#Probability of cancer given X
		elif arg1.label == "cancer" and arg2[0].label == "smoker":
			var_1 = .03 * arg1.parents[0].probability
			var_2 = .05 * (1 - arg1.parents[0].probability)
			return var_1 + var_2
		elif arg1.label == "cancer" and arg2[0].label == "pollution":
			var_1 = .03 * arg1.parents[1].probability
			var_2 = .001 * (1 - arg1.parents[1].probability)
			return var_1 + var_2
		elif arg1.label == "cancer" and arg2[0].label == "dyspnoea":
			value = .65 * arg1.probability
			amount = (.65 * arg1.probability) + (.3 * (1 - arg1.probability))
			return value/amount
		elif arg1.label == "cancer" and arg2[0].label == "xray":
			value = .9 * arg1.probability
			amount = (.9 * arg1.probability) + (.2 * (1 - arg1.probability))
			return value/amount

		#Probability of dyspnoea given X
		elif arg1.label == "dyspnoea" and arg2[0].label == "cancer":
			return .65
		elif arg1.label == "dyspnoea" and arg2[0].label == "smoker":
			var_1 = calcConditional(arg1.parents[0],arg2) * .65
			var_2 = (1 - calcConditional(arg1.parents[0],arg2)) * .3
			return var_1 + var_2
		elif arg1.label == "dyspnoea" and arg2[0].label == "pollution":
			var_1 = calcConditional(arg1.parents[0],arg2) * .65
			var_2 = (1 - calcConditional(arg1.parents[0],arg2)) * .3
			return var_1 + var_2

		#Probability of xray given X
		elif arg1.label == "xray" and arg2[0].label == "dyspnoea":
			var_1 = .9 * calcConditional(arg1.parents[0],arg2)
			var_sum = (1 - calcConditional(arg1.parents[0],arg2))
			var_2 = .2 * var_sum
			return var_1 + var_2
		elif arg1.label == "xray" and arg2[0].label == "cancer":
			return .9
		elif arg1.label == "xray" and arg2[0].label == "smoker":
			var_1 = calcConditional(arg1.parents[0],arg2) * .9
			var_2 = (1 - calcConditional(arg1.parents[0],arg2)) * .2
			return var_1 + var_2
		elif arg1.label == "xray" and arg2[0].label == "pollution":
			var_1 = calcConditional(arg1.parents[0],arg2) * .9
			var_2 = (1 - calcConditional(arg1.parents[0],arg2)) * .2
			return var_1 + var_2
		else:
			return 0
	elif len(arg2) == 2:

                #Probability of pollution given X,Y
		if (arg1.label == "pollution" and arg2[0].label == "cancer" and arg2[1].label == "smoker") \
			or (arg1.label == "pollution" and arg2[0].label == "smoker" and arg2[1].label == "cancer"):
			value = .03 * arg1.probability
			amount = value + (.05 * (1-arg1.probability))
			return value/amount
		elif (arg1.label == "pollution" and arg2[0].label == "dyspnoea" and arg2[1].label == "smoker") \
			or (arg1.label == "pollution" and arg2[0].label == "smoker" and arg2[1].label == "dyspnoea"):
			return 1-.102

		#Probability of smoker given X,Y
		elif (arg1.label == "smoker" and arg2[0].label == "cancer" and arg2[1].label == "smoker") \
			or (arg1.label == "smoker" and arg2[0].label == "smoker" and arg2[1].label == "cancer"):
			return 1
		elif (arg1.label == "smoker" and arg2[0].label == "dyspnoea" and arg2[1].label == "smoker") \
			or (arg1.label == "smoker" and arg2[0].label == "smoker" and arg2[1].label == "dyspnoea"):
			return 1

		#Probability of cancer given X,Y
		elif (arg1.label == "cancer" and arg2[0].label == "cancer" and arg2[1].label == "smoker") \
			or (arg1.label == "cancer" and arg2[0].label == "smoker" and arg2[1].label == "cancer"):
			return 1
		elif (arg1.label == "cancer" and arg2[0].label == "dyspnoea" and arg2[1].label == "smoker") \
			or (arg1.label == "cancer" and arg2[0].label == "smoker" and arg2[1].label == "dyspnoea"):
			return .067

		#Probability of dyspnoea given X,Y
		elif (arg1.label == "dyspnoea" and arg2[0].label == "cancer" and arg2[1].label == "smoker") \
			or (arg1.label == "dyspnoea" and arg2[0].label == "smoker" and arg2[1].label == "cancer"):
			return .65
		elif (arg1.label == "dyspnoea" and arg2[0].label == "dyspnoea" and arg2[1].label == "smoker") \
			or (arg1.label == "dyspnoea" and arg2[0].label == "smoker" and arg2[1].label == "dyspnoea"):
			return 1

		#Probability of xray given X,Y
		elif (arg1.label == "xray" and arg2[0].label == "cancer" and arg2[1].label == "smoker") \
			or (arg1.label == "xray" and arg2[0].label == "smoker" and arg2[1].label == "cancer"):
			return .9
		elif (arg1.label == "xray" and arg2[0].label == "dyspnoea" and arg2[1].label == "smoker") \
			or (arg1.label == "xray" and arg2[0].label == "smoker" and arg2[1].label == "dyspnoea"):
			return .247
		else:
			return 0
	else:
		return 0

def calcMarginal(m):
	for i in m:
		print("\nMarginal probability of %s: %.4f\n" % (i.label, i.probability))

def calcJoint(arg1,arg2):
	if len(arg2) == 1:
		return calcConditional(arg1,arg2) * arg2[0].probability
	else:
		return calcConditional(arg1,arg2) * calcJoint(arg2[0],arg2[1:])

def stringToNode(bnet, s):
	if s == 'p' or s == 'P':
		return bnet[0]
	elif s == 's' or s == 'S':
		return bnet[1]
	elif s == 'c' or s == 'C':
		return bnet[2]
	elif s == 'd' or s == 'D':
		return bnet[3]
	elif s == 'x' or s == 'X':
		return bnet[4]

def priorIndependence(arg1, arg2):
	return (arg1.label == "pollution" and arg2.label == "smoker") \
		or (arg1.label == "smoker" and arg2.label == "pollution")

class Node:
	def __init__(self,label):
		self.label = label
		self.probability = 0.0
		self.parents = []

	def set_probability(self,prior):
		self.probability = prior

def create_bnet(priors):

	pollution = Node("pollution")
	pollution.set_probability(priors[0])

	smoker = Node("smoker")
	smoker.set_probability(priors[1])

	cancer = Node("cancer")
	cancer.parents = [pollution, smoker]
	p1 = (1 - pollution.probability) * smoker.probability * .05
	p2 = (1 - pollution.probability) * (1 - smoker.probability) * .02
	p3 = pollution.probability * smoker.probability * .03
	p4 = pollution.probability * (1 - smoker.probability) * .001
	cancer.set_probability(p1+p2+p3+p4)

	dyspnoea = Node("dyspnoea")
	dyspnoea.parents = [cancer]
	p1 = cancer.probability * .65
	p2 = (1 - cancer.probability) * .3
	dyspnoea.set_probability(p1+p2)

	xray = Node("xray")
	xray.parents = [cancer]
	p1 = cancer.probability * .9
	p2 = (1 - cancer.probability) * .2
	xray.set_probability(p1+p2)

	return [pollution,smoker,cancer,dyspnoea,xray]

if __name__ == "__main__":
	
	# Default prior values
	priors = [0.9,0.3]

	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
		if "-p" not in opts:
			bnet = create_bnet(priors)
		for o, a in opts:
			if o in ("-p"):
				if a[0] == "P" or a[0] == "p":
					priors[0] = float(a[1:])
				elif a[0] == "S" or a[0] == "s":
					priors[1] = float(a[1:])
				bnet = create_bnet(priors)
			elif o in ("-m"):
				a_prime = []
				for i in a:
					a_prime.append(stringToNode(bnet,i))
				calcMarginal(a_prime)
			elif o in ("-g"):
				'''you may want to parse a here and pass the left of |
				and right of | as arguments to calcConditional
				'''
				p = a.find("|")
				arg1 = stringToNode(bnet,a[:p])
				arg2 = []
				for i in a[p+1:]:
					arg2.append(stringToNode(bnet,i))
				cp = calcConditional(arg1, arg2)
				s1 = arg1.label
				s2 = arg2[0].label
				for i in range(1,len(arg2)):
					s2 = s2 + (", %s"%(arg2[i].label))
				print("\nConditional probability of %s given %s: %.4f\n" %(s1,s2,cp))
			elif o in ("-j"):
				arg1 = stringToNode(bnet,a[0])
				arg2 = []
				for i in a[1:]:
					arg2.append(stringToNode(bnet,i))
				jp = calcJoint(arg1,arg2)
				s1 = arg1.label
				s2 = arg2[0].label
				for i in range(1,len(arg2)):
					s2 = s2 + (", %s"%(arg2[i].label))
				print("\nJoint probability of %s and %s: %.4f\n" %(s1,s2,jp))
			else:
				assert False, "unhandled option"

	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
        sys.exit(2)
