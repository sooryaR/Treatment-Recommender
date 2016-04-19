from __future__ import division
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
import math
import numpy as np
import sys
import re, math
from collections import Counter
from requests import get


ALPHA = 0.2
BETA = 0.45
ETA = 0.4
PHI = 0.2
DELTA = 0.85

brown_freqs = dict()
N = 0

WORD = re.compile(r'\w+')
symp_list=[]
symptoms_list=[]
symp_similar=[]
final_list=[]
i=0
threshold_val=0.4

def get_best_synset_pair(word_1, word_2):
    max_sim = -1.0
    synsets_1 = wn.synsets(word_1)
    synsets_2 = wn.synsets(word_2)
    if len(synsets_1) == 0 or len(synsets_2) == 0:
        return None, None
    else:
        max_sim = -1.0
        best_pair = None, None
        for synset_1 in synsets_1:
            for synset_2 in synsets_2:
               sim = wn.path_similarity(synset_1, synset_2)
               if sim > max_sim:
                   max_sim = sim
                   best_pair = synset_1, synset_2
        return best_pair

def length_dist(synset_1, synset_2):
    
    l_dist = sys.maxint
    if synset_1 is None or synset_2 is None: 
        return 0.0
    if synset_1 == synset_2:
        l_dist = 0.0
    else:
        wset_1 = set([str(x.name()) for x in synset_1.lemmas()])        
        wset_2 = set([str(x.name()) for x in synset_2.lemmas()])
        if len(wset_1.intersection(wset_2)) > 0:
            l_dist = 1.0
        else:
            l_dist = synset_1.shortest_path_distance(synset_2)
            if l_dist is None:
                l_dist = 0.0
    return math.exp(-ALPHA * l_dist)

def hierarchy_dist(synset_1, synset_2):

    h_dist = sys.maxint
    if synset_1 is None or synset_2 is None: 
        return h_dist
    if synset_1 == synset_2:
        # return the depth of one of synset_1 or synset_2
        h_dist = max([x[1] for x in synset_1.hypernym_distances()])
    else:
        # find the max depth of least common subsumer
        hypernyms_1 = {x[0]:x[1] for x in synset_1.hypernym_distances()}
        hypernyms_2 = {x[0]:x[1] for x in synset_2.hypernym_distances()}
        lcs_candidates = set(hypernyms_1.keys()).intersection(
            set(hypernyms_2.keys()))
        if len(lcs_candidates) > 0:
            lcs_dists = []
            for lcs_candidate in lcs_candidates:
                lcs_d1 = 0
                if hypernyms_1.has_key(lcs_candidate):
                    lcs_d1 = hypernyms_1[lcs_candidate]
                lcs_d2 = 0
                if hypernyms_2.has_key(lcs_candidate):
                    lcs_d2 = hypernyms_2[lcs_candidate]
                lcs_dists.append(max([lcs_d1, lcs_d2]))
            h_dist = max(lcs_dists)
        else:
            h_dist = 0
    return ((math.exp(BETA * h_dist) - math.exp(-BETA * h_dist)) / 
        (math.exp(BETA * h_dist) + math.exp(-BETA * h_dist)))
    
def word_similarity(word_1, word_2):
    synset_pair = get_best_synset_pair(word_1, word_2)
    return (length_dist(synset_pair[0], synset_pair[1]) * 
        hierarchy_dist(synset_pair[0], synset_pair[1]))


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

def tokenize(text):
     words = WORD.findall(text)
     return Counter(words)


def textual_similarity(text1,text2):
    vector1 = tokenize(text1.lower())
    vector2 = tokenize(text2.lower())
    cosine = cosine_similarity(vector1, vector2)
    return cosine


def most_similar_word(word, word_set):
    max_sim = -1.0
    sim_word = ""
    for ref_word in word_set:
      sim = word_similarity(word, ref_word)
      if sim > max_sim:
          max_sim = sim
          sim_word = ref_word
    return sim_word, max_sim
    
def info_content(lookup_word):
    
    global N
    if N == 0:
        for sent in brown.sents():
            for word in sent:
                word = word.lower()
                if not brown_freqs.has_key(word):
                    brown_freqs[word] = 0
                brown_freqs[word] = brown_freqs[word] + 1
                N = N + 1
    lookup_word = lookup_word.lower()
    n = 0 if not brown_freqs.has_key(lookup_word) else brown_freqs[lookup_word]
    return 1.0 - (math.log(n + 1) / math.log(N + 1))
    
def semantic_vector(words, joint_words, info_content_norm):
    
    sent_set = set(words)
    semvec = np.zeros(len(joint_words))
    i = 0
    for joint_word in joint_words:
        if joint_word in sent_set:
            semvec[i] = 1.0
            if info_content_norm:
                semvec[i] = semvec[i] * math.pow(info_content(joint_word), 2)
        else:
            sim_word, max_sim = most_similar_word(joint_word, sent_set)
            semvec[i] = PHI if max_sim > PHI else 0.0
            if info_content_norm:
                semvec[i] = semvec[i] * info_content(joint_word) * info_content(sim_word)
        i = i + 1
    return semvec                
            
def semantic_similarity(sentence_1, sentence_2, info_content_norm):
    
    words_1 = nltk.word_tokenize(sentence_1)
    words_2 = nltk.word_tokenize(sentence_2)
    joint_words = set(words_1).union(set(words_2))
    vec_1 = semantic_vector(words_1, joint_words, info_content_norm)
    vec_2 = semantic_vector(words_2, joint_words, info_content_norm)
    return np.dot(vec_1, vec_2.T) / (np.linalg.norm(vec_1) * np.linalg.norm(vec_2))


def word_order_vector(words, joint_words, windex):
    
    wovec = np.zeros(len(joint_words))
    i = 0
    wordset = set(words)
    for joint_word in joint_words:
        if joint_word in wordset:
            wovec[i] = windex[joint_word]
        else:
            sim_word, max_sim = most_similar_word(joint_word, wordset)
            if max_sim > ETA:
                wovec[i] = windex[sim_word]
            else:
                wovec[i] = 0
        i = i + 1
    return wovec

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def word_order_similarity(sentence_1, sentence_2):
    
    words_1 = nltk.word_tokenize(sentence_1)
    words_2 = nltk.word_tokenize(sentence_2)
    joint_words = list(set(words_1).union(set(words_2)))
    windex = {x[1]: x[0] for x in enumerate(joint_words)}
    r1 = word_order_vector(words_1, joint_words, windex)
    r2 = word_order_vector(words_2, joint_words, windex)
    return 1.0 - (np.linalg.norm(r1 - r2) / np.linalg.norm(r1 + r2))


def similarity(sentence_1, sentence_2, info_content_norm):
    
    return DELTA * semantic_similarity(sentence_1, sentence_2, info_content_norm) + \
        (1.0 - DELTA) * word_order_similarity(sentence_1, sentence_2)
        


def find_similar_symptoms(user_symptom):
    similar_list=[]
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
            semantic_val=similarity(symp,symptoms_file[0],True)            
            if isfloat(semantic_val):
                semantic_sim=float(semantic_val)
            else:
                semantic_sim=0.0
            if text_sim>0.75 or semantic_sim>threshold_val:  
                for item in symptoms_file:
                    similar_list.append(item)
                break
    return similar_list


#print find_similar_symptoms(['sleeplessness','nervous'])
