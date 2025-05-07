##Aerry##
# 帳號及密碼
username = ''#4b1900xx
password = ''
import io
import sys
from urllib.parse import urljoin
from PIL import Image, ImageChops
import ddddocr 
import os
import numpy as np
import onnxruntime
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.alert import Alert

import base64
import ddddocr 
import re
from datetime import datetime 
 #https://course.stust.edu.tw/CourSel/Login.aspx?ReturnUrl=%2fCourSel%2fBoard.aspx
LoginUrl = "https://course.stust.edu.tw/CourSel/Login.aspx?ReturnUrl=%2fCourSel%2fboard.aspx"

# 選課代號
className = ["無障礙生活"]#["體育生活(三)：游泳(C)"]#["西班牙文化"]
quitClass = ["無障礙生活"]
error_timeout_count = 0
ocr = 0
username = ''#input('請輸入帳號: ')#4b190031
password = ''#input('請輸入密碼: ')     
#模仿登入
uc_options = uc.ChromeOptions()
uc_options.add_argument('--mute-audio')      
browser = 0
f = 0
def myprint(str):
    currentDateAndTime = datetime.now() 
    out_text = f"{currentDateAndTime} ===> {str}\n"
    print(out_text)
    f = open('output.txt','a+')
    f.write(out_text)
    f.close()

def GetNumInStr(str):
    matches = re.search(r'\d+', str)
    num = -1
    if matches:
        num = int(matches[0])
    else:
        num = -1
    return num

def WaitObjId(browser,id):
    wait = WebDriverWait(browser, 3)
    try:
        element = wait.until(EC.presence_of_element_located((By.ID, f"{id}")))
        return True
    except TimeoutException: 
        global error_timeout_count
        error_timeout_count += 1
        return False
    
def 查詢課程(browser,classname):
    browser.get("https://course.stust.edu.tw/CourSel/Pages/QueryAndSelect.aspx")
    try:
        if(WaitObjId(browser,"__tab_ctl00_ContentPlaceHolder1_TabContainer1_TabPanel3")):
            browser.find_element(By.XPATH, 
                    '//*[@id="__tab_ctl00_ContentPlaceHolder1_TabContainer1_TabPanel3"]').click()#課程查詢
                
        if(WaitObjId(browser,"ctl00_ContentPlaceHolder1_TabContainer1_TabPanel3_txt_subname")):
            browser.find_element(By.XPATH, 
                    '//*[@id="ctl00_ContentPlaceHolder1_TabContainer1_TabPanel3_txt_subname"]').send_keys(classname)#課程名稱  

        browser.find_element(By.XPATH, 
            '//*[@id="ctl00_ContentPlaceHolder1_TabContainer1_TabPanel3_btn_querysub"]').click()#查詢
    except:
         查詢課程(browser,classname)
 
def 確認空位(browser):
    while True:
        for classs in className:#通常只會專住在一個課程上(太多課程 這邊判斷效率會變差) 所以其實不用陣列
            查詢課程(browser,classs)
            if(WaitObjId(browser,"ctl00_ContentPlaceHolder1_GridView1_ctl02_LinkButton1")):
                browser.find_element(By.XPATH, 
                    '//*[@id="ctl00_ContentPlaceHolder1_GridView1_ctl02_LinkButton1"]').click()#進入課程資料
                while True:
                    if(WaitObjId(browser,"ctl00_ContentPlaceHolder1_CourseDetail_onepage1_lab_count11")):
                        max = browser.find_element(By.XPATH, 
                            '//*[@id="ctl00_ContentPlaceHolder1_CourseDetail_onepage1_lab_count11"]').text #課程上限人數
                    if(WaitObjId(browser,"ctl00_ContentPlaceHolder1_CourseDetail_onepage1_lab_count12")):
                        current = browser.find_element(By.XPATH, 
                            '//*[@id="ctl00_ContentPlaceHolder1_CourseDetail_onepage1_lab_count12"]').text #課程目前人數
                    
                    myprint(f"人數 {GetNumInStr(current)} / {GetNumInStr(max)}")
    
                    if (GetNumInStr(current) < GetNumInStr(max)):
                        myprint("有位置,可以選了")
                        return;      
                    browser.refresh()
            else:
                continue


def Util() -> bool:

   
    #uc_options.add_argument('--headless') #隱藏 maybe bug
    
    #uc_options.add_argument("--incognito")
    #uc_options.add_argument('--disable-popup-blocking')
    #uc_options.add_argument("--force-device-scale-factor=0.8")
  
    ###browser.maximize_window() 
    if(error_timeout_count > 3):
        myprint("網頁出現錯誤 請重新打開程序")
        os.system("pause")
        return True
   
    browser.get(LoginUrl) 
    確認空位(browser)#這邊會先用訪客 確認該課程有空位 以免過多操作被判定機器人

    browser.delete_all_cookies() #清裡acookie以防網頁跟蹤 避免小bug
    #有空位後登入
    browser.get(LoginUrl) 
    if(WaitObjId(browser,"Login1_UserName")):
        browser.find_element(By.XPATH, 
            '//*[@id="Login1_UserName"]').send_keys(username)
        
    if(WaitObjId(browser,"Login1_Password")):
        browser.find_element(By.XPATH, 
            '//*[@id="Login1_Password"]').send_keys(password)
        
    if(WaitObjId(browser,"Login1_LoginButton")):
        browser.find_element(By.XPATH, 
            '//*[@id="Login1_LoginButton"]').click()
    myprint('登入成功')
    while True: 
        for classs in className:
            myprint('查詢課程')
            查詢課程(browser,classs)
            
            myprint('勾選課程')
            if(WaitObjId(browser,"ctl00_ContentPlaceHolder1_GridView1_ctl02_chb_select")):
                browser.find_element(By.XPATH, 
                    '//*[@id="ctl00_ContentPlaceHolder1_GridView1_ctl02_chb_select"]').click()#選擇課程打勾
            else:
                myprint( "重新偵測3") #結果
                return False
   
            myprint('辨識驗證碼')
            if not (WaitObjId(browser,"ctl00_ContentPlaceHolder1_img_captcha1")):
                myprint( "辨識出錯") #結果
                return False
            #這邊width加了20增加圖片寬度 方便圖片辨識ˋ
            #這邊參考了https://ithelp.ithome.com.tw/articles/10222515
            #const data = arguments[0]; , browser.find_element(By.ID,'ctl00_ContentPlaceHolder1_img_captcha1')
            img = browser.execute_script(
            """
            const data = document.getElementById('ctl00_ContentPlaceHolder1_img_captcha1');
            const canvas = document.createElement('canvas');
            canvas.width = data.width + 20;
            canvas.height = data.height;
            canvas.getContext('2d').drawImage(data, 0,  0);
            const dataURL = canvas.toDataURL('image/png');
            const base64 = dataURL.split(',')[1];
            return base64;
            """)
            img_data = base64.b64decode(img) 
            img_byte = Image.open(io.BytesIO(img_data))
             
            captcha = ocr.classification(img_byte)
            myprint(f'驗證碼{captcha}')
            myprint('送出請求')
            browser.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_txt_captcha"]').send_keys(captcha)#寫入驗證碼
            browser.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_btn_addsel"]').click()#送出選課
   
            if(WaitObjId(browser,"ctl00_ContentPlaceHolder1_gv_result_ctl02_Label6")):
                result = browser.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_gv_result_ctl02_Label6"]').text
                if(result.lower() == "加選成功".lower()):
                    myprint( classs + " => " + result) #結果
                    browser.quit()
                    return True
                elif(result.lower() == "重覆選課".lower()):
                    myprint( classs + " => " + result) #結果
                    if(quitClass[0].lower() != '0'):
                        myprint( quitClass[0] + " => " + "退選中") #結果
                        browser.get("https://course.stust.edu.tw/CourSel/Pages/SelectedAndDelete.aspx?role=S")
            
                        
                        # 定位目标 <a> 元素
                        a_element = browser.find_element(By.XPATH, f'//a[text()="{quitClass[0]}"]')
                        print(a_element.text)  # 确认找到的 <a> 元素是否正确
                        # 从 <a> 找到父级 <td>
                        td_element = a_element.find_element(By.XPATH, './parent::td')
                        print(td_element.text)  # 确认找到的 <a> 元素是否正确
                        # 从 <td> 找到父级 <tr>
                        tr_element = td_element.find_element(By.XPATH, './parent::tr')
                        tr_element.find_element(By.XPATH,'.//td')
                        print(tr_element.text)  # 确认找到的 <a> 元素是否正确
                    
        
                        # 找到该 <tr> 下的退選按钮并点击
                        drop_button = tr_element.find_element(By.XPATH, './/td/input[@type="submit" and @value="退選"]')
                        drop_button.click()

                        # 找到並點擊“退選”按鈕
                        #button = browser.find_element(By.ID, 'ctl00_ContentPlaceHolder1_gv_sel_ctl09_Button1')#談窗確定
                        #button.click()
                        alert = Alert(browser)
                        alert.accept()  # 點擊“確定”按鈕
                        alert = Alert(browser)
                        alert.accept()  # 點擊“確定”按鈕
                        myprint(quitClass[0] + "退選成功")
                    return False
                else:
                    myprint(f"未知訊息{result.lower()}, 重新偵測") #結果
                    return False
            else:
                myprint(f"選課送出失敗,未回傳任何東西, 重新偵測") #結果
                return False
            #browser.refresh()
            #continue

    wait.until(EC.url_contains("unknown"))#url_changes(browser.current_url))
#datas=[('./common_old.onnx','ddddocr'),('./onnxruntime_providers_shared.dll','onnxruntime\\capi')],
#
#
if __name__ == "__main__":
    f = open('output.txt','w')#使用w有助於每次打開文件都清空
     
    #請記得輸入帳號密碼
    #print('歡迎使用自動選課系統 請勿用做非法用途.販賣課程 此程序免費使用者的任何行為與開發者無關,請自行承擔責任')
    #print('使用ddddocr,及UD-ChromeDriver')
    #print('Discord: mem_callback')
    #print('Github: https://github.com/Aerry1337')
    myprint('歡迎使用自動選課系統')
    ocr = ddddocr.DdddOcr()#初始化驗證碼辨識   
    browser = uc.Chrome(uc_options)
    username = input('請輸入帳號: ')#4b190031
    password = input('請輸入密碼: ')    
    className.clear()
    className.append(input('請輸入完整課程名稱: '))#
    quitClass.clear()
    quitClass.append(input('請輸入退選課程名稱: '))#input('請輸入完整課程名稱: ')
   
    while True:
        if(Util() == False):
            browser.delete_all_cookies() #清裡acookie以防網頁跟蹤 避免小bug
            continue
        else:
            break
    myprint("程式結束")
    os.system("pause")
    exit(-1)
 