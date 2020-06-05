from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd 
from collections import defaultdict

# semua page di basabasi.co
# get all articles in an page
def find_archive(soupHome):
    """
    soupHome:  BeautifulSoup load page
    """

    judul = list()
    tanggal = list()
    penulis = list()
    url = list()
    category = list()
    artikel =  list()

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
        artikel.append('\n '.join([i.text for i in body.findAll('p')]))

    return {
        "judul":judul, 
        "tanggal_terbit":tanggal, 
        "kategori": category,
        "penulis": penulis, 
        "text": artikel, 
        "url": url
    }

# merge dict
def merge_two_dict(d1, d2):
    dfinal = defaultdict(list)
    for i in (d1, d2):
        for key, value in i.items():
            dfinal[key] += value
    return dfinal

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
data = dict()
driver.get("https://basabasi.co/page/178/") # replace this link to https://basabasi.co

content = driver.page_source
soupHome = BeautifulSoup(content)
data = find_archive(soupHome)

# other page
page = soupHome.find('ul', attrs={'class': 'page-numbers'}).find('a',attrs={'class':"next page-numbers"})['href']
NoneType = type(None)
while page != None:
    driver.get(page)
    content = driver.page_source
    soupHome = BeautifulSoup(content)    
    data = merge_two_dict(data, find_archive(soupHome))
    cek = soupHome.find('ul', attrs={'class': 'page-numbers'}).find('a',attrs={'class':"next page-numbers"})
    page = None if isinstance(cek, NoneType) else cek['href']

data = pd.DataFrame(data)
data.to_csv('basabasidotcoallpage.csv')