import random
random
data_str = []
with open("data_tot.json") as f:
    for line in f.readlines():
        data_str.append(line)

# print(len(data_str))
random.shuffle(data_str)

train = data_str[:10000]
test = data_str[10000:11000]
valid = data_str[11000:12000]

with open("data_train.json", "w") as f:
    for line in train:
        f.write(line)
with open("data_valid.json", "w") as f:
    for line in valid:
        f.write(line)
with open("data_test.json", "w") as f:
    for line in test:
        f.write(line)
