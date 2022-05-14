import json
import pandas as pd
from tqdm import tqdm
import jieba


def laic2cail(df, data_name):
    data = []
    for i in tqdm(range(len(df))):
        json_obj = {}

        charge = df["charge"][i]
        # if charge == "非法生产、买卖、运输制毒物品、走私制毒物品罪":
        #     charge = "非法买卖制毒物品"
        
        charge = charge.replace("[", "").replace("]", "").replace("罪", "")
        if charge == '制造、贩卖、传播淫秽物品':
            charge = '传播淫秽物品'
        if charge == '组织、强迫、引诱、容留、介绍卖淫':
            charge = "引诱、容留、介绍卖淫"
        if charge == "掩饰、隐瞒犯所得、犯所得收益":
            charge = "掩饰、隐瞒犯罪所得、犯罪所得收益"

        article = df["article"][i]

        # json_obj["fact"] = " ".join(jieba.lcut(df["justice"][i]))
        json_obj["fact"] = df["justice"][i]
        json_obj["meta"] = {
            'accusation': [charge],
            'relevant_articles': [int(article)],
            'term_of_imprisonment': {
                'imprisonment': int(df["judge"][i]),
                'death_penalty': False,
                'life_imprisonment': False,
            }
        }
        data.append(json.dumps(json_obj, ensure_ascii=False))

    with open("{}.json".format(data_name), "w") as f:
        for line in data:
            f.write(line+"\n")


def trans_cail(data_name):
    charge_tong = json.load(open("../charge_tong.json"))
    article_tong = json.load(open("../art_tong.json"))

    data = []
    with open("{}.json".format(data_name)) as f:
        for line in tqdm(f.readlines()):
            line = json.loads(line)
            data.append(line)
    print(len(data))

    new_data = []
    for line in data:
        charge = line['meta']['accusation'][0]
        article = line['meta']['relevant_articles'][0]
        if charge not in charge_tong.keys():
            continue
        if str(article) not in article_tong.keys():
            continue
        new_data.append(line)
    print(len(new_data))
    with open("{}.json".format(data_name), "w") as f:
        for line in new_data:
            line = json.dumps(line, ensure_ascii=False)
            f.write(line+"\n")


df = pd.read_csv("cail_small_sc2.csv")
df_train = df[df["split"] == 0]
df_valid = df[df["split"] == 1]
df_test = df[df["split"] == 2]


print(df["split"].value_counts())
split = ["train", "valid", "test"]
# split = ["valid"]

data = {
    split[i]: df[df["split"] == i].reset_index().drop(["index"], axis=1) for i in range(len(split))
}
for data_name in split:
    laic2cail(data[data_name], data_name)
    trans_cail(data_name)
