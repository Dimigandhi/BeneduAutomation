# 밑에 value <= [문제지 개수임 ㅋㅋ]

########################## 이 부분은 채크하고 답 받아오기 위한 부분
# while(value<=2):
#     driver.execute_script("DoTakeExam("+itsnumber+","+str(value)+")")
#     time.sleep(random.randint(1,3))
#     driver.implicitly_wait(2)
#     #solve(driver)
#     value += 1
#     sqlflag = [0,0,0,0,0]


# def checkProbNum(tmpval, probNum):
#     answer = -1
#     for row in rows:
#         #row[0] : id, row[1] : answer, row[2]: author, row[3]: date, row[4]: description, row[5]: probnum
#         if(probNum==row[5]):
#             answer = row[1]
#     if(answer == -1):
#             answer = random.randrange(1,6)
#             sqlflag[tmpval] = 1
#     return answer


# def checking(driver, probIndex, answerNum):
#     probIndex += 1
#     js_script = "ClickAnswer(\""+str(probIndex)+"\",\""+str(answerNum)+"\")"
#     driver.execute_script(js_script)
#     time.sleep(random.randint(1,3))

# def getAnswerToDB(driver,probNum):
#     for i in range(5):
#         j = 0
#         for j in range(5):
#             if(sqlflag[i]==0):
#                 break
#             select = driver.find_element_by_xpath("//*[@id=\"frmBenedu\"]/div[3]/section[2]/div[2]/div[3]/div/div/div[1]/div/div/table/tbody/tr["+str(i+1)+"]/td["+str(j+2)+"]/span")
#             if(select.get_attribute("class")=="badge bg_red"):
#                 answerReal = select.text
#                 sql = "INSERT INTO answerSheet (answer,author,created,category,number) VALUES("+answerReal+",,NOW(),'여기',"+probNum[i]+");"
#                 cursor.execute(sql)


# # def is_exists_by_xpath(driver, xpath):
# #         try:
# #             driver.find_element_by_xpath(xpath)
# #         except NoSuchElementException:
# #             return False
# #         return True

# # def string_to_digits(recognized_string):
# #     return ''.join([DIGITS_DICT.get(word, "") for word in recognized_string.split(" ")])

# # def TTS(audio_source):
# #     recognizer = sr.Recognizer()
# #     with sr.AudioFile(audio_source) as source:
# #         audio = recognizer.record(source)

# #     audio_output = ""

# #     try:
# #         audio_output = recognizer.recognize_google(audio)

# #         if any(character.isalpha() for character in audio_output):
# #             print("숫자가 나왔다.")
# #             audio_output = string_to_digits(recognizer.recognize_houndify(audio, client_id=CLIENT_ID, client_key=CLIENT_KEY))
# #             print("DEBUG: "+audio_output)
# #     except sr.UnknownValueError:
# #         print("모르는 에러")
# #     except sr.RequestError as e:
# #         print("Google Speach Request ERR")


# #     return audio_output

# # def BREAKRECAPTCHA(driver):
# #     # 이녀석이 리캡차 내부 /html/body/div[4]/div[4]/iframe 내부버튼 //*[@id="recaptcha-audio-button"]
# #     rand_delay(5)
# #     iframe = driver.find_element_by_xpath("/html/body/div[4]/div[4]/iframe")
# #     driver.switch_to_frame(iframe)

# #     if(is_exists_by_xpath(driver,"//*[@id=\"recaptcha-audio-button\"]")):
# #         driver.find_element_by_xpath("//*[@id=\"recaptcha-audio-button\"]").click()
# #         rand_delay(5)
# #         download_object = driver.find_element_by_xpath("/html/body/div/div/div[6]/a")
# #         download_link = download_object.get_attribute('href')
# #         rand_delay(5)
# #         request = requests.get(url) #오디오 파일을 리퀘스트한다.
# #         audio_file = io.BytesIO(request.content)

# #         converted_audio = io.BytesIO()
# #         sound = AudioSegment.from_mp3(audio_file)
# #         sound.export(converted_audio, format="wav")
# #         converted_audio.seek(0)

# #         audio_output = TTS(converted_audio)
# #         driver.find_element_by_xpath("//*[@id=\"audio-response\"]").send_keys(audio_output)
# #         rand_delay(5)
# #         driver.find_element_by_xpath("//*[@id=\"recaptcha-verify-button\"]").click()#submit
# #         rand_delay(5)
# #     else:
# #         print("오디오테스트가 아니다.")


# #solve는 아직 문항ID값을 추출해오는거밖에 안했다.
# def solve(driver):
#     html = driver.page_source
#     parpage = str(BeautifulSoup(html, 'html.parser'))

#     print('DEBUG: parsing through String')
#     prob = []
#     pIndex = parpage.find('문항ID : ')+7
#     prob.append(parpage[pIndex:pIndex+5])
#     leftpage = parpage[pIndex+10:]
#     pIndex = leftpage.find('문항ID : ')+7
#     prob.append(leftpage[pIndex:pIndex+5])
#     leftpage = leftpage[pIndex+10:]
#     pIndex = leftpage.find('문항ID : ')+7
#     prob.append(leftpage[pIndex:pIndex+5])
#     leftpage = leftpage[pIndex+10:]
#     pIndex = leftpage.find('문항ID : ')+7
#     prob.append(leftpage[pIndex:pIndex+5])
#     leftpage = leftpage[pIndex+10:]
#     pIndex = leftpage.find('문항ID : ')+7
#     prob.append(leftpage[pIndex:pIndex+5])

#     tmpval = 0
#     probnum = []

#     while(tmpval<5):
#         probnum.append(toInt(prob[tmpval]))
#         answer = checkProbNum(tmpval, probnum[tmpval])
#         checking(driver, tmpval, answer)
#         tmpval+=1

#     # 시작시간 해결이 안되면 이 부분에 딜레이가 있어야 함.
#     # driver.execute_script("grecaptcha = undefined") #캡챠 무시
#     # iframes = driver.find_element_by_xpath("//*[@id=\"recaptcha\"]/div/div/iframe")
#     # driver.switch_to_frame(iframes)

#     # driver.find_element_by_xpath("//*[@id=\"recaptcha-anchor\"]/div[5]").click()
#     #Recaptcha 뚫어야 하는 코드
#     time.sleep(60)

#     driver.find_element_by_xpath("//*[@id=\"btnSubmit\"]").click()
#     driver.switch_to_default_content()
#     getAnswerToDB(driver,probnum)