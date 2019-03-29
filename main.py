from engine import Engine

eng = Engine(population_size=100,
             mutation_rate=.8,
             keep_best=True,
             survival_rate=.5,
             selection_method='tournament',
             crossover_method='pmx',
             mutation_method='inverse',
             knapsack_method='greedy',
             greedy_type='static',
             tournament_size=60)

eng.load_data('medium_0.ttp')

eng.run(generations=1000, info_every=10, visualize_result=True)
