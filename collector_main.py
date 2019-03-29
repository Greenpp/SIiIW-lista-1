from collector import Collector, Test

SAMPLE_SIZE = 10
PARAMS = {'generations': 250}


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

test_mut_swap = Test(mutable_param='mutation_rate',
                     values=[i / 10 for i in range(11)],
                     sample=SAMPLE_SIZE,
                     parameters={'generations': 250, 'mutation_method': 'swap'})
test_mut_inv = Test(mutable_param='mutation_rate',
                    values=[i / 10 for i in range(11)],
                    sample=SAMPLE_SIZE,
                    parameters={'generations': 250, 'mutation_method': 'inverse'})
test_mut_shuf = Test(mutable_param='mutation_rate',
                     values=[i / 10 for i in range(11)],
                     sample=SAMPLE_SIZE,
                     parameters={'generations': 250, 'mutation_method': 'shuffle'})
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
test_pop = Test(mutable_param='population_size',
                values=range(100, 1001, 100),
                sample=SAMPLE_SIZE,
                parameters=PARAMS)
test_sel = Test(mutable_param='selection_method',
                values=['tournament', 'roulette'],
                sample=SAMPLE_SIZE,
                parameters=PARAMS)
test_gen = Test(mutable_param='generations',
                values=range(100, 1001, 100),
                sample=SAMPLE_SIZE,
                parameters=dict())
test_random = Test(mutable_param='selection_method',
                   values=['random', 'tournament'],
                   sample=SAMPLE_SIZE,
                   parameters=PARAMS)

# distribute tests
# distribute_test(collectors, test_mut_swap) # done
# distribute_test(collectors, test_mut_inv) # done
# distribute_test(collectors, test_mut_shuf) # done
# distribute_test(collectors, test_surv) # done
# distribute_test(collectors, test_cros_met) # done
# distribute_test(collectors, test_greed) TODO fix
# distribute_test(collectors, test_tour) # done
# distribute_test(collectors, test_pop) # done
# distribute_test(collectors, test_sel) # done
# distribute_test(collectors, test_gen) # done
# distribute_test(collectors, test_random) # done

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
    print(15 * '=' + ' ' + c.data_file + ' ' + 15 * '=')
    c.init()
    c.run()
    c.close()
