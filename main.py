from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as uc
import json
import os
from login_kktix import *
from get_ticket import *
import datetime

def main():
   
    user_name = input("請輸入 KKTIX 帳號(用戶名或gmail): ")
    password = input("請輸入 KKTIX 密碼: ")

    activity_url = input("請輸入活動連結: ")
    get_kind = input("請輸入執行方式(1.指定時間搶票, 2.立刻搶票): ")

    sell_hour, sell_minute, sell_second = 0, 0, 0
    if get_kind == "1":
        sell_hour, sell_minute, sell_second = map(int, input("請輸入開賣時間(24小時制)(格式: HH:MM:SS): ").split(':'))
    activity_name = activity_url.split("/")[-1]
    

    choose_kind = input("請輸入購買方式(1: 指定票價, 2: 有座位就好(每次會先嘗試1次指定票價)): ")
    price_key = input("請輸入想購買的票價，以空格分隔(例如: 1000 2000 3000)，輸入序位越前優先度越高: ").split()
    price_order = input('從區域便宜的開始購買嗎？(從最下面的區域往上判斷)(y/n): ').strip().lower()
    no_n = 0
    no_n = list(map(int, input("請輸入排除的票價(身障票等)，以空格分隔(例如: 1000 2000 3000): ").split()))
    count = input("請輸入購買數量: ")


     # 使用最簡單的設置
    options = uc.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1920,1080')
    
    driver = uc.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


    account_login(driver, user_name, password)
    get_active_ticket(driver, activity_name, price_key, choose_kind, count, price_order, no_n, sell_hour, sell_minute, sell_second, get_kind)
    input("購票完成，請按 Enter 鍵關閉瀏覽器...")


main()