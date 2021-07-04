from numpy.random import randint
from numpy.random import rand
 
# fonction objective
def objective(x):
	return x[0]**2.0 + x[1]**2.0
 
# décode la chaîne de bits en nombres
def decode(bounds, n_bits, bitstring):
	decoded = list()
	largest = 2**n_bits
	for i in range(len(bounds)):
		# extraire la sous-chaîne
		start, end = i * n_bits, (i * n_bits)+n_bits
		substring = bitstring[start:end]
		# convertir une chaîne de bits en une chaîne de caractères
		chars = ''.join([str(s) for s in substring])
		# convertir une chaîne de caractères en un nombre entier
		integer = int(chars, 2)
		value = bounds[i][0] + (integer/largest) * (bounds[i][1] - bounds[i][0])
		decoded.append(value)
	return decoded
 
# Sélection pour le tournoi
def selection(pop, scores, k=3):
	# première sélection aléatoire
	selection_ix = randint(len(pop))
	for ix in randint(0, len(pop), k-1):
		# vérifier si c'est mieux (par exemple, effectuer un tournoi)
		if scores[ix] < scores[selection_ix]:
			selection_ix = ix
	return pop[selection_ix]
 
# croisement de deux parents pour créer deux enfants
def crossover(p1, p2, r_cross):
	# les enfants sont des copies des parents par défaut
	c1, c2 = p1.copy(), p2.copy()
	# vérifier la recombinaison
	if rand() < r_cross:
		# Sélectionnez un point de croisement qui n'est pas à l'extrémité de la chaîne.
		pt = randint(1, len(p1)-2)
		# effectuer le crossover
		c1 = p1[:pt] + p2[pt:]
		c2 = p2[:pt] + p1[pt:]
	return [c1, c2]
 
# Opérateur de mutation
def mutation(bitstring, r_mut):
	for i in range(len(bitstring)):
		# vérifier la présence d'une mutation
		if rand() < r_mut:
			# Retourner le bit
			bitstring[i] = 1 - bitstring[i]
 
# algorithme génétique
def genetic_algorithm(objective, bounds, n_bits, n_iter, n_pop, r_cross, r_mut):
	# population initiale de chaînes de bits aléatoires
	pop = [randint(0, 2, n_bits*len(bounds)).tolist() for _ in range(n_pop)]
	# garder la trace de la meilleure solution
	best, best_eval = 0, objective(decode(bounds, n_bits, pop[0]))
	# énumérer les générations
	for gen in range(n_iter):
		# décoder la population
		decoded = [decode(bounds, n_bits, p) for p in pop]
		# évaluer tous les candidats de la population
		scores = [objective(d) for d in decoded]
		# vérifier la nouvelle meilleure solution
		for i in range(n_pop):
			if scores[i] < best_eval:
				best, best_eval = pop[i], scores[i]
				print(">%d, new best f(%s) = %f" % (gen,  decoded[i], scores[i]))
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
 
# définir la plage pour l'entrée
bounds = [[-5.0, 5.0], [-5.0, 5.0]]
# définir le nombre total d'itérations
n_iter = 100
# Nombre de bits par variable
n_bits = 16
# définir la taille de la population
n_pop = 100
# Taux de crossover
r_cross = 0.9
# Taux de mutation
r_mut = 1.0 / (float(n_bits) * len(bounds))
# effectuer la recherche par algorithme génétique
best, score = genetic_algorithm(objective, bounds, n_bits, n_iter, n_pop, r_cross, r_mut)
print('Done!')
decoded = decode(bounds, n_bits, best)
print('f(%s) = %f' % (decoded, score))