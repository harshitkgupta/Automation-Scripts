import requests
import pdfcrowd
import urllib2
from bs4 import BeautifulSoup, SoupStrainer

url= 'http://tutorials.jenkov.com/java-concurrency/index.html'
url_prefix = 'http://tutorials.jenkov.com/'
def save_as_pdf(link):
    try:
        client = pdfcrowd.Client("harshitgupta", "ad4ffd8759bda68041bb311278f627a2")
        
        page = requests.get(link)
        soup= BeautifulSoup(page.text)
        html = soup.find_all('div', {'class': 'card'})
        fileName = link.split(r'/')[-1].split('.')[0]+'.pdf'  
        output_file = open(fileName, 'wb')
        client.convertHtml(''.join(map(str, html)), output_file)
        output_file.close()
        print fileName," saved"
    except pdfcrowd.Error,why:
        print 'Failed:', why

page = requests.get(url)
page_bs = BeautifulSoup(page.text) 
tut_links = []
for link_detail in page_bs.select('#trailToc > ol > li > a'):
    link = link_detail.get('href').split(r'/')[-1];
    tut_links.append(url_prefix+link)
    
print tut_links
for link in tut_links:    
   save_as_pdf(link)


    #trailToc>ol>li>a



                

