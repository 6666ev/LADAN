import pandas as pd
import json


df = pd.read_csv("cail_small_sc2.csv")

def get_json_data(path):    
    with open(path) as f:
        dataset = []
        for line in f.readlines():
            json_obj = json.loads(line)
            dataset.append(json_obj)
        return dataset
    return dataset


trainset = get_json_data("train.json")
validset = get_json_data("valid.json")
testset = get_json_data("test.json")

def add_3label(json_data, split=0):
    year = df[df["split"]==split]["year"].tolist()
    year = df[df["split"]==split]["charge"].tolist()
    year = df[df["split"]==split]["province"].tolist()