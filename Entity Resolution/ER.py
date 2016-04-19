import re, math
from collections import Counter
from requests import get


WORD = re.compile(r'\w+')
url="http://swoogle.umbc.edu/StsService/GetStsSim?"
operation="operation=api&"

symp_list=[]
symptoms_list=[]
symp_similar=[]
final_list=[]
i=0

def cosine_similarity(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator


def semantic_similarity(p1,p2):
    phrase1="phrase1="+p1+"&"
    phrase2="phrase2="+p2

    s=url+operation+phrase1+phrase2
    sem=s.replace(' ','%20')
    response=get(sem)
    return response.text.strip()


def tokenize(text):
     words = WORD.findall(text)
     return Counter(words)


def textual_similarity(text1,text2):
    vector1 = tokenize(text1.lower())
    vector2 = tokenize(text2.lower())
    cosine = cosine_similarity(vector1, vector2)
    return cosine


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def deduplicate():
    with open("symptoms.txt") as file:
        lists=file.readlines()
        for i in range(len(lists)):
            symp_list.append(lists[i].rstrip('\n').rstrip('\r').rstrip('\t'))

    symptoms_list=list(set(symp_list))
    # print symptoms_list
    f=open('symptoms-similar.txt','w')

    for item in symptoms_list:
        del symp_similar[:]
        symp_similar.append(item)
        for item_next in symptoms_list:
            if item==item_next or symptoms_list.index(item_next)<=symptoms_list.index(item):
                continue
            text_sim=textual_similarity(item,item_next)
            semantic_val=semantic_similarity(item,item_next)
            if isfloat(semantic_val):
                semantic_sim=float(semantic_val)
            else:
                semantic_sim=0.0
            # print item,item_next,text_sim,semantic_sim
            if text_sim>0.7:
                similarity=text_sim
            else:
                similarity=semantic_sim
            if similarity>0.5:
                symp_similar.append(item_next)
                symptoms_list.remove(item_next)
        if len(symp_similar)>1:
            #print symp_similar
            f.write("\t".join(symp_similar))
            f.write("\n")
            symptoms_list.remove(item)
        print len(symptoms_list)
    for item in symptoms_list:
        f.write(str(item)+"\n")


deduplicate()




