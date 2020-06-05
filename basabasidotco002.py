from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd 

# home basabasi

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

judul = list()
tanggal = list()
penulis = list()
url = list()
category = list()
artikel =  list()

driver.get("https://basabasi.co/")

content = driver.page_source
soupHome = BeautifulSoup(content)


for div in soupHome.findAll('div', attrs={'class':"blog-grid-content"}):
    cat = div.find('a', href=True, attrs={'rel': 'category tag'}).text
    category.append(cat)
    uri = div.find('h3').find('a')['href']
    url.append(uri)

    driver.get(uri)
    content = driver.page_source
    soup = BeautifulSoup(content)

    header = soup.find('div', attrs={'class': 'blog-header-content'})
    body = soup.find('div', attrs={'class': 'blog-content'})
    tanggal.append(header.find('time', attrs={'class':'entry-date'}).text)
    judul.append(header.find('h1').text)
    penulis.append(header.find('span',attrs={'class':'blog-post-author'}).text)
    artikel.append('\n '.join([i.text for i in body.findAll('p', attrs={'style':"text-align: justify;"})]))


data = pd.DataFrame({'judul':judul, 'tanggal_terbit':tanggal, 'kategori':category, 'url':url, 'text':artikel})

data.to_csv('basabasihome.csv')