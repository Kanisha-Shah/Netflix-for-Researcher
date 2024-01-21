import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import re
import string

html_text = requests.get("https://arxiv.org/list/cs.AI/recent",headers={'User-Agent':'Mozilla/5.0'})
soup = bs(html_text.text,'lxml')

article = soup.find("dl")
dds = article.find_all("dd")
dts = article.find_all("dt")


title =[]
authors = []
keyword = []
abstract = []
date = []


for dt in dts:
  link = dt.find("span",class_="list-identifier").a['href']
  link = "https://arxiv.org/" + link

  html_text1 = requests.get(link,headers={'User-Agent':'Mozilla/5.0'})
  soup1 = bs(html_text1.text,'lxml')

  abstract.append(soup1.find("blockquote",class_= "abstract mathjax").text.replace("Abstract:","").replace("\n",""))
  dt = (soup1.find('div',class_="dateline").text.replace("[Submitted on ","").replace("]","").replace("\n",""))
  dt = re.sub(' +', ' ', dt).strip()

  dict1 = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Sep":"08","Aug":"09","Oct":"10","Nov":"11","Dec":"12"}
  day = dt[0]
  month = dt[2:5]
  year =dt[6:len(dt)]
  
  dt_form = year+"/"+dict1[month]+"/"+day
  date.append(dt_form)

for dd in dds:
  ti = (dd.find("div",class_="list-title mathjax").text.replace("Title:","").replace("\n",""))
  ti = ti.translate(str.maketrans('','',string.punctuation))
  ti = re.sub(' +', ' ', ti)
  title.append(ti)

  at = (dd.find("div",class_="list-authors").text.replace("Authors:","").replace("\n",""))
  at = at.translate(str.maketrans('','',string.punctuation))
  at = re.sub(' +', ' ', at)
  authors.append(at)

  keyword.append(dd.find("div",class_="list-subjects").text.replace("Subjects:","").replace("\n",""))

dataf = pd.DataFrame({"Title":title,
              "Authors":authors,
              "Keyword":keyword,
              "Abstract":abstract,
              "Date":date})


dataf.to_csv('rp.csv',index=True)

