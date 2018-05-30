def play(stat, storage):
    storage['cur'] += 1
    if storage['cur'] >= storage['max']:
        storage['cur'] = 0
        storage['edges'] += 1
        if storage['edges'] >= 3:
            storage['edges'] = 0
            storage['max'] += 1
        return 'l'


def load(storage):
    storage['cur'] = 0
    storage['max'] = 2
    storage['edges'] = 0
