from engine import Engine

eng = Engine(population_size=100,
             mutation_rate=.1,
             keep_best=True,
             selection_method='roulette',
             crossover_method='simple',
             mutation_method='swap',
             knapsack_method='greedy')

eng.load_data('easy_1.ttp')

eng.run(generations=100, info_every=10, visualize_result=True)
