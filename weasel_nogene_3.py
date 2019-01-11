# Python implementation of Richard Dawkin's weasel program
# Illustrates power of cumulative selection vs entirely random search
# This version allows all positions to mutate in any generation, meaning correct letters can be reversed

# Initializations
import sys, random
target = list("METHINKS IT IS LIKE A WEASEL")   # Target sequence
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "        # Alphabet of possible symbols (uppercase letters + blank)
n_offspring = 50                                # Number of offspring per generation
mut_rate = 0.08                                 # Mutation rate: probability that any given letter will change
best_offspring = []                             # Variable containing best offspring after each generation
                                                # Contains empty list when loop is first entered

# Construct random starting string of same length as target
parent = []
for i in range(len(target)):
    parent.append(random.choice(alphabet))

# Main loop: construct mutated offspring, select best for next generation, stop when target reached
gen = 0
while best_offspring != target:
    gen = gen + 1

    # Keep track of the number of good, bad, and neutral mutations arising in this generation
    n_beneficial = n_detrimental = n_neutral = num_mut = 0.0

    # Keep track of how many kids in current generation that look exactly like their parent
    num_unchanged = n_offspring

    # Construct n_offspring children that may contain mutations
    kid_list = []
    for i in range(n_offspring):

        # Copy content of parent to kid
        kid = parent[:]

        # Iterate over positions in kid, for each position allow possibility of mutating
        kid_changed = False
        for pos in range(len(kid)):

            # Let residue mutate with probability mut_rate
            if random.random() < mut_rate:
                kid_changed = True
                num_mut += 1

                # Randomly select new symbol (that is different from the one already present)
                old_symbol = parent[pos]
                possible_new_symbols = set(alphabet) - set(old_symbol)
                new_symbol = random.choice(list(possible_new_symbols))

                # Mutate kid
                kid[pos] = new_symbol

                # Check if mutation was beneficial, detrimental, or neutral and update count
                if old_symbol == target[pos]:           # Correct letter has been changed: detrimental
                    n_detrimental += 1
                elif new_symbol == target[pos]:         # Incorrect letter has been changed to correct: beneficial
                    n_beneficial += 1
                else:                                   # Incorrect letter has been changed to other incorrect letter: neutral
                    n_neutral += 1

        # If kid was mutated, then it no longer looks like its parent
        if kid_changed:
            num_unchanged -= 1

        # Add (possibly) mutated kid to list of current kids
        kid_list.append(kid)


    # Find most fit offspring (= string most similar to target)
    smallest_dif = len(target) + 1
    for kid in kid_list:

        # Find number of positions that differ between kid and target
        dif = 0.0
        for pos in range(len(target)):
            if kid[pos] != target[pos]:
                dif = dif + 1

        # Keep best kid found so far
        if dif < smallest_dif:
            smallest_dif = dif
            best_offspring = kid

    # Use best offspring as starting point for next round of mutation
    parent = best_offspring

    # Print progress
    fitness = (len(target)-smallest_dif)/len(target)            # Fitness of most fit individual
    ben_frac = n_beneficial/num_mut
    detr_frac = n_detrimental/num_mut
    neu_frac = n_neutral/num_mut
    result_string = ""
    for pos in range(len(target)):
        if best_offspring[pos] == target[pos]:
            result_string += best_offspring[pos]
        else:
            result_string += best_offspring[pos].lower()
    print ("Gen: %4d   Dif: %3d   Fit: %.4f   Bene: %.4f  Detr: %.4f  Neu: %.4f   Unchanged: %3d" % (gen, smallest_dif, fitness,
                                                                                                ben_frac, detr_frac, neu_frac,
                                                                                                num_unchanged))

