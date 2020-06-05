from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd 

# scrap satu artikel

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
driver.get("https://basabasi.co/perjalanan-kenangan-dan-tugas-seorang-seniman/")

content = driver.page_source
soup = BeautifulSoup(content)

header = soup.find('div', attrs={'class': 'blog-header-content'})
body = soup.find('div', attrs={'class': 'blog-content'})


judul = header.find('time', attrs={'class':'entry-date'}).text
date = header.find('h1').text
penulis = header.find('span',attrs={'class':'blog-post-author'}).text
artikel = '\n '.join([i.text for i in body.findAll('p', attrs={'style':"text-align: justify;"})])

print(judul, date, penulis, artikel)
