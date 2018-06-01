def play(stat, storage):
    from random import choice
    stat=stat['now']
    me = stat['me']
    d = storage['directions'][me['direction']]
    if stat['fields'][me['x']][me['y']] == me['id']:
        if stat['fields'][me['x'] + d[0]][me['y'] + d[1]] != me['id']:
            return ''
        return 'r'
    return 'l'


def load(stat, storage):
    storage['directions'] = [(1, 0), (0, 1), (-1, 0), (0, -1)]
