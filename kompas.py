from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd 
import requests
# scrap satu artikel
keywords="sampah and yogyakarta"

keywords= "+".join(keywords.split())

url = "https://search.kompas.com/search/?q={}&submit=Submit+Query".format(keywords)

def selenium_content(url):
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content)

    return soup

def text_kompas(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "lxml")
    judul = soup.find('h1', attrs={"class": "read__title"}).text
    time = soup.find("div", attrs={"class": "read__time"}).text.split()[2:]
    tanggal = time[0]
    jam = ' '.join(time[1:])
    # editor = soup.find("div", attrs={"id": "editor"}).find("a").text
    text = soup.find("div", attrs={"class": "read__content"}).text

    return {
        "judul":judul,
        "tanggal":tanggal,
        "jam": jam,
        # "editor":editor,
        "text":text,
        "post_url": url
    }

soup = selenium_content(url)
index = soup.find_all('div', attrs={"class":"gsc-webResult gsc-result"})

link_url = list()
judul = list()
text = list()
editor = list()
tanggal = list()

for data in index:
    get_code = data.find('div', attrs={"class": "gs-title"})
    if get_code:
        url = get_code.find('a')['href']
        link_url.append(url)
        dct = text_kompas(url)
        judul.append(dct["judul"])
        text.append(dct["text"])
        # editor.append(dct["editor"])
        tanggal.append(dct["tanggal"])

data = pd.DataFrame({
    "judul":judul,
    "post_url": link_url,
    # "editor": editor,
    "text": text,
    "tanggal": tanggal
})
print(data)