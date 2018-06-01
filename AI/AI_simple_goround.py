def play(stat, storage):
    core = storage['core']
    return core.get_next()


def load(stat, storage):
    class square_loop:
        def __init__(self):
            self.cur = 0
            self.max = 2
            self.edges = 0

        def get_next(self):
            self.cur += 1
            if self.cur >= self.max:
                self.cur = 0
                self.edges += 1
                if self.edges >= 3:
                    self.edges = 0
                    self.max += 1
                return 'l'

    storage['core'] = square_loop()
