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
# training_set=nltk.classify.apply_features(extract_features,trainer)
# classifier= nltk.NaiveBayesClassifier.train(training_set)
# f=open('my_classifier.pickle','wb')
# pickle.dump(classifier,f)
# f.close()
f = open('my_classifier.pickle','rb')
classifier = pickle.load(f)
f.close()
info=[]
i=0
with open('classifier.csv','wb') as f:
	writer = csv.DictWriter(f, fieldnames = ["ID", "Title", "Condition", "Phase", "Primary_Measure", "Primary_Desc", "Prim_out", "Secondary_Measure", "Secondary_Desc", "Secondary_out", "Intervention_type", "Intervention_name", "Intervention_desc"])
	writer.writeheader()

	with open('classifier_inter.csv','rb') as f:
		reader = csv.reader(f)
		header=reader.next()
		for row in reader:
			desc=row[8]
			if desc==temp:
			#	cnt=cnt+1
			#	print cnt
				writer.writerow({'ID':row[0], 'Title':row[1], 'Condition':row[2], 'Phase':row[3], 'Primary_Measure':row[4], 'Primary_Desc':row[5], 'Prim_out':row[6], 'Secondary_Measure':row[7], 'Secondary_Desc':row[8], 'Secondary_out':outcome_sentiment, 'Intervention_type':row[9], 'Intervention_name':row[10], 'Intervention_desc':row[11]})
				continue
			temp=""
			temp=row[8]	
			is_negated=False
			negation='not'
			is_negated= negation in desc
			level = classifier.classify(extract_features(desc.split()))
			if is_negated==False:
				outcome_sentiment=level
				writer.writerow({'ID':row[0], 'Title':row[1], 'Condition':row[2], 'Phase':row[3], 'Primary_Measure':row[4], 'Primary_Desc':row[5], 'Prim_out':row[6], 'Secondary_Measure':row[7], 'Secondary_Desc':row[8], 'Secondary_out':outcome_sentiment, 'Intervention_type':row[9], 'Intervention_name':row[10], 'Intervention_desc':row[11]})
			else:
				if level=='positive':
					outcome_sentiment="negative"
					writer.writerow({'ID':row[0], 'Title':row[1], 'Condition':row[2], 'Phase':row[3], 'Primary_Measure':row[4], 'Primary_Desc':row[5], 'Prim_out':row[6], 'Secondary_Measure':row[7], 'Secondary_Desc':row[8],'Secondary_out':outcome_sentiment, 'Intervention_type':row[9], 'Intervention_name':row[10], 'Intervention_desc':row[11]})
				else:
					outcome_sentiment="positive"
					writer.writerow({'ID':row[0], 'Title':row[1], 'Condition':row[2], 'Phase':row[3], 'Primary_Measure':row[4], 'Primary_Desc':row[5], 'Prim_out':row[6], 'Secondary_Measure':row[7], 'Secondary_Desc':row[8], 'Secondary_out':outcome_sentiment, 'Intervention_type':row[9], 'Intervention_name':row[10], 'Intervention_desc':row[11]})

