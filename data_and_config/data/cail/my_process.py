import json

from attr import dataclass

data = []
zm = []
with open("data_tot.json") as f:
    for line in f.readlines():
        json_obj = json.loads(line)
        data.append(json_obj)
        charge = json_obj["meta"]["accusation"]
        if len(charge) > 1:
            zm.append(charge)

# print(zm)
print(len(data))
print(len(zm))