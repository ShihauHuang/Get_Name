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
import threading

def Execute_range(start_id, end_id, name_list, thread_id) :
    
    for name in name_list :
        id = search('(\d+)\s+', name).group(1)
        last_name = search('\d+\s+(.+)', name).group(1)
        if int(id) >= start_id and int(id) <= end_id : # 從哪個 id ~ 哪個 id
            Get_name_list_and_Write_to_Excel(id, last_name, sess, thread_id)

def Get_name_list_and_Write_to_Excel(id, last_name, sess, thread_id) :

    url = 'https://www.ancestry.com/search/collections/7488/?name=_' + last_name + '&name_x=_1&count=50'  # 起始網址
    
    i = 1
    while True: # 此情況較適合使用 while 而非 for，因無須先找取名字總數

        while True : # 發送 requests 時，會有低機率性回傳 502，所以讓他重新發送
            try :
                res = sess.get(url)
                if res.status_code != 200:
                    print(thread_id + str(res) + '___重新取得中')
                    sleep(uniform(1 , 3)) # 隨機等待時間
                    continue
                else :
                    break
            except :
                print(thread_id + 'get fail___重新取得中')
                continue
        soup = BeautifulSoup(res.text, 'html.parser')

        if i == 1 : # 於每個名字第一次搜尋時，先取得總數
            try :
                total = search( 'of\s+(.+)', soup.select('h3.w50')[0].text.strip()).group(1).replace(',', '')
            except :
                total = '0'
            with open ('Amount Check_' + thread_id + '.txt', 'a+', encoding='utf-8') as f:
                f.write(str(id) + '_Last name "' + last_name + '" total : ' + total + '     ')
            #with open ('Amount Check with page_' + thread_id + '.txt', 'a+', encoding='utf-8') as f:
            #    f.write(str(id) + '_Last name "' + last_name + '" total : ' + total + '\n')
            print(thread_id + 'Last name "' + last_name + '" total : ' + total)

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

            with open ('Name list_' + thread_id + '.csv', 'a+', encoding='utf-8', newline='') as csvfile :
                writer = csv.writer(csvfile)
                writer.writerow([id, Name, Birth_Year, Arrival_Date, Departure_Port, Ethnicity_and_Nationality, Ship_Name])

        try:

            if items != [] : 
                print(thread_id + 'Page ' + str(i) + ' ----------------------------------- Done')
                #with open ('Amount Check with page_' + thread_id + '.txt', 'a+', encoding='utf-8') as f:
                #    f.write('Page ' + str(i) + ' ----------------------------------- Done\n')

                next_link = soup.select('li.next a')[0]['href']
                url = 'https://www.ancestry.com/search/collections/7488/' + next_link
                i = i + 1
                #with open ('Amount Check with page_' + thread_id + '.txt', 'a+', encoding='utf-8') as f:
                #    f.write('Page ' + str(i) + '___' + url + '\n')
            else:
                raise
                
        except Exception as e:
            max_amount_check = i * 50
            print(thread_id + 'max_amount_check : ' + str(max_amount_check))
            print(thread_id + 'total : ' + str(total))
            #with open ('check_' + thread_id + '.txt', 'w+', encoding='utf-8') as f:
            #    f.write( str(res) + '\n' + str(soup) + '\n')
            if max_amount_check >= int(total) or i >= 101:
                if i >= 101 : # 使 log 方便閱讀
                    i = 100
                with open ('Amount Check_' + thread_id + '.txt', 'a+', encoding='utf-8') as f:
                    f.write( 'Search Pages: ' + str(i) + '\n')
                break
            elif items == [] : # 得到 200，但沒有回傳正常數據
                print(thread_id + '重新取得 item')
                continue
            else :
                #with open ('Amount Check with page_' + thread_id + '.txt', 'a+', encoding='utf-8') as f:
                #    f.write( str(res) + '\n' + str(items) + '\n')
                print(thread_id + str(e) )
                _exit(0)

cmd = r'"C:\Program Files\Google\Chrome\Application\chrome.exe" https://www.ancestry.com/account/signin --remote-debugging-port=9222 --user-data-dir="C:\Users\Shihau\Documents\Selenium\ChromeProfile" --incognito'
Popen(cmd, shell=True)
sleep(6) # 需讓網頁等待一點時間，否則會被判定為機器人

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome = webdriver.Chrome(options=chrome_options)

chrome.implicitly_wait(30)
user_acct = chrome.find_element(by=By.XPATH, value='//input[@id="username"]')
user_acct.clear()
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

with open ('Final column for python2 with ID.csv', encoding='ISO-8859-1') as cc :
    name_list =  list(map(lambda x: x.strip(), cc.readlines()))

run_threads = [] # 使用多執行續去抓取 data
range_list = [[2243, 2275], [2276, 2300], [2376, 2400], [2345, 2375]] # 從哪裡開始~哪裡結束
#range_list = [ [4898, 1621], [14775, 14775]] # 從哪裡開始~哪裡結束
for t in range (len(range_list)) : # 建立 x 個多行續
    run_threads.append(threading.Thread(target=Execute_range , args=(range_list[t][0], range_list[t][1], name_list, str(t),)))
for tt in run_threads:
    tt.start()
    sleep(0.2)
for tt in run_threads:
    tt.join()


       
#name = '4	De Alba De Gandiaga'
#id = search('(\d+)\s+', name).group(1)
#last_name = search('\d+\s+(.+)', name).group(1)
#Get_name_list_and_Write_to_Excel(id, last_name, sess)        


#5001 ~ 10000
#15001 ~ 20000