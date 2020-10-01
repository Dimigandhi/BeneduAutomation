from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pymysql
import random
# from pydub import AudioSegment
# import speech_recognition as sr
import time
# import requests
# import io
NUMS_DICT = {
    "①" : 1,
    "②" : 2,
    "③" : 3,
    "④" : 4,
    "⑤" : 5
}
SUBJECT_DICT = {
    "korean" : '//*[@id="body_rdoSbjCode_0"]',
    "english" : '//*[@id="body_rdoSbjCode_2"]',
    "history" : '//*[@id="body_rdoSbjCode_3"]',
    "physics" : '//*[@id="body_rdoSbjCode_4"]',
    "chemistry" : '//*[@id="body_rdoSbjCode_5"]',
    "industry" : '//*[@id="body_rdoSbjCode_7"]',
    "drafting" : '//*[@id="body_rdoSbjCode_8"]'
}



def open_page(user_email, user_password):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://www.benedu.co.kr/index.aspx')
    assert "No results found." not in driver.page_source
    driver.implicitly_wait(3)
    driver.find_element_by_css_selector("ul.nav.navbar-nav.navbar-right").click()
    driver.find_element_by_name("inputEmail").send_keys(user_email)
    driver.find_element_by_name("inputPassword").send_keys(user_password)
    time.sleep(3)
    driver.find_element_by_css_selector("button#btnLogin.btn.btn-info.pull-right").click()
    driver.implicitly_wait(3)
    return driver

def gotoPage(driver):
    driver.find_element_by_css_selector('li#mnu03StdStudy.dropdown').click()
    time.sleep(random.randint(1,3))
    driver.find_element_by_css_selector('a[href="03StdStudy02PaperTestList.aspx"]').click()
    time.sleep(random.randint(1,3))
    itsnumber = str(driver.find_element_by_xpath('//*[@id="DT_TestList"]/tbody/tr[1]/td[2]').get_attribute("onclick"))
    itsnumber = itsnumber[itsnumber.find("ShowPop(\"")+9:itsnumber.find("\", ")]
    value = 1
    while(value<=9):
        driver.execute_script('DoCommentary('+itsnumber+','+str(value)+')')
        time.sleep(random.randint(4,6))
        pre_getAnswer(driver)
        time.sleep(random.randint(4,6))
        value += 1
    return driver


def createtestsheet(driver):
    time.sleep(2)
    driver.get('https://www.benedu.co.kr/Views/01_Students/03StdStudy01Question.aspx')
    driver.find_element_by_xpath(SUBJECT_DICT["english"]).click()
    time.sleep(1)
    #뽑아오는 문제는 3학년으로 한정.
    driver.find_element_by_xpath('//*[@id="body_chkGrade3"]').click()
    time.sleep(1)
    #모의고사, 수능 한정.
    driver.find_element_by_xpath('//*[@id="body_chkSrc01"]').click()
    time.sleep(1)
    #45문제 한정.
    driver.find_element_by_xpath('//*[@id="body_TextBox2"]').clear()
    driver.find_element_by_xpath('//*[@id="body_TextBox2"]').send_keys('45')
    time.sleep(1)
    #푼문제는 안뽑음. 답 받아올때만 이거 씀
    driver.find_element_by_xpath('//*[@id="body_chkOption01"]').click()
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="body_btnExecute"]').click()
    time.sleep(6)
    #저장.

    driver.find_element_by_xpath('//*[@id="btnSave2"]').click()
    time.sleep(6)
    
    driver.find_element_by_xpath('//*[@id="btnCancel"]').click()
    time.sleep(6)
    driver.get('https://www.benedu.co.kr/Views/01_Students/00StdHome.aspx')
    return driver


def pre_getAnswer(driver):
    html = driver.page_source

    parpage = str(BeautifulSoup(html, 'html.parser'))

    answer = []
    pIndex = parpage.find('AnswerCorrectImage')+30
    leftpage = parpage[pIndex+10:]
    #처음 함수를 건너뜀
    counts = 0
    while(leftpage.find('AnswerCorrectImage')!=-1):

        pIndex = leftpage.find('AnswerCorrectImage')+21
        answer.append(NUMS_DICT[leftpage[pIndex:pIndex+1]])
        leftpage = leftpage[pIndex+10:]
        counts = counts + 1

    print(answer)


    #찾는다.
def rand_delay(t):
    oper = random.choice(['plus','minus'])
    if(oper == 'plus'):
        time.sleep(t+random.randint(1,3))
    else:
        time.sleep(t-random.randint(1,3))
    return

driver = open_page(input(),input())
literation = int(input('몇번이나 할까?'))

for i in range(literation):
    #open_page는 내가 만든 함수메인 페이지까지 간다. 간 후 driver를 리턴한다.
    driver = gotoPage(driver)
    rand_delay(4)
    
    print("literation complete! counter: "+str(i))

