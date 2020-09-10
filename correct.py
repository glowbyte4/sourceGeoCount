import json
import math

fin = open('result.json', 'r')
res = fin.read()
max = 0
corr = []
for item in json.loads(res):
    weight = (item['weight'])
    if item['weight'] > max:
        max = item['weight']
    if weight > 2:
        item['weight'] = math.log2(weight)
    corr.append(item)

fout = open('corr_ratings1.json', 'w')
fout.write(json.dumps(corr))
print(max)