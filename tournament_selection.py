

def create_sample(popfit, sample_size):
	"""
	Uses A roulette wheel selection scheme to produce a sample from a population of size
	'sample size'
	"""
	sample = []
	popfit_local = []
	popfit_local.extend(popfit)
	for i in range(0, sample_size):
		# create the wheel
		total = 0
		wheel = []
		for member in popfit_local:
			# print member[1]
			# print member
			total = total + member[1]
			wheel.append(total)
		if total != 0:
			# pick from wheel	
			pick = random.random() * total
			for k, wheel_val in enumerate(wheel):
				if wheel_val >= pick:
					sample.append(popfit_local[k])
					del popfit_local[k]
					break
		else:
			sample.append(random.choice(popfit_local))
	sample = list(zip(*sample))
	return sample

def tournament_selection(pop_fits, mutation_rate):
	"""
	Creates new popfits uisng tournament selection.
	Finds subj fitness of new member
	Returns objective fitnesses of new members
	"""
	child_objs = []
	for i, pop_fit in enumerate(pop_fits):
		# print pop_fit
		# Choose a parent
		A = random.choice(pop_fit)
		B = random.choice(pop_fit)
		parent = B
		if A[1] > B[1]:
			parent = A
		# Mutate parent
		child = mutate_member(parent[0], mutation_rate)
		# Choose a replacement
		#A = random.choice(pop_fit)
		#B = random.choice(pop_fit)
		indA = randrange(0,len(pop_fit))
		indB = randrange(0,len(pop_fit))
		A = pop_fit[indA]
		B = pop_fit[indB]
		index = indB
		if A[1] > B[1]:
			index = indA
		pop_fits[i][index] = (child, exp1_subj_fitness(child,create_sample(pop_fits[1], SAMPLE_SIZE)))
		child_objs.append([obj_fitness(child), index])
	return child_objs

def experiment1(generations):
	"""
	Determines the objective fitness of each indivdual in each population.
	Calculates the subjective fitness of each individual in each population.
	Uses tournament selection to decide which individuals are reproduced/ mutated.
	Repeats for 'generations' number of generations.
	The objective fitnesses for each indivudal are returned as a list for each generation
	along with the average subjective fitness for each population.
	"""
	obj_fitnesses = []
	subj_fitnesses1 = []
	subj_fitnesses2 = []
	gen_subj_fitnesses1 = [0 for i in range(0,POP_SIZE)]
	gen_subj_fitnesses2 = [0 for i in range(0,POP_SIZE)]
	pop1 = create_population(POP_SIZE,LENGTH)
	pop2 = create_population(POP_SIZE,LENGTH)
	# objective fintesses for this gen's pop1
	gen_obj_fitnesses1 = [obj_fitness(member) for member in pop1]
	# objective fitnesses for this gen's pop2
	gen_obj_fitnesses2 = [obj_fitness(member) for member in pop2]
	obj_fitnesses.append(gen_obj_fitnesses1+gen_obj_fitnesses2)

	# create a list of tuples containing members with their subjective fitnesses
	pop1_fit = zip(pop1, gen_subj_fitnesses1)
	pop2_fit = zip(pop2, gen_subj_fitnesses2)
	for i in range(0,generations):
		# print pop1_fit
		# print pop2_fit

		# subjective fitnesses for this generation's population 1
		gen_subj_fitnesses1 = exp1_subj_fitness_pop(pop1_fit,pop2_fit) # double check the logic of this function
		# subjective fitnesses for this generation's population 2
		gen_subj_fitnesses2 = exp1_subj_fitness_pop(pop2_fit,pop1_fit)

		subj_fitnesses1.append(gen_subj_fitnesses1)
		subj_fitnesses2.append(gen_subj_fitnesses2)

		# create new pops and calc obj fitnesses
		child_objs = tournament_selection([pop1_fit, pop2_fit], MUTATION_BIAS)
		gen_obj_fitnesses1[child_objs[0][1]] = child_objs[0][0]
		gen_obj_fitnesses2[child_objs[1][1]] = child_objs[1][0]
		obj_fitnesses.append(gen_obj_fitnesses1+gen_obj_fitnesses2)
		pop1 = list(zip(*pop1_fit)[0])
		pop2 = list(zip(*pop2_fit)[0])
		#print len(pop1)
		#print len(pop2)
		#print i
	return [obj_fitnesses, subj_fitnesses1, subj_fitnesses2]

