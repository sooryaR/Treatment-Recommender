import csv

path="/home/soorya/Treatment-Recommender/Classification/classifier.csv"
disease_files={}
check={}
with open(path,'rb') as f:
	reader=csv.reader(f)
	header=reader.next()
	for row in reader:
		name=" ".join(row[2].split("-"))
		key_to_check=row[2]+" "+row[0]
		if check.has_key(key_to_check):
			continue
		else:
			check[key_to_check]=1
			temp=disease_files.get(name,"")
			if temp=="" :
				disease_files[name]=row[0]
			else:
				disease_files[name]=disease_files[name]+","+row[0]

file=open('Disease_Index.csv','wb')
writer=csv.writer(file)
for item in disease_files:
	row=[]
	row.append(item)
	row.append(disease_files[item])
	writer.writerow(row)