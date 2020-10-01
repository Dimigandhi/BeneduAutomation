from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pymysql, random, time


sql_ip = '149.28.29.84'
sql_user = 'benedu_RW'
sql_pw = 'bendbpass!@'

indexURL = 'https://benedu.co.kr/Index.aspx'
mainURL = 'https://benedu.co.kr/Views/01_Students/00StdHome.aspx'
testURL = 'https://benedu.co.kr/Views/01_Students/03StdStudy02PaperTestList.aspx'
createSheetURL = 'https://www.benedu.co.kr/Views/01_Students/03StdStudy02PaperTestList.aspx'
taskURL = 'https://benedu.co.kr/Views/01_Students/03StdStudy04Homework.aspx'

NUMS_DICT = {
    "①": 1,
    "②": 2,
    "③": 3,
    "④": 4,
    "⑤": 5,
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
}

conn = pymysql.connect(host=sql_ip, port=3306, user=sql_user, password=sql_pw, database='benedu')
cursor = conn.cursor()
cursor.execute("SELECT * FROM answerSheet;")
rows = cursor.fetchall()


<<<<<<< HEAD
def login(benID, benPW):
=======
def login(benID, benPW,driver):
    for jj in range(15):
        print()
    print('------------------------------')
>>>>>>> 65030b749737dc35673d4b2cd5db29b3211c2930
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


def createTestSheet():
    # driver.get(createSheetURL)
    # time.sleep(0.5)

    time.sleep(0.5)
    driver.find_element_by_css_selector('#mnu03StdStudy > a').click()
    time.sleep(0.1)
    driver.find_element_by_css_selector('#mnu03StdStudy > ul > li:nth-child(1) > a').click()
    time.sleep(0.5)

    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, subject)))
    driver.find_element_by_css_selector(subject).click()
    time.sleep(0.2)

<<<<<<< HEAD
    # driver.find_element_by_css_selector('#body_chkGrade1').click()  # 1학년
    # time.sleep(0.2)
    # driver.find_element_by_css_selector('#body_chkGrade2').click()  # 2학년
    # time.sleep(0.2)
    # driver.find_element_by_css_selector('#body_chkGrade3').click()  # 3학년
    # time.sleep(0.2)

    # driver.find_element_by_css_selector('#body_chkSrc01').click()  # 모의고사만
    # time.sleep(0.2)
    driver.find_element_by_css_selector('#body_TextBox2').clear()  # 문항 수 삭제
    time.sleep(0.2)
    driver.find_element_by_css_selector('#body_TextBox2').clear()
    time.sleep(0.5)
    driver.find_element_by_css_selector('#body_TextBox2').send_keys('45')  # 문항 수 45
    time.sleep(0.5)
    driver.find_element_by_css_selector('#body_btnExecute').click()  # 검색
=======
    driver.find_element_by_xpath(SUBJECT_DICT["korean"]).click()
    time.sleep(1)
    # 뽑아오는 문제는 3학년으로 한정.
    driver.find_element_by_xpath('//*[@id="body_chkGrade3"]').click()
    time.sleep(1)
    # 모의고사, 수능 한정.
    driver.find_element_by_xpath('//*[@id="body_chkSrc01"]').click()
    time.sleep(1)
    # 45문제 한정.
    driver.find_element_by_xpath('//*[@id="body_TextBox2"]').clear()
    driver.find_element_by_xpath('//*[@id="body_TextBox2"]').send_keys('45')
    time.sleep(1)
    # 풀어본 문항 제외
    driver.find_element_by_xpath('//*[@id="body_chkOption01"]').click()
    time.sleep(1)
    # 문항 검색
    driver.find_element_by_xpath('//*[@id="body_btnExecute"]').click()
>>>>>>> 65030b749737dc35673d4b2cd5db29b3211c2930

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
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#btnDoTest')))  # 바로 응시하기 텍스트 대기
    time.sleep(0.5)

    return


def deleteSheet():
    driver.get(testURL)

    driver.find_element_by_css_selector(
        '#DT_TestList > tbody > tr:nth-child(1) > td:nth-child(1) > input[type="checkbox"]').click()  # 리스트 최상위 선택
    time.sleep(0.2)
    driver.find_element_by_css_selector('#container_left > button:nth-child(1)').click()  # 선택삭제버튼 클릭
    time.sleep(1)
    driver.find_element_by_css_selector(
        '#CheckAllDeleteForm > div > div > div.box-footer > button.btn.btn-default').click()  # 삭제버튼 클릭
    WebDriverWait(driver, 8).until(EC.visibility_of_element_located((
        By.CSS_SELECTOR, '#txtMessage')))  # 모두 삭제되었습니다 메시지 확인
    time.sleep(0.2)
    driver.find_element_by_css_selector(
        '#AlertForm > div > div > div.box-footer > div > div.container_item_c > button').click()  # 확인버튼

    return


def crawlTest():
    driver.get(testURL)
    time.sleep(0.5)

    # 1번을 응시하는 것이 아니라 CSS selector에서 CRAWLSHEET를 응시하도록 선택, deleteSheet도 동일하게 만들어야 함
    driver.find_element_by_css_selector('#DT_TestList > tbody > tr:nth-child(1) > td:nth-child(4)').click()  # 1번 응시
    time.sleep(0.2)
    
    itsnumber = str(driver.find_element_by_xpath('//*[@id="DT_TestList"]/tbody/tr[1]/td[2]').get_attribute("onclick"))
    itsnumber = itsnumber[itsnumber.find("ShowPop(\"")+9:itsnumber.find("\", ")]
    value = 1
    while(value<=9):
        global insert

        driver.execute_script('DoCommentary('+itsnumber+','+str(value)+')')
        time.sleep(0.2)
        parseAnswer(value)
        value += 1

    return


def toInt(tmpString):
    tmpst = ''
    for i in range(len(tmpString)):
        if tmpString[i].isnumeric():
            tmpst = tmpst+tmpString[i]

    return int(tmpst)


def checkDB(probNum):
    cursor.execute("SELECT qid FROM answerSheet WHERE qid=\'" + str(probNum) + "';")
    rows = cursor.fetchall()

    for row in rows:
        if probNum == row[0]:
            return False
    return True


def parseAnswer(value):
    html = driver.page_source

    parpage = str(BeautifulSoup(html, 'html.parser'))

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

    tmpval = 0
    probnum = []

    if len(answer) == 5:
        global insert, insertLoopDB
        while tmpval < 5:
            probnum.append(toInt(prob[tmpval]))

            if checkDB(probnum[tmpval]):
                insert += 1
                dbtuple = (probnum[tmpval], answer[tmpval])
                print(dbtuple)
                sql = "INSERT INTO answerSheet(qid,qans) VALUES(%s,%s)"
                cursor.execute(sql, dbtuple)
            tmpval += 1

        conn.commit()

    insertLoopDB += insert
    insert = 0
    print("Loop DB insertion: " + str(insertLoopDB) + "/" + str(value * 5))
    print()

    return


# MAIN function
benID = 'angrypig777@gmail.com'
# benID = input('Benedu Email: ')
# benPW = ''
benPW = input('Benedu Password: ')
for i in range(25):
    print()
print('------------------------------')

for i in SUBJECT_DICT:
    print(str(i))

print("크롤링할 과목 선택")
print()
while 1:
    try:
        global subject
        subject = input()
        subject = SUBJECT_DICT[subject]
        break
    except:
        print("Invalid subject - try again")


i = 0
insert = 0
insertLoopDB = 0
insertTotalDB = 0

driver = webdriver.Chrome('chromedriver.exe')
driver.maximize_window()
login(benID, benPW)


while 1:
    try:
        i += 1

        createTestSheet()
        time.sleep(0.5)

        crawlTest()
        time.sleep(0.5)

        deleteSheet()
        time.sleep(0.5)

        insertTotalDB += insertLoopDB
        insertLoopDB = 0
        print("Loop complete: " + str(i))
        print("Total DB insertion: " + str(insertTotalDB) + "/" + str(i * 45))
        print()

    except Exception as e:
        print()
        print("!@#!@#!@#!@#!@#!@#!@#!@#!@#!@#")
        print("BROAD ERROR: " + str(e) + "!@#!@#!@#!@#!@#!@#!@#!@#!@#!@#")
        print()

        driver.get(mainURL)
        pass
