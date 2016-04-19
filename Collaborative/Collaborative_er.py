import re, math
from collections import Counter
from requests import get


WORD = re.compile(r'\w+')
url="http://swoogle.umbc.edu/StsService/GetStsSim?"
operation="operation=api&"



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


similar_list=[]

def find_similar_symptoms(user_symptom):
    file=open('/home/soorya/Treatment-Recommender/Code/symptoms_similar.txt','r')
    for line in file:
        line=line.rstrip('\n')
        symptoms_file=line.split('\t')
        for symp in user_symptom:
            if symp==symptoms_file[0]:
                for item in symptoms_file:
                    similar_list.append(item)
                break
            text_sim=textual_similarity(symp,symptoms_file[0])
            semantic_val=semantic_similarity(symp,symptoms_file[0])            
            if isfloat(semantic_val):
                semantic_sim=float(semantic_val)
            else:
                semantic_sim=0.0
            if text_sim>0.75 or semantic_sim>0.55:
                for item in symptoms_file:
                    similar_list.append(item)
                break
    return similar_list


#print find_similar_symptoms(['sleeplessness','nervous'])
