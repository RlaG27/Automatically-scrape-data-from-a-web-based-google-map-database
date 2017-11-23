pairs = [['a', 1], ['b', 2], ['c', 3]]

d = {}
for key, value in pairs:
    if key not in d:
         d[key] = []
    d[key].append(value)

print(d)

import random

pairs = [[random.randint(1, 100), random.randint(1, 100)] for i in range(100)]
#pairs = sorted(pairs, key = lambda x: (x[0], x[1]))

first_elm = []
for i, row in enumerate(pairs):
    print(i, row)
    if row[0] not in first_elm:
        first_elm.append(row[0])


import statistics
print(statistics.median_low(pairs))
