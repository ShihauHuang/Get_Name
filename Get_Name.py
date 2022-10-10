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

def Get_name_list_and_Write_to_Excel(id, last_name, sess) :

    url = 'https://www.ancestry.com/search/collections/7488/?name=_' + last_name + '&name_x=_1&count=50'  # 起始網址
    
    i = 1
    while True: # 此情況較適合使用 while 而非 for，因無須先找取名字總數

        while True : # 發送 requests 時，會有低機率性回傳 502，所以讓他重新發送
            res = sess.get(url)
            if res.status_code != 200:
                print(str(res) + '___重新取得中')
                sleep(uniform(1 , 3)) # 隨機等待時間
                continue
            else :
                break
        soup = BeautifulSoup(res.text, 'html.parser')

        if i == 1 : # 於每個名字第一次搜尋時，先取得總數
            try :
                total = search( 'of\s+(.+)', soup.select('h3.w50')[0].text.strip()).group(1).replace(',', '')
            except :
                total = '0'
            with open ('Amount Check.txt', 'a+', encoding='utf-8') as f:
                f.write(str(id