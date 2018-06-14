import os
for group in 'N17', 'F17':
    for patch in 'E/W/S/N/E1W2/S1N2/E2W1/S2N1/E1W2S1N2/E2W1S2N1'.split('/'):
        path = os.path.join(group, patch, 'log')
        name = '%s-%s.tgz' % (group, patch)
        command = 'cd %s; tar -czf %s *.zlog' % (path, name)
        print('>', command)
        os.system(command)
