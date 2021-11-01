#!/usr/bin/env python
# coding: utf-8

# In[24]:

import time
import os
import re
import urllib.request
from openpyxl import Workbook
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# In[14]:


options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument('start-maximized')


driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(10)

# In[3]:


ID = '#'
PASS = '#'


# In[25]:


def Login(ID, PASS):
    driver.get("https://mbasic.facebook.com")
    driver.find_element(By.CSS_SELECTOR, '#m_login_email').send_keys(ID)
    driver.find_element(By.NAME, 'pass').send_keys(PASS), time.sleep(1)
    driver.find_element(By.NAME, "pass").send_keys(Keys.ENTER), time.sleep(5)
    driver.get("https://m.facebook.com")


# In[26]:

# remove hash to scrape all listings for a seller. keep hash to scrape 20 listings

def Marketplace_listings():
#For All Product list Activate this code

    # while True:
    #     value = SeeMore()
    #     if value==False:
    #         break
#End All Product List control
#For specific range of product list activate this code
    Number_of_product = 22
    count = 0
    while True:
        value = SeeMore()
        if count == 0: 
            listingelems = driver.find_elements_by_xpath('//*[@aria-label="Commerce Profile"]//a[contains(@href,"/marketplace")]')
            for elem in listingelems:
                count+=1
        else:
            count+=8 #because every time when we click 8 product will be show
        if(count>=Number_of_product or value== False):
            break
# End specific range of product list

    listingelems = driver.find_elements_by_xpath('//*[@aria-label="Commerce Profile"]//a[contains(@href,"/marketplace")]')
    return [elem.get_attribute('href') for elem in listingelems]


# In[27]:


def Seemore():
    try:
        driver.find_element_by_xpath('//span[@dir="auto"]//span[contains(text(),"See more")]').click()
    except NoSuchElementException:
        return False
    from random import randint
    from time import sleep
    sleep(randint(10, 100))
    return True
# In[28]:


def SeeMore():
    try:
        driver.find_element_by_xpath('//span[@dir="auto"]//span[text()="See more"]').click()
    except NoSuchElementException:
        return False
    from random import randint
    from time import sleep

    sleep(randint(10, 100))
    return True

# In[29]:


def Tagsfind():
    try:
        driver.find_element_by_xpath('//*[text()="Show more"]').click()
    except:
        pass
    tagselem = driver.find_elements_by_xpath('//*[@class="fnu23jab a9txdygg"]//span[@dir="auto"]/span')
    return [tagtext.text for tagtext in tagselem]


# In[30]:


def Gallery_download(profile_name, title):
    title = re.sub(r'[^a-zA-Z0-9 \n\.]', '', title)
    path = f'{os.getcwd()}/{profile_name}/{title}'
    if not os.path.exists(path):
        os.mkdir(f'{os.getcwd()}/{profile_name}/{title}')
    thumbnails = driver.find_elements_by_xpath('//div[contains(@style,"transform:translate")]//img')
    for index, picelem in enumerate(thumbnails):
        src = picelem.get_attribute('src')
        try:
            urllib.request.urlretrieve(src, f'{path}/image{index}.png')
        except:
            pass



# In[31]:


def scraper(listingitems, df):
    count = 1
    for url in listingitems:
        driver.get(url)
        title = driver.find_element_by_css_selector('div.hv4rvrfc>div>span.hnhda86s').text
        price = driver.find_element_by_css_selector('div.hv4rvrfc>div.aov4n071>div>span').text
        description = driver.find_element_by_xpath('(//*[@data-pagelet="MainFeed"]//div[@class="aahdfvyu"])[1]').text
        try:
            driver.find_element_by_xpath('//span[text()="Condition"]')
            condition = driver.find_element_by_xpath('(//*[@data-pagelet="MainFeed"]//div[@class="aahdfvyu"]//span[@dir="auto"])[2]/span').text
        except:
            condition = 'Nill'
        Gallery_download(profile_name, title)
        try:
            driver.find_element_by_xpath('//span[text()="Tags"]')
            Tags = Tagsfind()
        except:
            Tags = "Nill"

        data = {'Title': title, 'Price': price, 'Condition': condition, 'Description': description, 'Tags': Tags}
        print(data, file=df)
        print("List done...!---> %d"%count)
        count+=1


# In[32]:


def spreadsheet(profile_name):
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    ws.title = profile_name
    with open(f'{os.getcwd()}/{profile_name}/data.txt', mode='r', encoding="utf8") as rdf:
        for line in rdf:
            dictt = eval(line.strip())
            data = []
            for k, v in dictt.items():
                if isinstance(v, list):
                    v = '|'.join(v)
                data.append(v)
            ws.append(data)
    wb.save(f'{os.getcwd()}/{profile_name}/{profile_name}.xlsx')


# In[15]:


Login(ID, PASS)

# In[33]:


with open('./sellers.txt', mode='r') as f:
    for line in f:
        Seller_url = line.strip()
        driver.get(Seller_url)
        profile_name = driver.find_element_by_xpath('(//div[@aria-label="Commerce Profile"]//span[@dir="auto"])[2]').text
        print(profile_name)
        if not os.path.exists(f'{os.getcwd()}/{profile_name}'):
            os.mkdir(f'{os.getcwd()}/{profile_name}')
        with open(f'{os.getcwd()}/{profile_name}/data.txt', mode='w', encoding="utf-8") as wdf:
            listingitems = Marketplace_listings()
            scraper(listingitems, wdf)
        spreadsheet(profile_name)

# In[17]:


os.getcwd()

# In[ ]:


