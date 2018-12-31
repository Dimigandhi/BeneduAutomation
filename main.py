# 밑에 value <= [문제지 개수임 ㅋㅋ]

########################## 이 부분은 채크하고 답 받아오기 위한 부분
# while(value<=2):
#     driver.execute_script("DoTakeExam("+itsnumber+","+str(value)+")")
#     time.sleep(random.randint(1,3))
#     driver.implicitly_wait(2)
#     #solve(driver)
#     value += 1
#     sqlflag = [0,0,0,0,0]

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

import crawl as crawl
import use as use

crawl.crawlMain()
#use.useMain()


