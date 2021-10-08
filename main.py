from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from time import sleep

chromedriver_path= r"C:\Users\Admin\OneDrive\Desktop\Angela\chromedriver.exe"

googleform="https://forms.gle/ib6CHnyKSCLFyaSR9"
gformresponses="https://docs.google.com/forms/d/1SWpu99T3yjXTFChGbYb1Zwq2m7mj2bXEr5d1WDS0iZ4/edit#responses"

#BeautifulSoup Part

# 🌟 IMP
headerss={"Accept-Language":"en-US,en;q=0.9",
          "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
          }
zillowlink="https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

# 🌟 IMP to use url= and hearders=
response=requests.get(url=zillowlink,headers=headerss)
scrapweb=response.text

soup=BeautifulSoup(scrapweb,"html.parser")
# print(soup.prettify())

# links = soup.find_all(name="a", class_="list-card-link list-card-link-top-margin list-card-img")#7
# alinks=soup.select(".list-card-top a")9
# prices=soup.select(".list-card-info .list-card-price")
# links=soup.select("ul li article a")#18
# linkl=[]
# for l in links:
#     if "http" not in l.get("href"):
#         linkl.append(f'https://www.zillow.com{l.get("href")}')
#     else:
#         linkl.append(l.get("href"))

links=soup.select(".list-card-top a")
prices = soup.find_all(name="div", class_="list-card-price")
adres = soup.find_all(name="address", class_="list-card-addr")

houselist= []
for l in links:
    href=l.get("href")
    if "http" not in href:
        houselist.append(f'https://www.zillow.com{href}')
    else:
        houselist.append(href)
priclist= [p.text.split("+")[0] for p in prices if "$" in p.text] #$2,350/mo
pricelist=[p.split("/")[0] for p in priclist]
adreslist = [ad.text for ad in adres]                               # ['$1,200/mo', '$2,795', '$2,195', '$2,350/mo', '$2,395/mo', '$2,595/mo', '$2,900/mo', '$2,700/mo', '$2,600/mo']
print(houselist,"\n",pricelist,"\n",adreslist)                      # ['$1,200', '$2,795', '$2,195', '$2,350', '$2,395', '$2,595', '$2,900', '$2,700', '$2,600']

#selenium Part

drive=webdriver.Chrome(chromedriver_path)
drive.get(googleform)
gmail="pk1649@srmist.edu.in"
gpass="Gajini@1649"
mail=drive.find_element_by_xpath('//*[@id="identifierId"]')
mail.click()
mail.send_keys(gmail,Keys.ENTER)
sleep(2)
passw=drive.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
passw.click()
passw.send_keys(gpass,Keys.ENTER)

for href in range(len(links)):

    sleep(4)
    addres =drive.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    cost = drive.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    lnkofp =drive.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit=drive.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    sleep(3)
    addres.send_keys(adreslist[href])
    cost.send_keys(pricelist[href])
    lnkofp.send_keys(houselist[href])
    submit.click()
    drive.get(googleform)
# drive.quit()
drive.get(gformresponses)
spredsheet=drive.find_element_by_xpath('//*[@id="ResponsesView"]/div/div[1]/div[1]/div[2]/div[1]/div/div/span/span/div/div[1]')
spredsheet.click()
sleep(1)
create=drive.find_element_by_xpath('//*[@id="wizViewportRootId"]/div[9]/div/div[2]/div[2]/div[3]/div[1]/div[2]')
create.click()
drive.quit()