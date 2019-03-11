from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import json
import csv
headers = {'User-Agent':
       'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = "https://www.indeed.co.in/jobs?q=software+developer&l=Bengaluru%2C+Karnataka"
company_name = []
job_title = []
page_num = 10
session = requests.Session()
while True:
    pageTree = session.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    jobs= pageSoup.find_all("a", {"data-tn-element": "jobTitle"})
    Companys = pageSoup.find_all("span", {"class": "company"})
    for Company, job in zip(Companys, jobs):
        companyname=Company.text
        company_name.append(companyname.replace("\n",""))
        job_title.append(job.text)
    if pageSoup.find("span", text=re.compile("Next")):
        page = "https://www.indeed.co.in/jobs?q=software+developer&l=Bengaluru%2C+Karnataka&start={}".format(page_num)
        page_num +=10
    else:
        break
print("company: ",company_name)

print("____________")

print("job:",job_title)
df = pd.DataFrame({"company_name":company_name,"job_title":job_title})
print(df.head(1000))
for urls in page:
	json_file = open('output.json','w')
	json.dump(df,json_file)
	json_file.close()
