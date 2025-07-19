from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as uc
import json
import os

def save_cookies(driver, filepath):
    """保存 cookies 到文件"""
    with open(filepath, 'w') as f:
        json.dump(driver.get_cookies(), f)

def load_cookies(driver, filepath):
    """從文件載入 cookies"""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            cookies = json.load(f)
            for cookie in cookies:
                try:
                    driver.add_cookie(cookie)
                except:
                    pass

def wait_for_manual_verification(driver):
    """等待手動完成驗證"""
    print("請手動完成 Cloudflare 驗證...")
    while True:
        try:
            # 檢查是否還在驗證頁面
            if "cloudflare" in driver.current_url.lower():
                print("檢測到 Cloudflare 驗證頁面，等待中...")
                time.sleep(3)
                continue
            
            # 檢查頁面是否可以正常訪問
            if driver.find_elements(By.TAG_NAME, "body"):
                print("驗證完成！")
                break
                
        except Exception as e:
            time.sleep(2)
            continue

def login(driver, username, password):
    """登入功能"""
    try:
        # 等待登入表單載入
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "user_login"))
        )
        
        print("開始填寫登入資訊...")
        
        # 輸入用戶名和密碼
        username_field = driver.find_element(By.ID, "user_login")
        username_field.clear()
        username_field.send_keys(username)
        time.sleep(1)
        
        password_field = driver.find_element(By.ID, "user_password")
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(1)
        
        # 點擊登入按鈕
        login_button = driver.find_element(By.NAME, "commit")
        login_button.click()
        
        print("已點擊登入按鈕，等待登入完成...")
        time.sleep(5)
        
        return True
    except Exception as e:
        print(f"登入失敗: {e}")
        return False

def account_login(driver, user_name, password):
    print("開始登入流程...")
    
    try:
        cookies_file = "kktix_cookies.json"
        
        # 步驟1：先訪問主頁面
        print("正在訪問 KKTIX 主頁...")
        driver.get('https://kktix.com/')
        
        # 等待 Cloudflare 驗證
        wait_for_manual_verification(driver)
        
        # 載入之前保存的 cookies
        load_cookies(driver, cookies_file)
        
        # 刷新頁面以應用 cookies
        driver.refresh()
        time.sleep(3)
        
        # 步驟2：前往登入頁面
        print("正在訪問登入頁面...")
        driver.get('https://kktix.com/users/sign_in')
        
        # 再次等待可能的 Cloudflare 驗證
        wait_for_manual_verification(driver)
        
        # 步驟3：檢查是否需要登入
        if "sign_in" in driver.current_url:
            print("檢測到登入頁面，開始登入...")
            
            if login(driver, user_name, password):
                print("登入表單已提交")
                
                # 等待登入處理
                time.sleep(7)
                wait_for_manual_verification(driver)
                
                # 檢查登入結果
                current_url = driver.current_url
                if "sign_in" not in current_url:
                    print("登入成功！")
                    save_cookies(driver, cookies_file)
                    print("已保存 cookies 供下次使用")
                else:
                    print("登入可能失敗，請檢查帳號密碼或手動完成驗證")
                    
            else:
                print("登入失敗")
        else:
            print("可能已經登入或不需要登入")
        
        print("\n=== 登入流程完成 ===")
        print(f"當前 URL: {driver.current_url}")
        print("請檢查瀏覽器中的登入狀態")
        
    except Exception as e:
        print(f"執行過程中發生錯誤: {e}")
        input("按 Enter 鍵結束程序...")
    
    finally:
        # 可選：關閉瀏覽器
        # driver.quit()
        pass
