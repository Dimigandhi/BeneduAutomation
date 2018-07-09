import open_Driver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def open_page(user_email, user_password):
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get('https://www.benedu.co.kr/index.aspx')
    assert "No results found." not in driver.page_source
    driver.implicitly_wait(3)
    driver.find_element_by_css_selector("ul.nav.navbar-nav.navbar-right").click()
    driver.find_element_by_name("inputEmail").send_keys(user_email)
    driver.find_element_by_name("inputPassword").send_keys(user_password)
    driver.find_element_by_css_selector("button#btnLogin.btn.btn-info.pull-right").click()
    driver.implicitly_wait(3)
    return driver

def gotoPage(driver):
    driver.find_element_by_css_selector('li#mnu03StdStudy.dropdown').click()
    driver.find_element_by_css_selector('a[href="03StdStudy02PaperTestList.aspx"]').click()
    driver.implicitly_wait(3)
    driver.find_element_by_xpath('//*[text()[contains(.,\'ㅂㅇㄹㅂㅇㄹ\')]]').click()
    itsnumber = str(driver.find_element_by_xpath('//*[@id="DT_TestList"]/tbody/tr[1]/td[2]').get_attribute("onclick"))
    itsnumber = itsnumber[itsnumber.find("ShowPop(\"")+9:itsnumber.find("\", ")]
    value = 1
    while(value<=1):
        driver.execute_script("DoTakeExam("+itsnumber+","+str(value)+")")
        solve(driver)
        value += 1
    
# 문항번호가 몇자리인지 몰라서만든 함수.
def toInt(tmpString):
    tmpst = ''

    for i in range(len(tmpString)):
        if(tmpString[i].isnumeric()):
            tmpst = tmpst+tmpString[i]
    return int(tmpst)

#solve는 아직 문항ID값을 추출해오는거밖에 안했다.
def solve(driver):
    html = driver.page_source
    parpage = str(BeautifulSoup(html, 'html.parser'))

    print('DEBUG: parsing through String')
    prob = []
    pIndex = parpage.find('문항ID : ')+7
    prob.append(parpage[pIndex:pIndex+5])
    leftpage = parpage[pIndex+5:]
    pIndex = parpage.find('문항ID : ')+7
    prob.append(parpage[pIndex:pIndex+5])
    leftpage = parpage[pIndex+5:]
    pIndex = parpage.find('문항ID : ')+7
    prob.append(parpage[pIndex:pIndex+5])
    leftpage = parpage[pIndex+5:]
    pIndex = parpage.find('문항ID : ')+7
    prob.append(parpage[pIndex:pIndex+5])
    leftpage = parpage[pIndex+5:]
    pIndex = parpage.find('문항ID : ')+7
    prob.append(parpage[pIndex:pIndex+5])

    tmpval = 0
    while(tmpval<5):
        probnum = toInt(prob[tmpval])
        print(probnum)
        tmpval+=1

    

    

# 이부분이 메인
try :
    driver = open_page(usr_id, usr_pw)
except:
    driver = open_page(input("Email 입력해주세요"),input("비밀번호를 입력해보세요"))
    #open_page는 내가 만든 함수메인 페이지까지 간다. 간 후 driver를 리턴한다.
    gotoPage(driver)
    #gotoPage 함수에선 문제를 생성은 안하고 푸는것만 함. 아직 미완성 안에 solve함수를 문제 시트마다 접근한다.


# 이 밑부분은 DB 접속할때 쓸 부분

# conn = pymysql.connect(host='localhost', port=3306, user='1kl1', password='', database='benedu')
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM answersheet;')
# res = cursor.fetchall()
# print(res)
# conn.close()