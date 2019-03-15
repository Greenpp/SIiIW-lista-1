from engine import Engine

eng = Engine(population_size=100,
             mutation_rate=.8,
             keep_best=True,
             survival_rate=0,
             selection_method='tournament',
             crossover_method='pmx',
             mutation_method='inverse',
             knapsack_method='greedy',
             greedy_type='dynamic',
             tournament_size=15)

eng.load_data('easy_1.ttp')

eng.run(generations=100, info_every=10, visualize_result=True)
