from asyncio.windows_events import NULL
from requests import Session
from bs4 import BeautifulSoup
from random import uniform
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from subprocess import Popen
from re import search
import csv
from os import _exit

def Get_name_list_and_Write_to_Excel(id, last_name, sess, start_at = False, start_url = False) :

    if start_url != False :
        url = start_url
    else :
        url = 'https://www.ancestry.com/search/collections/7488/?name=_' + last_name + '&name_x=_1&count=50'
    
    if start_at != False :
        i = start_at
    else :
        i = 1
        
    while True:
        res = sess.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        if i == 1 :
            try :
                total = search( 'of\s+(.+)', soup.select('h3.w50')[0].text.strip()).group(1).replace(',', '')
            except :
                total = '0'
            with open ('Amount Check.txt', 'a+', encoding='ISO-8859-1') as f:
                f.write('Last name "' + last_name + '" total : ' + total + '\n')
            with open ('Amount Check with page.txt', 'a+', encoding='ISO-8859-1') as f:
                f.write('Last name "' + last_name + '" total : ' + total + '\n')
            print('Last name "' + last_name + '" total : ' + total)

        items = soup.select('tr[id*="sRes"]')
        for item in items:
            Name = item.select('span.srchHit')[0].text.replace('’', "'")
            Birth_Year = item.select('td[valign="top"]')[2].text.replace('’', "'")
            Arrival_Date = item.select('td[valign="top"]')[3].text.replace('’', "'")
            Departure_Port = item.select('td[valign="top"]')[4].text.replace('’', "'")
            Ethnicity_and_Nationality = item.select('td[valign="top"]')[5].text.replace('’', "'")
            Ship_Name = item.select('td[valign="top"]')[6].text.replace('’', "'")

            #print(Name) 
            #print(Birth_Year)
            #print(Arrival_Date)
            #print(Departure_Port)
            #print(Ethnicity_and_Nationality)
            #print(Ship_Name)

            with open ('Name list.csv', 'a+', encoding='utf-8', newline='') as csvfile :
                writer = csv.writer(csvfile)
                writer.writerow([id, Name, Birth_Year, Arrival_Date, Departure_Port, Ethnicity_and_Nationality, Ship_Name])

        print('Page ' + str(i) + ' ----------------------------------- Done')
        with open ('Amount Check with page.txt', 'a+', encoding='ISO-8859-1') as f:
            f.write('Page ' + str(i) + ' ----------------------------------- Done\n')

        try:
            next_link = soup.select('li.next a')[0]['href']
            url = 'https://www.ancestry.com/search/collections/7488/' + next_link
            with open ('Amount Check with page.txt', 'a+', encoding='ISO-8859-1') as f:
                f.write(url + '\n')
            i = i + 1
            #sleep(uniform(0.1 , 3)) # 隨機等待時間
        except :
            break


cmd = r'"C:\Program Files\Google\Chrome\Application\chrome.exe" https://www.ancestry.com/account/signin --remote-debugging-port=9222 --user-data-dir="C:\Users\Shihau\Documents\Selenium\ChromeProfile" --incognito'
Popen(cmd, shell=True)
sleep(6) # 需讓網頁等待一點時間，否則會被判定為機器人

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome = webdriver.Chrome(options=chrome_options)

chrome.implicitly_wait(30)
user_acct = chrome.find_element(by=By.XPATH, value='//input[@id="username"]')
user_acct.clear()
chrome.implicitly_wait(30)
user_acct.send_keys('jerry.lin@monash.edu')
user_pwd = chrome.find_element(by=By.XPATH, value='//input[@name="password"]')
user_pwd.clear()
user_pwd.send_keys('aa001yhjerrylin')
sleep(1)
chrome.implicitly_wait(30)
chrome.find_element(by=By.XPATH, value='//button[@id="signInBtn"]').click()

chrome.implicitly_wait(30)
chrome.find_element(by=By.XPATH, value='//*[@id="navAccountUsername"]')

print('Sign in successfully.')

sess = Session()
sess.headers.clear()
sess.headers.update({'user-agent' : 'Mozilla/5.0'})
# 獲取 & 填充 cookies
cookies = chrome.get_cookies()
for cookie in cookies:
    sess.cookies.set(cookie['name'], cookie['value'])

start_at = 1
start_url = 'https://www.ancestry.com/search/collections/7488/?name=_Dos+Santos+Maciel+Neto&name_x=_1&count=50&fh=2000&fsk=MDsxOTk5OzUw'
name = '1	Nolet De Brauwere Van S'
id = search('(\d+)\s+', name).group(1)
last_name = search('\d+\s+(.+)', name).group(1)
#Get_name_list_and_Write_to_Excel(id, last_name, sess, start_at, start_url)        
Get_name_list_and_Write_to_Excel(id, last_name, sess)  