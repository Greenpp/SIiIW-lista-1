# from engine import Engine
#
# eng = Engine(population_size=100,
#              mutation_rate=1,
#              keep_best=True,
#              survival_rate=0,
#              selection_method='tournament',
#              crossover_method='pmx',
#              mutation_method='inverse',
#              knapsack_method='greedy',
#              greedy_type='static',
#              tournament_size=30)
#
# eng.load_data('hard_0.ttp')
#
# eng.run(generations=100, info_every=10, visualize_result=True)

from collector import Collector, Test

SAMPLE_SIZE = 10
PARAMS = {'generations': 200}


def distribute_test(cols, t):
    for col in cols:
        col.add_test(t)


# create collector for every file type
ct = Collector('trivial_0.ttp')
ce = Collector('easy_0.ttp')
cm = Collector('medium_0.ttp')
ch = Collector('hard_0.ttp')

collectors = [ct, ce, cm, ch]

# create tests

test_mut = Test(mutable_param='mutation_rate',
                values=[i / 10 for i in range(11)],
                sample=SAMPLE_SIZE,
                parameters=PARAMS)
test_surv = Test(mutable_param='survival_rate',
                 values=[i / 10 for i in range(11)],
                 sample=SAMPLE_SIZE,
                 parameters=PARAMS)
test_cros_met = Test(mutable_param='crossover_method',
                     values=['simple', 'ox', 'cx', 'pmx'],
                     sample=SAMPLE_SIZE,
                     parameters=PARAMS)
test_greed = Test(mutable_param='greedy_type',
                  values=['static', 'dynamic'],
                  sample=SAMPLE_SIZE,
                  parameters=PARAMS)
test_tour = Test(mutable_param='tournament_size',
                 values=([1] + list(range(10, 101, 10))),
                 sample=SAMPLE_SIZE,
                 parameters=PARAMS)

# distribute tests
distribute_test(collectors, test_mut)
distribute_test(collectors, test_surv)
distribute_test(collectors, test_cros_met)
distribute_test(collectors, test_greed)
distribute_test(collectors, test_tour)

# estimate execution time
total_time = 0
for c in collectors:
    total_time += c.estimate_time()

h = total_time // 3600
total_time -= (h * 3600)
m = total_time // 60
total_time -= (m * 60)
s = total_time
print('Estimated time: {:02}:{:02}:{:02}'.format(h, m, s))

if input('Continue?[y/n]: ') != 'y':
    exit(0)

# execute
for c in collectors:
    print(25 * '=')
    c.init()
    c.run()
    c.close()
