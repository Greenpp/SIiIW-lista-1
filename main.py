from engine import Engine

eng = Engine(10)

eng.load_data('trivial_1.ttp')
eng.init()

eng.greedy_item_select()

eng.test()
eng.sort()
