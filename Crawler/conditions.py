import urllib2
import csv
from bs4 import BeautifulSoup
import html5lib
from bs4 import NavigableString

link_list=[]

def find_links(link):
	url_link="https://www.patientslikeme.com/"+link
	url1=urllib2.urlopen(url_link)
	content=url1.read()
	soup=BeautifulSoup(content,"html5lib")
	a_tags=soup.find_all('a')
	for tag in a_tags:
		if tag.has_attr('href') and "/conditions" in tag['href'] and tag['href'] in link_list:
			break
		if tag.has_attr('href') and "/conditions/" in tag['href']:
			link_list.append(tag['href'])
			break


def links_to_crawl():
	f=open('conditions_link.txt','a')
	for line in link_list:
		f.write(line)
		f.write("\n")
	f.close()
	temp="https://www.patientslikeme.com"
	for val in link_list:
		link=temp+val
		url=urllib2.urlopen(link)
		content=url.read()
		soup=BeautifulSoup(content,"html5lib")
		print link
		disease_name=soup.find('span',itemprop='name').string
		div_all=soup.div
		#print div_all
		links= div_all.find_all('a',itemprop='url')
		symptoms=[]
		treatments=[]
		for link in links:
			if link.span.string in treatments or link.span.string in symptoms:
				continue
			if "/treatments" in link['href']:
				treatments.append(link.span.string)
			elif "/symptoms" in link['href']:
				symptoms.append(link.span.string)

		if len(treatments)==0:
			treatments.append('No Treatment specified')
		if len(symptoms)==0:
			symptoms.append('No Symptom specified')
			
		symp="|".join(symptoms)
		tmts="|".join(treatments)
		#print tmts
		row=[]
		row.append(disease_name)
		row.append(symp)
		row.append(tmts)

		writer.writerow(row)


#header=['Disease_name','Symptoms','Treatments']
file=open('new_diseases_crawled.csv','ab') 
writer=csv.writer(file)
#writer.writerow(header)
page_num=150
while page_num<200:
	page_num+=1
	link="https://www.patientslikeme.com/patients?patient_page="+str(page_num)+"&utm_campaign=day_04_ms&utm_medium=email&utm_source=welcome"
	url=urllib2.urlopen(link)
	content=url.read()
	soup=BeautifulSoup(content,"html5lib")
	print "reading page"+str(page_num)
	a_tags=soup.find_all('a')
	for tag in a_tags:
		if tag.has_attr('href') and "/patients/view" in tag['href']:
			#print tag['href']
			find_links(tag['href'])
links_to_crawl()