import csv
from Collaborative import collaborative_filter
import os.path
import re
import sys

user_disease=sys.argv[1]
user_symptom=sys.argv[2]
user_age=sys.argv[3]
user_gender=sys.argv[4]


def find_treatments(file_list,user_disease):
	trial_files="/home/soorya/Treatment-Recommender/Code/Files/TrialFiles"
	treatments=[]
	for file in file_list:
		temp=[]
		sec_measure=[]
		pos=0
		fname=trial_files+"/"+file+".csv"
		handle=open(fname,'rb')
		reader=csv.reader(handle)
		for row in reader:
			dname=" ".join(row[2].split("-"))
			if user_disease.lower()!=dname.lower():
				continue
			if row[7] in sec_measure:
				continue
			sec_measure.append(row[7])
			if row[9]=="positive" :
				pos+=1
				if row[1] not in temp:
					temp.append(row[1])
		if len(sec_measure)>0:
			prob=float(pos)/len(sec_measure)
		else:
			prob=0.0
		if prob>=0.5:
			for item in temp:
				treatments.append(item)
	return treatments


def content_based_filtering(user_disease):
	file_name="/home/soorya/Treatment-Recommender/Code/Disease_Index.csv"
	with open(file_name,'rb') as f:
		reader=csv.reader(f)
		file_list=""
		for row in reader:
			if user_disease.lower() in row[0].lower():
				if file_list!="" :
					file_list+=","
				file_list+=row[1]
		return find_treatments(file_list.split(","),user_disease)


content_treatments=[]
collaborative_treatments=[]
ranking_score={}
treatment_file="/home/soorya/Treatment-Recommender/Code/Treatments"
major_eff=[]
moderate_eff=[]
slight_eff=[]
no_eff=[]
pos_score={}
neg_score={}
recommend_treatments=[]
top_treatments=3
top_content_treatments=1
content_treatments = content_based_filtering(user_disease)
collaborative_treatments = collaborative_filter(user_symptom,user_disease,user_age,user_gender)
#print collaborative_treatments
for name in collaborative_treatments:
	fpath=treatment_file+"/"+name+".txt"
	if not os.path.isfile(fpath):
		continue
	file=open(fpath,'r')
	cnt=0
	for line in file:
		if not line.strip():
			continue
		row=line.split(',')
		if len(row)==1 and str(row[0]).isdigit():
			if cnt==0 or cnt==1:
				neg_score[name]=neg_score.get(name,0)+int(row[0])
				cnt+=1
			else:
				pos_score[name]=pos_score.get(name,0)+int(row[0])
				cnt+=1
		if user_disease.lower() not in row[0].lower():
			continue
		for index,item in enumerate(row):
			if len(row)<3:
				break
			if index==2:
				total_eval=int(item)
			elif "major" in item:
				arr=re.findall('[0-9]+',item)
				val=float(arr[0])
				major_eff.append((val/total_eval,name))
			elif "moderate" in item:
				arr=re.findall('[0-9]+',item)
				val=float(arr[0])
				moderate_eff.append((val/total_eval,name))
			elif "slight" in item:
				arr=re.findall('[0-9]+',item)
				val=float(arr[0])
				slight_eff.append((val/total_eval,name))
			elif "no perceived" in item:
				arr=re.findall('[0-9]+',item)
				val=float(arr[0])
				no_eff.append((val/total_eval,name))

major_eff.sort(reverse=True)
moderate_eff.sort(reverse=True)
slight_eff.sort(reverse=True)
no_eff.sort(reverse=True)
pos_score=sorted(pos_score,key=pos_score.get,reverse=True)
neg_score=sorted(neg_score,key=neg_score.get,reverse=True)

score=len(major_eff)
for val,name in major_eff:
	ranking_score[name]=ranking_score.get(name,0)+score
	score-=1
score=len(moderate_eff)
for val,name in moderate_eff:
	ranking_score[name]=ranking_score.get(name,0)+score
	score-=1
score=1
for val,name in slight_eff:
	ranking_score[name]=ranking_score.get(name,0)+score
	score+=1
score=1
for val,name in no_eff:
	ranking_score[name]=ranking_score.get(name,0)+score
	score+=1
score=len(pos_score)
for name in pos_score:
	ranking_score[name]=ranking_score.get(name,0)+score
	score-=1
score=1
for name in neg_score:
	ranking_score[name]=ranking_score.get(name,0)+score
	score+=1

for treatment in sorted(ranking_score,key=ranking_score.get,reverse=True):
	#print treatment
	if top_treatments==0:
		break
	recommend_treatments.append(treatment)
	top_treatments-=1
	#print treatment


for treatment in content_treatments:
	if top_content_treatments==0:
		break
	recommend_treatments.append(treatment)
	top_content_treatments-=1
	#print treatment


for treatment in recommend_treatments:
	print treatment
