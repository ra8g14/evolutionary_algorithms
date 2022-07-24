from __future__ import division
import random, string
from random import randrange, sample
# from operator import itemgetter
import time
import csv
from bitstring import BitArray
from bitstring import Bits

LENGTH = 100
POP_SIZE = 25
SAMPLE_SIZE = 15
MUTATION_BIAS = 0.005

def create_population(length, size):
	"""
	Creates a population of size 'size'. Each member consists of a string of length
	'length' bits. All bits are initialised to 0. 
 	"""
 	# pop = [BitArray([0]*length) for i in range(size)]
 	pop = [[0]*length for i in range(size)]
 	return pop

def create_mutli_dim_pop(length, dimensions, size):
 	pop = [[[0]*length for i in range(size)] for j in range(dimensions)]
 	return pop

def obj_fitness(member):
 	"""
 	Evaluates the objective fitness of a member by counting the number of 1s in the bitstring.
 	"""
 	# consider using coutner if this is too slow
 	fitness = member.count(1)
 	return fitness

def exp1_score(a, b):
	"""
	score(a,b) = 1 if a>b, 0 otherwise
	"""
	if a.count(1) > b.count(1):
		return 1
	else:
		return 0

def exp1_subj_fitness(member, sample):
	"""
	Evaluates the subjective fitness of a member uisng the sum of exp1_score function
	against an input sample.
	"""
	fitness = 0
	for member2 in sample:
		fitness = fitness + exp1_score(member,member2[0])
	return fitness

def exp1_subj_fitness_pop(popfit1, popfit2):
	"""
	Evaluates the fitnesses of each member in an entire population, using samples from
	another population and the 'exp1_subj_fitness' function.
	Returns the fexxpitnesses as a list. 
	"""
	fitnesses = []
	for member in popfit1:
		fitnesses.append(exp1_subj_fitness(member[0],random.sample(popfit2, SAMPLE_SIZE)))
	# update popfit1 with new subj fitnesses
	# popfit1 = zip(list(zip(*popfit1)), fitnesses)
	return fitnesses

def mutate_member(member_original, mutation_rate):
	"""
	Mutates a member in a popoulation with probability 'mutation_rate' that a bit is
	assigned a new random value (or is flipped).
	"""
	member = []
	member.extend(member_original)
	for i,bit in enumerate(member):
		# test = random.random()
		# print test
		if random.random() < mutation_rate:
			#member[i] = !member[i]
			member[i] = 0 if random.random() < 0.5 else 1
	return member

def make_new_gen(pop_fit, mutation_rate):
	# select member for mutation
	total = 0
	wheel = []
	# create wheel
	for member in pop_fit:
		total = total + member[1]
		wheel.append(total)
	# pick from wheel
	if total != 0:
		pick = random.random() * total
		for i, wheel_val in enumerate(wheel):
			if wheel_val >= pick:
				index = i
				break
	else:
		index = randrange(0, len(pop_fit))
		pop_fit[index] = (mutate_member(pop_fit[index][0], mutation_rate),0)
		return[index, pop_fit[index][0]] 
	child = mutate_member(pop_fit[index][0], mutation_rate)
	# swap with random member of the population
	while True:
		index2 = randrange(0, len(pop_fit))
		if index2 != index:
			break
	pop_fit[index2] = (child,0)
	return[index2,child]

def make_new_gen2(pop_fit, mutation_rate):
	new_pop_fit = []
	for n in range(0,len(pop_fit)):
		# select member for mutation
		total = 0
		wheel = []
		# create wheel
		for member in pop_fit:
			total = total + member[1] + 1
			wheel.append(total)
		# pick from wheel
		pick = random.random() * total
		for i, wheel_val in enumerate(wheel):
			if wheel_val >= pick:
				index = i
				break
		new_pop_fit.append((mutate_member(pop_fit[index][0], mutation_rate), 0))
	return new_pop_fit

def exp1(generations,filename):
	obj_fitnesses =[[0 for i in range(0,POP_SIZE*2)]]
	# initialise populations and subj fitnesses
	pop1 = create_population(LENGTH, POP_SIZE)
	pop2 = create_population(LENGTH, POP_SIZE)
	subj_fitnesses1 = [[0 for i in range(0,POP_SIZE)]]
	subj_fitnesses2 = [[0 for i in range(0,POP_SIZE)]]
	# create a list of tuples containing members with their subjective fitnesses
	pop1_fit = zip(pop1, subj_fitnesses1[0])
	pop2_fit = zip(pop2, subj_fitnesses2[0])
	for i in range(0,generations):
		# make a new generation - use fitness proportionate selection to mutate a new parent in each population and find a replacement
		# child1 = make_new_gen(pop1_fit, MUTATION_BIAS)
		# child2 = make_new_gen(pop2_fit, MUTATION_BIAS)
		pop1_fit = make_new_gen2(pop1_fit, MUTATION_BIAS)
		pop2_fit = make_new_gen2(pop2_fit, MUTATION_BIAS)
		## update objective fitnesses list with new members
		# calculate new objective fitnesses for new populations
		obj_fitnesses_ext = []
		# obj_fitnesses_ext.extend(obj_fitnesses[i])
		for mem in pop1_fit:
			obj_fitnesses_ext.append(obj_fitness(mem[0]))
		for mem in pop2_fit:
			obj_fitnesses_ext.append(obj_fitness(mem[0]))
		obj_fitnesses.append(obj_fitnesses_ext)
		# obj_fitnesses[i+1][child1[0]] = obj_fitness(child1[1])
		# obj_fitnesses[i+1][child2[0]+POP_SIZE] = obj_fitness(child2[1])
		# calc new subjective fitnesses for each member in both populations
		fitnesses1 = exp1_subj_fitness_pop(pop1_fit,pop2_fit)
		pop1_fit = zip(list(zip(*pop1_fit)[0]), fitnesses1)
		fitnesses2 = exp1_subj_fitness_pop(pop2_fit,pop1_fit)
		pop2_fit = zip(list(zip(*pop2_fit)[0]), fitnesses2)
		subj_fitnesses1.append(fitnesses1)
		subj_fitnesses2.append(fitnesses2)
	with open(filename + ".csv", "a") as fp:
		wr = csv.writer(fp, dialect='excel')
		wr.writerows(obj_fitnesses)
	return [obj_fitnesses, subj_fitnesses1, subj_fitnesses2, pop1_fit, pop2_fit]





	