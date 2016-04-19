import nltk
from nltk.tokenize import word_tokenize
from nltk import bigrams
from nltk.probability import ELEProbDist, FreqDist
from nltk import NaiveBayesClassifier
from collections import defaultdict
import pickle
import csv
#nltk.usage(nltk.classify.ClassifierI)
trainer = []
neg=[]
a=open('/home/soorya/Treatment-Recommender/Classification/negative-words.txt','r')
b=""
neg1=[]
outcome_sentiment=""
temp=""
count=0
cnt=0
pos=[]
happy=[]
for i in a.read():
	if i not in '\n':
		b+=i
	else:	
		neg1.append(b)
		neg.append((neg1,"negative"))
		b=""
		neg1=[]
a=open('/home/soorya/Treatment-Recommender/Classification/positive-words.txt','r')
for i in a.read():
        if i not in '\n':
                b+=i
        else:	
		neg1.append(b)
                pos.append((neg1,"positive"))
                b=""
		neg1=[]
for (words, sentiment) in pos+neg:
    trainer.append((words, sentiment))

def read_file(fname, t_type):
    sent = []
    f = open(fname, 'r')
    line = f.readline()
    while line != '':
        sent.append([line, t_type])
        line = f.readline()
    f.close()
    return sent

def get_words_in_trainer(trainer):
    all_words = []
    for (words, sentiment) in trainer:
	all_words.extend(words)
    return all_words
    
def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    fdist =nltk.FreqDist(wordlist)
    return word_features

word_features = get_word_features(get_words_in_trainer(trainer))
def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
    	features[word] = (word in document_words)
    return features

#training_set=nltk.classify.apply_features(extract_features,trainer)
#classifier= nltk.NaiveBayesClassifier.train(training_set)
# f=open('my_classifier.pickle','wb')
# pickle.dump(classifier,f)
# f.close()
f = open('my_classifier.pickle','rb')
classifier = pickle.load(f)
f.close()
info=[]
i=0
outcome_sentiment=""
test_file = read_file('test-positive.txt','positive')
#test_file.extend(read_file('test-negative.txt','negative'))
total=accuracy=float(len(test_file))

for line in test_file:
	is_negated=False
	negation='not'
	is_negated=negation in line[0]
	level=classifier.classify(extract_features(line[0].split()))
	if is_negated==False:
		outcome_sentiment=level
	else:
		if level=='positive':
			outcome_sentiment="negative"
		else:
			outcome_sentiment="positive"
	if outcome_sentiment!=line[1]:
		accuracy-=1
	#print line[0]+" Predicted:"+outcome_sentiment+" Original:"+line[1]

print('Total accuracy: %f%% (%d/%d).' % (accuracy / total * 100, accuracy,total))