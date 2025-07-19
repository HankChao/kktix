from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import undetected_chromedriver as uc
import json
import os
import datetime

def wait_until_specific_time(sell_hour, sell_minute, sell_second):
    while True:
        # 获取当前时间
        now = datetime.datetime.now()
        
        # 设置目标时间
        target_time = now.replace(hour=sell_hour, minute=sell_minute, second=sell_second, microsecond=0)
        
        # 如果目标时间已经过去，则设置为第二天
        if now > target_time:
            target_time += datetime.timedelta(days=1)
        
        # 计算等待时间
        wait_seconds = (target_time - now).total_seconds()
        
        print(f"将在 {wait_seconds:.2f} 秒后启动脚本")
        time.sleep(wait_seconds)
        
        return  # 到达指定时间后退出函数
    
    
def get_active_ticket(driver, activity_name, price_key, choose_kind, count, price_order, no_n, sell_hour, sell_minute, sell_second, get_kind):

    ticket_url = f"https://kktix.com/events/{activity_name}/registrations/new"
    if get_kind == "1":#指定時間搶票
        wait_until_specific_time(sell_hour, sell_minute, sell_second)

    driver.get(ticket_url)

    zones = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "ticket-unit"))
    )

    zones.reverse() #預設從便宜開始購買

    for no_price in no_n:#排除指定票價
        for zone in zones:
            el = zone.find_element(By.CSS_SELECTOR, ".ticket-price .ng-binding")
            price = el.text.strip().replace("TWD$", "").replace(",", "")
            if no_price == int(price):#如果有排除的票價
                print(f"排除票價: {price}，從區域中移除")
                zones.remove(zone)

    if price_order == "n":#從貴開始購買
        zones.reverse()
    print(f"找到{len(zones)}個區域")

    have_sold = False
    while not have_sold:
        try:
            for zone in zones:
                el = zone.find_element(By.CSS_SELECTOR, ".ticket-price .ng-binding")
                print(el.text)
                price = el.text.strip().replace("TWD$", "").replace(",", "")  # 移除貨幣符號和逗號

                #指定票價或有座位就好(try 1 time)
                for key in price_key:#照順序確認區域票價
                    if key in price:
                        
                        inputs = zone.find_elements(By.TAG_NAME, "input")
                        print(inputs)
                        if inputs:
                            print(f"正在嘗試購買票價{price}...")
                            input_box = inputs[0]
                            input_box.clear()
                            input_box.send_keys(str(count))
                            input_box.send_keys(Keys.TAB)
                            print("✅ 成功輸入票數")
                            print(f"已成功購買票價{price}的{count}張票")
                            have_sold = True
                            break
                        else:
                            print(f"${price}票種已售完")
                            break
                        
                if have_sold:
                    break


            if choose_kind == "2" and not have_sold:#有座位就好
                for zone in zones:
                    el = zone.find_element(By.CSS_SELECTOR, ".ticket-price .ng-binding")
                    print(el.text)
                    price = el.text.strip()  

                    inputs = zone.find_elements(By.TAG_NAME, "input")
                    if inputs:
                        input_box = inputs[0]
                        input_box.clear()
                        input_box.send_keys(str(count))
                        input_box.send_keys(Keys.TAB)
                        print(f"已成功購買票價{price}的{count}張票")
                        have_sold = True
                        break
                    
                    else:
                        print(f"${price}已售完")
                        continue

            checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
            checkbox.click()


            try:
                auto_btn = driver.find_element(By.XPATH, "//button[span[text()='電腦配位']]")
                auto_btn.click()
                print("✅ 點擊了『電腦配位』按鈕")
            except:
                try:
                    next_btn = driver.find_element(By.XPATH, "//button[span[text()='下一步']]")
                    next_btn.click()
                    print("✅ 找不到『電腦配位』，已點擊『下一步』按鈕")
                except:
                    print("❌ 找不到任何可用的前往下一步按鈕")
        except:
            print('購票頁面載入失敗，重新載入...')
            driver.refresh()
            


        
