from engine import Engine

eng = Engine(population_size=100,
             mutation_rate=.1,
             keep_best=True,
             selection_method='tournament',
             crossover_method='pmx',
             mutation_method='inverse',
             knapsack_method='greedy',
             tournament_size=15)

eng.load_data('hard_1.ttp')

eng.run(fitness=0, info_every=10, visualize_result=True)
