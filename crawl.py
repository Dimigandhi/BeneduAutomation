from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pymysql, random, time


sql_user = 'benedu_RW'
sql_pw = 'bendbpass!@'

NUMS_DICT = {
    "①" : 1,
    "②" : 2,
    "③" : 3,
    "④" : 4,
    "⑤" : 5,
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

SUBJECT_DICT = {
    # !!수학은 주관식 추가해야함!!
    "korean": '#body_rdoSbjCode_0',
    "math": '#body_rdoSbjCode_1',
    "english": '#body_rdoSbjCode_2',
    "history": '#body_rdoSbjCode_3',
    "physics1": '#body_rdoSbjCode_4',
    "chemistry1": '#body_rdoSbjCode_5',
    "science": '#body_rdoSbjCode_6',
    "industry": '#body_rdoSbjCode_7',
    "drafting": '#body_rdoSbjCode_8'

    # "korean" : '//*[@id="body_rdoSbjCode_0"]',
    # "english" : '//*[@id="body_rdoSbjCode_2"]',
    # "history" : '//*[@id="body_rdoSbjCode_3"]',
    # "physics" : '//*[@id="body_rdoSbjCode_4"]',
    # "chemistry" : '//*[@id="body_rdoSbjCode_5"]',
    # "industry" : '//*[@id="body_rdoSbjCode_7"]',
    # "drafting" : '//*[@id="body_rdoSbjCode_8"]'
}

indexURL = 'https://benedu.co.kr/Index.aspx'
mainURL = 'https://www.benedu.co.kr/Views/01_Students/00StdHome.aspx'
testURL = 'https://www.benedu.co.kr/Views/01_Students/03StdStudy02PaperTestList.aspx'
createSheetURL = 'https://www.benedu.co.kr/Views/01_Students/03StdStudy02PaperTestList.aspx'

conn = pymysql.connect(host='115.68.231.45', port=3306, user=sql_user, password=sql_pw, database='benedu')
cursor = conn.cursor()
cursor.execute("SELECT * FROM answerSheet;")
rows = cursor.fetchall()


def login(benID, benPW):
    for i in range(15):
        print()
    print('------------------------------')
    print()

    driver.get(indexURL)
    time.sleep(0.2)
    assert "No results found." not in driver.page_source

    driver.find_element_by_css_selector('#liLogin > a').click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#inputEmail')))
    time.sleep(0.2)
    driver.find_element_by_css_selector('#inputEmail').send_keys(benID)
    time.sleep(0.1)
    driver.find_element_by_css_selector('#inputPassword').send_keys(benPW)
    time.sleep(0.2)
    driver.find_element_by_css_selector('#btnLogin').click()
    time.sleep(0.2)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#mnu02StdGrade > a')))
    time.sleep(1.2)

    return


def rand_delay(t):
    oper = random.choice(['plus','minus'])
    if(oper == 'plus'):
        time.sleep(t+random.randint(1,3))
    else:
        time.sleep(t-random.randint(1,3))
    return


def createTestSheet():
    driver.get(createSheetURL)
    time.sleep(0.5)

    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, SUBJECT_DICT['korean'])))
    driver.find_element_by_css_selector(SUBJECT_DICT['korean']).click()
    time.sleep(0.2)

    driver.find_element_by_css_selector('#body_chkGrade2').click()  # 2학년
    time.sleep(0.2)
    driver.find_element_by_css_selector('#body_chkSrc01').click()  # 모의고사만
    time.sleep(0.2)
    driver.find_element_by_css_selector('#body_chkSrc01').clear()  # 문항 수 삭제
    time.sleep(0.5)
    driver.find_element_by_css_selector('#body_chkSrc01').send_keys('45')  # 문항 수 45
    time.sleep(0.5)
    driver.find_element_by_css_selector('#body_btnExecute').click()  # 검색

    WebDriverWait(driver, 8).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#body_txtTestName')))
    WebDriverWait(driver, 8).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnSave2')))  # 저장 버튼 로딩까지 대기
    time.sleep(0.8)
    driver.find_element_by_css_selector('#body_txtTestName').clear()
    time.sleep(0.5)
    driver.find_element_by_css_selector('#body_txtTestName').send_keys('CRAWLSHEET')
    time.sleep(0.2)
    driver.find_element_by_css_selector('#btnSave2').click()
    WebDriverWait(driver, 8).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#btnDoTest')))  # 바로 응시하기 나올때까지 대기
    time.sleep(0.5)

    return


def deletetestsheet(driver):
    driver.find_element_by_css_selector('li#mnu03StdStudy.dropdown').click()
    time.sleep(random.randint(1,3))
    driver.find_element_by_css_selector('a[href="03StdStudy02PaperTestList.aspx"]').click()
    time.sleep(random.randint(1,3))
    driver.find_element_by_xpath('//*[@id="DT_TestList"]/tbody/tr[1]/td[1]/input').click()
    driver.execute_script('Checked_Delete()')
    time.sleep(0.5)
    driver.execute_script('Checked_Delete_OK()')
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="AlertForm"]/div/div/div[3]/div/div[2]/button').click()
    time.sleep(2)
    return


def gotoPage(driver):
    time.sleep(random.randint(2,4))
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
    return


def toInt(tmpString):
    tmpst = ''
    for i in range(len(tmpString)):
        if(tmpString[i].isnumeric()):
            tmpst = tmpst+tmpString[i]
    return int(tmpst)


def findDB(probNum):
    cursor.execute("SELECT * FROM answerSheet;")
    rows = cursor.fetchall()
    for row in rows:
        # row[0] : id, row[1] : qid, row[2] : qans, row[3]: qtext, row[4]:timestamp
        if(probNum == row[1]):
            return False
    return True


def pre_getAnswer(driver):
    html = driver.page_source

    parpage = str(BeautifulSoup(html, 'html.parser'))

    print('DEBUG: parsing through String')
    prob = []

    pIndex = parpage.find('문항ID : ')+7
    prob.append(parpage[pIndex:pIndex+7])
    leftpage = parpage[pIndex+10:]
    pIndex = leftpage.find('문항ID : ')+7
    prob.append(leftpage[pIndex:pIndex+7])
    leftpage = leftpage[pIndex+10:]
    pIndex = leftpage.find('문항ID : ')+7
    prob.append(leftpage[pIndex:pIndex+7])
    leftpage = leftpage[pIndex+10:]
    pIndex = leftpage.find('문항ID : ')+7
    prob.append(leftpage[pIndex:pIndex+7])
    leftpage = leftpage[pIndex+10:]
    pIndex = leftpage.find('문항ID : ')+7
    prob.append(leftpage[pIndex:pIndex+7])

    parpage = str(BeautifulSoup(html, 'html.parser'))

    answer = []
    pIndex = parpage.find('AnswerCorrectImage')+30
    leftpage = parpage[pIndex+10:]
    # 처음 함수를 건너뜀
    while(leftpage.find('AnswerCorrectImage')!=-1):

        pIndex = leftpage.find('AnswerCorrectImage')+21
        answer.append(NUMS_DICT[leftpage[pIndex:pIndex+1]])
        leftpage = leftpage[pIndex+10:]
    # 찾는다.
    # AnswerCorrectImage


# //*[@id="question_2"]/table/tbody/tr[2]/td[2]
# //*[@id="question_3"]/table/tbody/tr[2]/td[2]

    # answer = []

    tmpval = 0
    probnum = []

    # for k in range(5):
    #     for m in range(5):
    #         xp = "//*[@id=\"question_"+str(k)+"\"]/table/tbody/tr[2]/td["+str(m+1)+"]/span"

    #         try:
    #             numElement = driver.find_element_by_xpath(xp)
    #             if(numElement.value_of_css_property('color')=="rgba(255, 0, 0, 1)"):
    #                 answer.append(NUMS_DICT[numElement.text])

    #         except NoSuchElementException as identifier:
    #             print("pass!")

    # print(probnum)
    # print(answer)
    if(len(answer) == 5):
        while(tmpval < 5):
            probnum.append(toInt(prob[tmpval]))
            if(findDB(probnum[tmpval])):
                dbtuple = (probnum[tmpval], answer[tmpval])
                print(dbtuple)
                sql = "INSERT INTO answerSheet(qid,qans) VALUES(%s,%s)"
                cursor.execute(sql, dbtuple)
            print("SQL Executed")
            tmpval += 1
        conn.commit()


# MAIN function
benID = 'angrypig777@gmail.com'
# benID = input('Benedu Email: ')
# benPW = ''
benPW = input('Benedu Password: ')
i=0

driver = webdriver.Chrome('chromedriver.exe')
# driver.maximize_window()

login(benID, benPW)

while 1:
    createTestSheet()
    time.sleep(0.5)

    gotoPage(driver)
    time.sleep(0.5)

    deletetestsheet(driver)
    time.sleep(0.5)
    print("Loop complete: " + i)

# conn.close()

# gotoPage 함수에선 문제를 생성은 안하고 푸는것만 함. 아직 미완성 안에 solve함수를 문제 시트마다 접근한다.
