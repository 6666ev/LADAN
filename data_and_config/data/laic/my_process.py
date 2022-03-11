import json
import pandas as pd
import os



def chinese2arabic(cn: str) -> int:
    CN_NUM = {
        '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0,
        '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2,
    }

    CN_UNIT = {
        '十': 10, '拾': 10, '百': 100, '佰': 100, '千': 1000, '仟': 1000, '万': 10000, '萬': 10000, '亿': 100000000, '億': 100000000, '兆': 1000000000000,
    }
    unit = 0   # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            dig = CN_NUM.get(cndig)
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val

flaw = open("../law.txt", 'r')
totallaw = 0
law2num = {}
for line in flaw.readlines():
    law2num[line.strip()] = totallaw
    totallaw += 1

def laic2cail(dataset="train"):
    df = pd.read_csv("%s.csv" % dataset)
    data = []
    skip_law = 0
    for i in range(len(df)):
        fact = df["justice"][i]
        judge = df["judge"][i]
        charge = df["charge"][i].replace("罪","")
        article = chinese2arabic(df["article"][i])
        if charge == "非法生产、买卖、运输制毒物品、走私制毒物品":
            charge = "非法买卖制毒物品"
        if str(article) not in law2num.keys():
            skip_law+=1
            continue
            
        json_obj = {
            "fact":fact,
            "meta":{
                "accusation":[charge],
                "relevant_articles":[article],
                "term_of_imprisonment":{
                    "death_penalty":False,
                    "imprisonment":int(judge),
                    "life_imprisonment":False
                }
            }
        }

        json_str = json.dumps(json_obj, ensure_ascii=False)
        data.append(json_str)
    print(skip_law)

    with open("data_%s.json" % dataset,"w") as f:
        for line in data:
            f.write(line+"\n")

laic2cail("train")
laic2cail("valid")
laic2cail("test")
    