from select import select
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select
from time import sleep

userid = ''
userpass = ''
with open('userid.txt') as f:
    l = [s.strip() for s in f.readlines()]
    userid = l[0]
    userpass = l[1]

driver = webdriver.Chrome()

def login():
    driver.get("https://hayatabi.c-nexco.co.jp/drive/detail.html?id=135")
    #ログイン
    mailform =  driver.find_element(By.NAME, 'mail')
    mailform.send_keys(userid)
    passform = driver.find_element(By.NAME, 'passwd')
    passform.send_keys(userpass)
    loginbutton = driver.find_element(By.XPATH, '//*[@id="FORM_LOGIN"]/div[1]/div[2]/div/div/a')
    sleep(1)
    loginbutton.click()
    sleep(1)

#print(driver.page_source)

def checklist():
    #チェックリストを埋める
    checkbox1 = driver.find_element(By.ID, 'CHECK_STIPULATION')
    checkbox1.click()
    checkbox2 = driver.find_element(By.ID, 'CHECK_STIPULATION_BIKE')
    checkbox2.click()
    checkbox3 = driver.find_element(By.XPATH, '//*[@id="REQUIRED_QUESTION"]/ul[1]/li[9]/input')
    checkbox3.click()
    checkbox4 = driver.find_element(By.XPATH, '//*[@id="REQUIRED_QUESTION"]/ul[2]/li[2]/input')
    checkbox4.click()
    sleep(0.5)
    submitbutton = driver.find_element(By.XPATH, '//*[@id="aMainContents"]/div[3]/div[12]/a')
    submitbutton.click()
    sleep(0.5)
    Alert(driver).accept()
    
    #割引内容を選択(二輪車定率割引)
    dropdown1 = driver.find_element(By.NAME, 'course')
    select1 = Select(dropdown1)
    select1.select_by_value('1')

def checklist2():
    #ETCカードを選択
    dropdown2 = driver.find_element(By.NAME, 'etc')
    select2 = Select(dropdown2)
    select2.select_by_index(1)

    #車載機を選択
    dropdown3 = driver.find_element(By.NAME, 'onboard_number')
    select3 = Select(dropdown3)
    select3.select_by_index(1)

    #確認画面へ
    sleep(0.5)
    #submitbutton2 = driver.find_element(By.XPATH, '//*[@id="toConfirm"]/a')
    #submitbutton2.click()
    driver.execute_script("$('#toConfirm').submit()")


login()
checklist()

#予約可能な日付を取得
avail_date = []
cal_avail = driver.find_elements(By.CLASS_NAME, 'available')
del cal_avail[-1]
for i in range(len(cal_avail)):
    avail_date.append(cal_avail[i].get_attribute('id'))
print(avail_date)

fail_flag = 0
for i in range(len(avail_date)):
    if i >= 1 and fail_flag == 0:
        driver.get("https://hayatabi.c-nexco.co.jp/drive/detail.html?id=135")
        checklist()
    fail_flag = 0

    #予約する日付を選択
    select_date = driver.find_element(By.XPATH, '//*[@id="'+avail_date[i]+'"]/a')
    select_date.click()
    #//*[@id="1_2022_7_2"]/a

    checklist2()

    #予約済みチェック
    if len(driver.find_elements(By.XPATH, '//*[@id="departDate_1"]/dd/em')) > 0:
        print("Already reserved!", avail_date[i])
        fail_flag = 1
        continue

    #申し込み確定
    sleep(1)
    submitbutton3 = driver.find_element(By.XPATH, '//*[@id="toConfirm"]/a')
    submitbutton3.click()
    sleep(1)
    if len(driver.find_elements(By.XPATH, '//*[@id="aMainContents"]/div[3]/center/p')) > 0:
        print("Success!", avail_date[i])
        sleep(3)

print("Done!")
