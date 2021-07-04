# genetic algorithm
def genetic_algorithm(objective, n_bits, n_iter, n_pop, r_cross, r_mut):
	# population initiale de chaînes de bits aléatoires
	pop = [randint(0, 2, n_bits).tolist() for _ in range(n_pop)]
	# garder la trace de la meilleure solution
	best, best_eval = 0, objective(pop[0])
	# énumérer les générations
	for gen in range(n_iter):
		# évaluer tous les candidats de la population
		scores = [objective(c) for c in pop]
		# vérifier la nouvelle meilleure solution
		for i in range(n_pop):
			if scores[i] < best_eval:
				best, best_eval = pop[i], scores[i]
				print(">%d, new best f(%s) = %.3f" % (gen,  pop[i], scores[i]))
		# sélectionner les parents
		selected = [selection(pop, scores) for _ in range(n_pop)]
		# créer la prochaine génération
		children = list()
		for i in range(0, n_pop, 2):
			# obtenir les parents sélectionnés en paires
			p1, p2 = selected[i], selected[i+1]
			# Crossover et mutation
			for c in crossover(p1, p2, r_cross):
				# mutation
				mutation(c, r_mut)
				# stocker pour la prochaine génération
				children.append(c)
		# remplacer la population
		pop = children
	return [best, best_eval]