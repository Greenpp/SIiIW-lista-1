from engine import Engine

eng = Engine()
eng.load_data('easy_1.ttp')

eng.run(generations=1000, info_every=10)
