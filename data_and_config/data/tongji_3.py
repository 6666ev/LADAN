import json
import thulac
import re
import random
from tqdm import tqdm
import os

Cutter = thulac.thulac(seg_only=True)

flaw = open("./law.txt", 'r')
totallaw = 0
law2num = {}
num2law = {}

for line in flaw.readlines():
    law2num[line.strip()] = totallaw
    num2law[totallaw] = line.strip()
    totallaw += 1
print(totallaw)

flaw = open("accu.txt", 'r', encoding='utf-8')
totalaccu = 0
accu2num = {}
num2accu = {}
for line in flaw.readlines():
    accu2num[line.strip()] = totalaccu
    num2accu[totalaccu] = line.strip()
    totalaccu += 1
print(totalaccu)

file1 = open("cail_small_sc/train.json", 'r', encoding='utf-8')
file2 = open("cail_small_sc/test.json", 'r', encoding='utf-8')
file3 = open("cail_small_sc/valid.json", 'r', encoding='utf-8')

strpass = '二审'
totalsample = 0
totlaw = [0] * totallaw
totaccu = [0] * totalaccu

train_set = file1.readlines()
random.seed(88)
random.shuffle(train_set)

for line in train_set:
    dic = json.loads(line)
    # if (strpass in dic["fact"] != -1 or len(dic["meta"]["accusation"]) > 1 or len(dic["meta"]["relevant_articles"]) > 1):
    #     pass
    # else:
    templaw = str(dic["meta"]["relevant_articles"][0])
    tempaccu = dic["meta"]["accusation"][0]
    tempaccu = tempaccu.replace("[", "").replace("]", "")
    totlaw[law2num[templaw]] += 1
    totaccu[accu2num[tempaccu]] += 1
    totalsample += 1


for line in file3.readlines():
    dic = json.loads(line)
    # if (strpass in dic["fact"] != -1 or
    #         len(dic["meta"]["accusation"]) > 1 or len(dic["meta"]["relevant_articles"]) > 1):
    #     pass
    # else:
    templaw = str(dic["meta"]["relevant_articles"][0])
    tempaccu = dic["meta"]["accusation"][0]
    tempaccu = tempaccu.replace("[", "").replace("]", "")
    totlaw[law2num[templaw]] += 1
    totaccu[accu2num[tempaccu]] += 1
    totalsample += 1


print(totalsample)
clearlaw = 0
clearaccu = 0
clearlawlist = []
clearacculist = []
clearlaw2num = {}
clearaccu2num = {}

lawfile = open("./new_law.txt", "w")
accufile = open("./new_accu.txt", "w")

for i in range(totallaw):
    # if totlaw[i] >= 100:
    clearlawlist.append(i)
    clearlaw2num[str(num2law[i])] = clearlaw
    clearlaw += 1
    lawfile.write(num2law[i] + '\n')
for i in range(totalaccu):
    # if totaccu[i] >= 100:
    clearacculist.append(i)
    clearaccu2num[num2accu[i]] = clearaccu
    clearaccu += 1
    accufile.write(num2accu[i] + '\n')

print(clearlaw, clearaccu)
print(clearlaw2num)


file1.close()
file2.close()
file3.close()



# longest = 0

regex_list = [
    (r"(经审理查明|公诉机关指控|检察院指控|起诉书指控|指控)([，：,:]?)([\s\S]*)([，。,]?)(足以认定|就上述指控|上述事实)", 2),
    (r"(经审理查明|公诉机关指控|检察院指控|起诉书指控|指控)([，：,:]?)([\s\S]*)([，。,]?)(足以认定|就上述指控|上述事实)", 2),
    (r"(经审理查明|公诉机关指控|检察院指控|起诉书指控|指控)([，：,:]?)([\s\S]*)$", 2),
    (r"^([\s\S]*)([，。,]?)(足以认定|就上述指控|上述事实)", 0)
]


def format_string(s):
    return s.replace("b", "").replace("\t", " ").replace("t", "")

def process_split_data(file1, outputfile1):
    totaltrain = 0 
    for line in tqdm(file1.readlines()):
        dic = json.loads(line)
        # if totaltrain > 1000:
        #     break
        # if (strpass in dic["fact"] != -1 or
        #         len(dic["meta"]["accusation"]) > 1 or len(dic["meta"]["relevant_articles"]) > 1):
        #     pass
        # else:
        templaw = str(dic["meta"]["relevant_articles"][0])
        tempaccu = dic["meta"]["accusation"][0]
        tempaccu = tempaccu.replace("[", "").replace("]", "")

        if (law2num[templaw] in clearlawlist and accu2num[tempaccu] in clearacculist):
            totaltrain += 1
            # if (dic["meta"]["term_of_imprisonment"]["imprisonment"] > longest):
            #     longest = dic["meta"]["term_of_imprisonment"]["imprisonment"]
    #            if dic["meta"]["term_of_imprisonment"]["death_penalty"] == True or dic["meta"]["term_of_imprisonment"]["life_imprisonment"] == True:
    #                print (dic)

            fact = dic['fact']
            s = format_string(fact)

            for reg, num in regex_list:
                regex = re.compile(reg)
                result = re.findall(regex, s)
                if len(result) > 0:
                    fact = result[0][num]
                    break
            fact_cut = Cutter.cut(fact.strip(), text=True)

            # fact_cut = dic["fact"]
            sample_new = {}
    #            sample_new["fact"] = dic["fact"].strip()
            sample_new["fact_cut"] = fact_cut
            tempaccu = dic["meta"]["accusation"][0].replace(
                "[", "").replace("]", "")
            sample_new["accu"] = clearaccu2num[tempaccu]
            sample_new["law"] = clearlaw2num[str(
                dic["meta"]["relevant_articles"][0])]
            tempterm = dic["meta"]["term_of_imprisonment"]
            sample_new["time"] = tempterm["imprisonment"]
            sample_new["term_cate"] = 2
            sn = json.dumps(sample_new, ensure_ascii=False) + '\n'
            outputfile1.write(sn)
            # if (totaltrain % 100 == 0):
            #     print(totaltrain)
    print(totaltrain)

file1 = open("cail_small_sc/train.json", 'r', encoding='utf-8')
file2 = open("cail_small_sc/test.json", 'r', encoding='utf-8')
file3 = open("cail_small_sc/valid.json", 'r', encoding='utf-8')

outputfile1 = open("cail_small_sc/train_cs.json", "w", encoding='utf-8')
outputfile2 = open("cail_small_sc/test_cs.json", "w", encoding='utf-8')
outputfile3 = open("cail_small_sc/valid_cs.json", "w", encoding='utf-8')

process_split_data(file1, outputfile1)
process_split_data(file2, outputfile2)
process_split_data(file3, outputfile3)
