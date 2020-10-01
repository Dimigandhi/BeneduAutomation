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
sql_user = 'benedu_READ'
sql_pw = 'benpass'

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


def login(benID, benPW):
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


def retrieveAnswer(prob_id):
    SQL = "SELECT qans FROM answerSheet WHERE qid=' " + str(prob_id) + "';"
    cursor.execute(SQL)
    result = cursor.fetchall()

    row_count = cursor.rowcount
    if row_count == 0:
        print("PROBID: " + str(prob_id) + " isn't in DB")
        return -1

    for x in result:
        probans = str(result).replace("(", "")
        probans = probans.replace(")", "")
        probans = probans.replace(",", "")
        probans = probans.replace(" ", "")
        return probans


def toInt(tmpString):
    tmpst = ''
    for i in range(len(tmpString)):
        if tmpString[i].isnumeric():
            tmpst = tmpst+tmpString[i]

    return int(tmpst)


def markAnswer(probIndex, answerNum):
    probIndex += 1

    js_script = 'ClickAnswer("' + str(probIndex) + '", "' + str(answerNum) + '");'
    try:
        driver.execute_script(js_script)
        print(js_script)

    except:
        try:
            time.sleep(0.2)
            number = driver.find_element_by_css_selector(
                '#AnswerArea > div > div > div:nth-child(1) > div > div > table > tbody > tr:nth-child(1) > td:nth-child(1)').text
            number = int(number) - 1 + probIndex
            element = "#btn_" + str(number) + "_" + str(answerNum)
            driver.find_element_by_css_selector(element).click()
            time.sleep(0.1)

        except:
            print("Error_Element: " + str(element))
            time.sleep(0.2)
            return 0
    return 1


def process():
    time.sleep(1)

    probnum = 0
    
    html = driver.page_source
    html = str(BeautifulSoup(html, 'html.parser'))

    # print(html)
    # for i in range(15):
    #     print()

    while probnum < 5:
        html_qid = html.find('문항ID : ') + 7
        prob_id = int(html[html_qid:html_qid + 7].replace(" ", ""))
        prob_ans = retrieveAnswer(prob_id)

        if prob_ans == -1:
            print("QID[" + str(prob_id) + "] not stored in DB")
        else:
            print("ProbNUM[" + str(probnum+1) + "]: prob_id[" + str(prob_id) + "]: prob_ans[" + str(prob_ans) + "]")

            mark_suc = 0
            while mark_suc:
                mark_suc = markAnswer(probnum, prob_ans)


        probnum += 1
        html = html[html_qid + 10:]


# MAIN function
benID = 'angrypig777@gmail.com'
# benID = input('Benedu Email: ')
# benPW = ''
benPW = input('Benedu Password: ')
for i in range(25):
    print()
print('------------------------------')

loop = 0

driver = webdriver.Chrome('chromedriver.exe')
driver.maximize_window()
login(benID, benPW)

try:
    driver.find_element_by_css_selector('#mnu03StdStudy > a').click()
    time.sleep(0.1)
    driver.find_element_by_css_selector('#mnu03StdStudy > ul > li:nth-child(5) > a').click()  # 과제 목록
    # driver.find_element_by_css_selector('#mnu03StdStudy > ul > li:nth-child(3) > a').click()  # 시험지 목록
    time.sleep(0.5)
except Exception as e:
    print("ERROR: " + str(e))
    pass

while 1:
    while "TakeExam.aspx" not in str(driver.current_url):
        time.sleep(0.5)

    loop += 1
    process()
    CurURL = str(driver.current_url)
    print("Loop complete: " + str(loop))

    while CurURL == str(driver.current_url):
        time.sleep(0.5)
