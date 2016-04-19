#from Collaborative_er import find_similar_symptoms
from collaborative_er_sem import find_similar_symptoms
import csv
import re

# user_symptom=raw_input().split(',')
# user_disease=raw_input()
# user_age=raw_input()
# user_gender=raw_input()

def find_similar_users(user_symptom,user_disease,age,gender):

	similar_symptom = find_similar_symptoms(user_symptom)
	for i,item in enumerate(similar_symptom):
		similar_symptom[i]=item.lower()
	user_symp_len=len(user_symptom)
	user_symptom=user_symptom+similar_symptom
	symptom_list=list(set(user_symptom))
	for i,item in enumerate(symptom_list):
		symptom_list[i]=item.strip('\r')
	#print symptom_list
	similarity=[]
	top_k_users=3
	top_treatments=[]
	with open('/home/soorya/Treatment-Recommender/Code/patients_data.csv','rb') as file:
		reader=csv.reader(file)
		header=reader.next()
		for row in reader:
			if user_disease.lower() not in row[3].lower():
				continue

			to_check=row[4].split(',')	
			patient_gender,age_line=row[1].split(',')
			lst=re.findall('[0-9]+',age_line)
			patient_age=int(lst[0])
			for i,item in enumerate(to_check):
				to_check[i]=item.lower()
			common_symptom=[item for item in symptom_list if item.lower() in to_check]
			similarity_val=float(len(common_symptom))/(len(to_check)+user_symp_len)
			similarity.append((similarity_val,row[0],patient_gender,patient_age,row[5]))

		similarity.sort(reverse=True)
		users_matched=0
		for value,user,p_gender,p_age,p_treatments in similarity:
			if users_matched==top_k_users:
				break
			if p_gender.lower()!=gender.lower() or abs(int(p_age)-int(age))>5 or value==0.0:
				continue
			tms=p_treatments.split(',')
			#print user,value
			for item in tms:
				top_treatments.append(item)
			users_matched+=1
		treatments=list(set(top_treatments))
		return treatments


def collaborative_filter(symptom,disease,age,gender):
	user_symptom=symptom.split(',')
	for i,item in enumerate(user_symptom):
		user_symptom[i]=item.lower()
	return find_similar_users(user_symptom,disease,age,gender)


#collaborative_filter('Sexual dysfunction,Mood swings','Multiple Sclerosis',50,'Male')
