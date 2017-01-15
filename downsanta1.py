#http://media1.santabanta.com/full6/Global%20Celebrities(F)/Leila%20Thomas/leila-thomas-0a.jpg

import requests
import os
import logging
import threading
import bs4
import requests
import pprint




def download_img(baseurl):
	folder=baseurl.split(r'/')[-1]
	complete_path= os.path.join("santabanta",folder)
	if(not os.path.exists(complete_path)):
		os.makedirs(complete_path)
	failedTimes=0	
	for i in range(0,500):
		if(failedTimes >=5):
			break;
		url=baseurl+"-"+str(i)+"a.jpg"
		fileName=url.split(r'/')[-1]
		complete_fileName= os.path.join("santabanta",folder,fileName)
		failed=0
		if(os.path.isfile(complete_fileName)): 
			logging.debug("%s exists already"%(fileName))
		else:	
			res = requests.get(url)
			try:
				res.raise_for_status()
				logging.debug("%s downloaded"%(fileName))		
			except Exception as exc:
				logging.error("%s for %s"%(exc,fileName))
				failedTimes+=1;
				continue	
			imgFile = open(complete_fileName, 'wb')  
			for chunk in res.iter_content(100000):
					imgFile.write(chunk)
			imgFile.close();
			
	

requests_log = logging.getLogger("requests")
requests_log.addHandler(logging.NullHandler())
requests_log.propagate = False
logging.basicConfig(filename=r'report.log',level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

_url="http://www.santabanta.com/wallpapers/indian-celebrities(f)/2/?page="
for page in range(1,2):
	page_url = _url+str(page)
	page = requests.get(page_url)
	page_bs = bs4.BeautifulSoup(page.text)
	actress_list=[]
	for link in page_bs.select('a[href]'):
		href = link.get('href')
		if link.get('href').startswith(r'/wallpapers/') and link.get('title') is not None:
			actress_list.append(link.getText())
	
	for actress in actress_list:
		first=actress.title().replace(' ','%20')	
		second=actress.replace(' ','-')	 
		baseurl="http://media1.santabanta.com/full6/Indian%20%20Celebrities(F)/"+first+"/"+second
		logging.info("fetching %s" %(baseurl))
		download_img(baseurl)
