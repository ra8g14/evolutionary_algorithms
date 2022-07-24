def run(length, dimensions, eq, generations, filename):
	obj_fitnesses =[[0 for i in range(0,POP_SIZE*2)]]
	# initialise populations and subj fitnesses
	pop1 = create_population(length, POP_SIZE, dimensions)
	pop2 = create_population(length, POP_SIZE, dimensions)
	subj_fitnesses1 = [[0 for i in range(0,POP_SIZE)]]
	subj_fitnesses2 = [[0 for i in range(0,POP_SIZE)]]
	# create a list of tuples containing members with their subjective fitnesses
	pop1_fit = zip(pop1, subj_fitnesses1[0])
	pop2_fit = zip(pop2, subj_fitnesses2[0])
	for i in range(0,generations):
		# make a new generation - use fitness proportionate selection to mutate a new parent
		pop1_fit = make_new_gen(pop1_fit, MUTATION_BIAS)
		pop2_fit = make_new_gen(pop2_fit, MUTATION_BIAS)
		# calculate new objective fitnesses for new populations
		obj_fitnesses_next = []
		for mem in pop1_fit:
			obj_fitnesses_next.append(obj_fitness(mem[0]))
		for mem in pop2_fit:
			obj_fitnesses_next.append(obj_fitness(mem[0]))
		obj_fitnesses.append(obj_fitnesses_next)
		# calc new subjective fitnesses for each member in both populations
		fitnesses1 = exp2_subj_fitness_pop(pop1_fit,pop2_fit,eq)
		pop1_fit = zip(list(zip(*pop1_fit)[0]), fitnesses1)
		fitnesses2 = exp2_subj_fitness_pop(pop2_fit,pop1_fit,eq)
		pop2_fit = zip(list(zip(*pop2_fit)[0]), fitnesses2)
		subj_fitnesses1.append(fitnesses1)
		subj_fitnesses2.append(fitnesses2)
	with open(filename + ".csv", "a") as fp:
		wr = csv.writer(fp, dialect='excel')
		wr.writerows(obj_fitnesses)
	with open(filename + "_subj_fitnesses" + ".csv", "a") as fp:
		wr = csv.writer(fp, dialect='excel')
		wr.writerows(subj_fitnesses1)
		wr.writerow("\n")
		wr.writerows(subj_fitnesses2)
	return [obj_fitnesses, subj_fitnesses1, subj_fitnesses2, pop1_fit, pop2_fit]