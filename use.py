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

conn = pymysql.connect(host='115.68.231.45', port=3306, user=sql_user, password=sql_pw, database='benedu')
cursor = conn.cursor()
cursor.execute("SELECT * FROM answerSheet;")
rows = cursor.fetchall()

indexURL = 'https://benedu.co.kr/Index.aspx'
mainURL = 'https://www.benedu.co.kr/Views/01_Students/00StdHome.aspx'
testURL = 'https://www.benedu.co.kr/Views/01_Students/03StdStudy02PaperTestList.aspx'
createSheetURL = 'https://www.benedu.co.kr/Views/01_Students/03StdStudy01Question.aspx'

SUBJECT_DICT = {
    "korean" : '//*[@id="body_rdoSbjCode_0"]',
    "english" : '//*[@id="body_rdoSbjCode_2"]',
    "history" : '//*[@id="body_rdoSbjCode_3"]',
    "physics" : '//*[@id="body_rdoSbjCode_4"]',
    "chemistry" : '//*[@id="body_rdoSbjCode_5"]',
    "industry" : '//*[@id="body_rdoSbjCode_7"]',
    "drafting" : '//*[@id="body_rdoSbjCode_8"]'
}

def rand_delay(t):
    oper = random.choice(['plus','minus'])
    if(oper == 'plus'):
        time.sleep(t+random.randint(1,3))
    else:
        time.sleep(t-random.randint(1,3))
    return

def login(benID, benPW,driver):
    for i in range(15):
        print()
    print('------------------------------')
    print()

    driver.get(indexURL)
    time.sleep(0.2)
    assert "No results found." not in driver.page_source
    driver.find_element_by_xpath('//*[@id="liLogin"]/a').click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="inputEmail"]')))
    time.sleep(0.2)
    driver.find_element_by_xpath('//*[@id="inputEmail"]').send_keys(benID)
    driver.find_element_by_xpath('//*[@id="inputPassword"]').send_keys(benPW)
    time.sleep(0.2)
    driver.find_element_by_xpath('//*[@id="btnLogin"]').click()
    time.sleep(1.5)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="mnu06StdMyBenedu"]/a')))
    time.sleep(0.2)
    return driver

def createTestSheet(driver):
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="mnu03StdStudy"]/a')))
    driver.find_element_by_xpath('//*[@id="mnu03StdStudy"]/a').click()
    time.sleep(0.1)
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="mnu03StdStudy"]/ul/li[1]/a')))
    driver.find_element_by_xpath('//*[@id="mnu03StdStudy"]/ul/li[1]/a').click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id=\"tab_tag_1_1\"]')))
    while True:
        if EC.presence_of_all_elements_located:
            break
        else:
            continue
    time.sleep(0.2)

    driver.find_element_by_xpath(SUBJECT_DICT["english"]).click()
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

    WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="body_txtTestName"]')))
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnSave2"]')))
    driver.find_element_by_xpath('//*[@id="btnSave2"]').click()
    WebDriverWait(driver, 8).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="MessageForm"]/div/div/div[2]/div')))
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="btnCancel"]').click()
    time.sleep(0.2)

    return

def deletetestsheet(driver):
    driver.find_element_by_css_selector('li#mnu03StdStudy.dropdown').click()
    time.sleep(random.randint(1,3))
    driver.find_element_by_css_selector('a[href="03StdStudy02PaperTestList.aspx"]').click()
    time.sleep(random.randint(1,3))
    driver.find_element_by_xpath('//*[@id="DT_TestList"]/tbody/tr[1]/td[1]/input').click()
    driver.execute_script('Checked_Delete()')
    rand_delay(4)
    driver.execute_script('Checked_Delete_OK()')
    rand_delay(4)
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
        driver.execute_script('DoTakeExam('+itsnumber+','+str(value)+')')
        time.sleep(random.randint(4,6))
        solve(driver)
        time.sleep(random.randint(4,6))
        value += 1
    return

def toInt(tmpString):
    tmpst = ''
    for i in range(len(tmpString)):
        if(tmpString[i].isnumeric()):
            tmpst = tmpst+tmpString[i]
    return int(tmpst)

def checkProbNum(tmpval, probNum):
    answer = -1
    for row in rows:
        #row[0] : id, row[1] : answer, row[2]: author, row[3]: date, row[4]: description, row[5]: probnum
        if(probNum==row[1]):
            print('We did it!!!')
            return row[2]
    if(answer == -1):
            answer = random.randrange(1,6)
            
    return answer

def checking(driver, probIndex, answerNum):
    probIndex += 1
    js_script = "ClickAnswer(\""+str(probIndex)+"\",\""+str(answerNum)+"\")"
    driver.execute_script(js_script)
    time.sleep(random.randint(1,3))


def solve(driver):
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

    tmpval = 0
    probnum = []

    while(tmpval<5):
        probnum.append(toInt(prob[tmpval]))
        answer = checkProbNum(tmpval, probnum[tmpval])
        checking(driver, tmpval, answer)
        tmpval+=1

    # 시작시간 해결이 안되면 이 부분에 딜레이가 있어야 함.
    # driver.execute_script("grecaptcha = undefined") #캡챠 무시
    # iframes = driver.find_element_by_xpath("//*[@id=\"recaptcha\"]/div/div/iframe")
    # driver.switch_to_frame(iframes)

    # driver.find_element_by_xpath("//*[@id=\"recaptcha-anchor\"]/div[5]").click()
    #Recaptcha 뚫어야 하는 코드
    # time.sleep(60)
    # print('------------------------------')

    # driver.find_element_by_xpath("//*[@id=\"btnSubmit\"]").click()
    # getAnswerToDB(driver,probnum)

def useMain():
    # benID = input('Benedu Email: ')
    # benPW = input('Benedu Password: ')
    benID = 'mamy0320@naver.com'
    benPW = 'thdehehd1302'
    liter = int(input('문제 풀이 시트 개수'))

    driver = webdriver.Chrome('chromedriver.exe')
    #driver.maximize_window()

    driver = login(benID, benPW,driver)

    for i in range(liter):
        createTestSheet(driver)
        rand_delay(4)
        # login는 내가 만든 함수메인 페이지까지 간다. 간 후 driver를 리턴한다.
        gotoPage(driver)
        rand_delay(4)
        deletetestsheet(driver)
        rand_delay(4)
        cursor.execute("SELECT * FROM answerSheet;")
        rows = cursor.fetchall()
        print("liter complete! counter: " + str(i))
    conn.close()