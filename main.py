from engine import Engine

eng = Engine(100)

eng.load_data('easy_1.ttp')
eng.greedy_item_select(method='ratio')

eng.init()

for i in range(1000):
    print('Best fitness: {}'.format(eng.population[0].fitness))
    eng.next_generation()

eng.plot_data()
