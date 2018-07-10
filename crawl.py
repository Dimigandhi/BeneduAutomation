from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import pymysql
import random
from pydub import AudioSegment
import speech_recognition as sr
import time
import requests
import io


CLIENT_ID = "1027360838218-0c36067e7dtg6cbspb9p4tl6svgshbqn.apps.googleusercontent.com"
CLIENT_KEY = "-jS5d_00O71rqOir9ViMvg4X"

sql_pw = input("sql 비밀번호를 입력하세요:")
sql_user = '1kl1'

DIGITS_DICT = {
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

conn = pymysql.connect(host='localhost', port=3306, user=sql_user, password=sql_pw, database='benedu')
cursor = conn.cursor()
cursor.execute('SELECT * FROM answersheet;')
rows = cursor.fetchall()
sqlflag = [0,0,0,0,0] # 0 이면 안하고 1이면 해라

#rand_delay는 받는 시간 +-5초 사이의 딜레이를 준다.... 최소 5초는 줘라
def rand_delay(t):
    oper = random.choice(['plus','minus'])
    if(oper == 'plus'):
        time.sleep(t+random.randint(1,4))
    else:
        time.sleep(t-random.randint(1,4))
    return
    

def open_page(user_email, user_password):
    driver = webdriver.Chrome("chromedriver.exe")
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
    driver.implicitly_wait(3)
    #
    driver.find_element_by_xpath('//*[text()[contains(.,\'ㅂㅇㄹㅂㅇㄹ\')]]').click()
    time.sleep(random.randint(1,3))
    itsnumber = str(driver.find_element_by_xpath('//*[@id="DT_TestList"]/tbody/tr[1]/td[2]').get_attribute("onclick"))
    itsnumber = itsnumber[itsnumber.find("ShowPop(\"")+9:itsnumber.find("\", ")]
    value = 1
    # 밑에 value <= [문제지 개수임 ㅋㅋ]
    while(value<=1):
        driver.execute_script("DoTakeExam("+itsnumber+","+str(value)+")")
        time.sleep(random.randint(1,3))
        driver.implicitly_wait(2)
        solve(driver)
        value += 1
        sqlflag = [0,0,0,0,0]

    
# 문항번호가 몇자리인지 몰라서만든 함수.
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
        if(probNum==row[5]):
            answer = row[1]
    if(answer == -1):   
            answer = random.randrange(1,6)
            sqlflag[tmpval] = 1
    return answer


def checking(driver, probIndex, answerNum):
    probIndex += 1
    js_script = "ClickAnswer(\""+str(probIndex)+"\",\""+str(answerNum)+"\")"
    driver.execute_script(js_script)
    time.sleep(random.randint(1,3))

def getAnswerToDB(driver,probNum):
    for i in range(5):
        j = 0
        for j in range(5):
            if(sqlflag[i]==0):
                break
            select = driver.find_element_by_xpath("//*[@id=\"frmBenedu\"]/div[3]/section[2]/div[2]/div[3]/div/div/div[1]/div/div/table/tbody/tr["+str(i+1)+"]/td["+str(j+2)+"]/span")
            if(select.get_attribute("class")=="badge bg_red"):
                answerReal = select.text()
                sql = "INSERT INTO answersheet (answer,author,created,category,number) VALUES("+answerReal+",,NOW(),'여기',"+probNum[i]+");"
                cursor.execute('SELECT * FROM answersheet;')
            

        
def is_exists_by_xpath(driver, xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True
    
def string_to_digits(recognized_string):
    return ''.join([DIGITS_DICT.get(word, "") for word in recognized_string.split(" ")])

def TTS(audio_source):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_source) as source:
        audio = recognizer.record(source) 

    audio_output = ""

    try:
        audio_output = recognizer.recognize_google(audio)

        if any(character.isalpha() for character in audio_output):
            print("숫자가 나왔다.")
            audio_output = string_to_digits(recognizer.recognize_houndify(audio, client_id=CLIENT_ID, client_key=CLIENT_KEY))
            print("DEBUG: "+audio_output)
    except sr.UnknownValueError:
        print("모르는 에러")
    except sr.RequestError as e:
        print("Google Speach Request ERR")

        
    return audio_output

def BREAKRECAPTCHA(driver):
    # 이녀석이 리캡차 내부 /html/body/div[4]/div[4]/iframe 내부버튼 //*[@id="recaptcha-audio-button"]
    rand_delay(5)
    iframe = driver.find_element_by_xpath("/html/body/div[4]/div[4]/iframe")
    driver.switch_to_frame(iframe)
    
    if(is_exists_by_xpath(driver,"//*[@id=\"recaptcha-audio-button\"]")):
        driver.find_element_by_xpath("//*[@id=\"recaptcha-audio-button\"]").click()
        rand_delay(5)
        download_object = driver.find_element_by_xpath("/html/body/div/div/div[6]/a")
        download_link = download_object.get_attribute('href')
        rand_delay(5)
        request = requests.get(url) #오디오 파일을 리퀘스트한다.
        audio_file = io.BytesIO(request.content)
            
        converted_audio = io.BytesIO()
        sound = AudioSegment.from_mp3(audio_file)
        sound.export(converted_audio, format="wav")
        converted_audio.seek(0)

        audio_output = TTS(converted_audio)
        driver.find_element_by_xpath("//*[@id=\"audio-response\"]").send_keys(audio_output)
        rand_delay(5)
        driver.find_element_by_xpath("//*[@id=\"recaptcha-verify-button\"]").click()#submit
        rand_delay(5)
    else:
        print("오디오테스트가 아니다.")


    




#solve는 아직 문항ID값을 추출해오는거밖에 안했다.
def solve(driver):
    html = driver.page_source
    parpage = str(BeautifulSoup(html, 'html.parser'))

    print('DEBUG: parsing through String')
    prob = []
    pIndex = parpage.find('문항ID : ')+7
    prob.append(parpage[pIndex:pIndex+5])
    leftpage = parpage[pIndex+10:]
    pIndex = leftpage.find('문항ID : ')+7
    prob.append(leftpage[pIndex:pIndex+5])
    leftpage = leftpage[pIndex+10:]
    pIndex = leftpage.find('문항ID : ')+7
    prob.append(leftpage[pIndex:pIndex+5])
    leftpage = leftpage[pIndex+10:]
    pIndex = leftpage.find('문항ID : ')+7
    prob.append(leftpage[pIndex:pIndex+5])
    leftpage = leftpage[pIndex+10:]
    pIndex = leftpage.find('문항ID : ')+7
    prob.append(leftpage[pIndex:pIndex+5])

    tmpval = 0
    probnum = []
    
    while(tmpval<5):
        probnum.append(toInt(prob[tmpval]))
        answer = checkProbNum(tmpval, probnum[tmpval])
        checking(driver, tmpval, answer)
        tmpval+=1
    
    # 시작시간 해결이 안되면 이 부분에 딜레이가 있어야 함.
    # driver.execute_script("grecaptcha = undefined") #캡챠 무시
    iframes = driver.find_element_by_xpath("//*[@id=\"recaptcha\"]/div/div/iframe")
    driver.switch_to_frame(iframes)
    
    driver.find_element_by_xpath("//*[@id=\"recaptcha-anchor\"]/div[5]").click()
    

    if(is_exists_by_xpath(driver, "//span[@aria-checked=\"true\"]")):
        driver.find_element_by_xpath("//*[@id=\"btnSubmit\"]").click()
        driver.switch_to_default_content()
        getAnswerToDB(driver,probnum)
    
    else:
        driver.switch_to_default_content()
        BREAKRECAPTCHA(driver)

        
    

    
# 이부분이 메인
driver = open_page(input("Email 입력해주세요"),input("비밀번호를 입력해보세요"))
#open_page는 내가 만든 함수메인 페이지까지 간다. 간 후 driver를 리턴한다.
gotoPage(driver)
conn.close()
#gotoPage 함수에선 문제를 생성은 안하고 푸는것만 함. 아직 미완성 안에 solve함수를 문제 시트마다 접근한다.
