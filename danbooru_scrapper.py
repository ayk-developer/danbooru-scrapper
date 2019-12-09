from bs4 import BeautifulSoup as soup
import requests
import sys, os, requests, shutil


print("\nDanbooru Scrapper \n")
tag = input("Type in the tag to scrap :")
page_no = int(input("Type in the amount of pages to scrap :"))


for j in range(1,page_no):
	print("Scraping Page Number "+str(j))
	page = requests.get("https://danbooru.donmai.us/posts?page="+str(j)+"&tags="+tag)
	c = page.content
	s= soup(c,'html.parser')
	all=s.find_all("article")
	for i in range(len(all)):
		try:
		    name=all[i].find("img",{"class":"has-cropped-false"})["src"]
		    r=requests.get(name,stream=True)
		    r.raw.decode_content = True
		    f = open(name.split("/")[-1], "wb" )
		    shutil.copyfileobj(r.raw, f)
		    f.close()
		except TypeError:
			print("crop true at picture number" + str(i))
			name=all[i].find("img",{"class":"has-cropped-true"})["src"]
			r=requests.get(name,stream=True)
			r.raw.decode_content = True
			f = open(name.split("/")[-1], "wb" )
			shutil.copyfileobj(r.raw, f)
			f.close()
