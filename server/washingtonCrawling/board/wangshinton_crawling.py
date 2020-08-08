### import 

from selenium import webdriver  ## chrome 브라우저 불러오기
from time import sleep
from bs4 import BeautifulSoup    ##핵심 element를 가지고 오기 

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import pickle


#conora 19로 검색하기 
search_term = "conora 19"
url="https://www.washingtontimes.com/search/?cx=015385541671335030271%3Anfb7f1nj88q&cof=FORID%3A11&ie=UTF-8&q={}&sa=GO".format(search_term)

browser = webdriver.Chrome("../webdriver/chromedriver")

browser.get(url)
sleep(2)


### element를 가지오 오기 
soup = BeautifulSoup(browser.page_source,"html.parser")
print(soup.prettify())

conora19_content=[]
conora19_title=[] 

cur_page_num = 1 
crawl_num = 5

sleep(2)


content_body = ""

try : 
    conora_body = soup.select('div.bigtext > p')  
    sleep(0.5)

    for i in range(len(conora_body)) : 
        content_body = content_body + str("\n") + conora_body[i].text.strip()
#             print("body {}:{}".format(i,conora_body[i].text))

    conora19_content.append(content_body)

except: 
    print("기사 가져오기 발생")


browser.get(url)
sleep(2)

try: 
    WebDriverWait(browser, 6) \
        .until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(@aria-label,"Page {}")]'.format(cur_page_num)))).click()

    sleep(3)


except :
    print ("Loading Eorror")
    


####  Page 하나씩 10개정도 Contents를 보는 것임 ##########
while cur_page_num <= crawl_num : 
    
    soup = BeautifulSoup(browser.page_source,"html.parser")
    sleep(2)
    conora19_href=[]
    
    print("cur_page_num:",cur_page_num)
    cur_page_num = cur_page_num + 1 
  


    ####  Title 저장하는 부분  (List Save) ##########
    #################################################
    
    pro_list = soup.select('div.gs-title > a')
    print(len(pro_list))

    try : 
        for v in pro_list:

            print("conora 19 Title:{}".format(v.text.strip()))
            print(v.attrs['href'])
                      
            conora19_title.append(v.text.strip())
            conora19_href.append(v.attrs['href'])

            print()

        print()

    except :
        print("title 발생")
         


    print("cur_page:{},crawl_all_page:{}".format(cur_page_num,crawl_num))


    ## 기사 내부 들어가기 (기사 내용 가지고 오기)

    for num in range(0,10) :

        browser.get(conora19_href[num])
        soup = BeautifulSoup(browser.page_source,"html.parser")
        sleep(6)

        try : 
#             browser.execute_script('window.scrollBy(0,-3000)')
            browser.execute_script("scroll(0, 2000);")
            sleep(2)

#             (browser.find_element_by_class_name('expand')).click()
            
            WebDriverWait(browser, 6) \
                .until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'p.expand'))).click()
            
        
        except: 
            print("확장 버튼 에러")


        soup = BeautifulSoup(browser.page_source,"html.parser")
        sleep(2)


        ####  Contents 저장하는 부분  (List Save) ##########
        #################################################
        
        content_body = ""

        try : 
            conora_body = soup.select('div.bigtext > p')  
            sleep(1)

            for i in range(len(conora_body)) : 
                content_body = content_body + str("\n") + conora_body[i].text.strip()
    #             print("body {}:{}".format(i,conora_body[i].text))

                conora19_content.append(content_body)

        except: 
            print("기사 가져오기 발생")

    

    
    browser.get(url)
    sleep(4)
 
    try: 
        WebDriverWait(browser, 6) \
            .until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(@aria-label,"Page {}")]'.format(cur_page_num)))).click()

        sleep(3)
        
    except :
        
        print ("Loading Eorror")
        

####### washington_times_title01.pk  저장하기  
####### washington_times_contents01.pk  저장하기  
#########################################################

with open("data/washington_times_title101.pk", "wb") as f:
    pickle.dump(conora19_title, f)

with open("data/washington_times_contents01.pk","wb") as f:
    pickle.dump(conora19_content, f)
    



