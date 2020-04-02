'''
IMPORTS
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import re
import os
from time import sleep





'''
initializes selenium(the automated browser)
uncomment when using getKbDump(), or genKbHtmls()
'''
driver = webdriver.Chrome()


'''
takes content in str format,
the regular expression to find,
and regular expression to replace within the the results of the found pattern
''' 
def parser(file, expression, remove):
    l = re.findall(expression, file)
    return [re.sub(remove ,'',i) for i in l]

'''
opens salesforce kb with automated browser
pauses until you get past the okta auth, user logs in
after pressing enter on the cmd window, obtains html content that
contains KB numbers and writes to a file (DumpFile.txt)
which is used in the next function
'''
def getKbDump():
    DumpFile = open('DumpFile.txt','w+',encoding = 'UTF-8')
    driver.get('https://globalvf.my.salesforce.com/knowledge/publishing/knowledgePublishingHome.apexp')
    os.system('pause')
    arrow = '/html/body/div[1]/div[3]/table/tbody/tr/td/div[1]/form/table/tbody/tr/td[2]/span/div/div[3]/div[2]/table/tbody/tr/td[1]/span/span[1]/img'
    pageSize = '/html/body/div[1]/div[3]/table/tbody/tr/td/div[1]/form/table/tbody/tr/td[2]/span/div/div[3]/div[2]/table/tbody/tr/td[1]/span/span[1]/table/tbody/tr[5]/td[2]'
    nextPage = '//*[@id="articleList_nextPage"]'
    
    listSize_button = driver.find_elements_by_xpath(arrow)[0]
    pageSize_button = driver.find_elements_by_xpath(pageSize)[0]
    nextPage_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, nextPage)))
    listSize_button.click()
    pageSize_button.click()
    nextPage_button.click()
    DumpFile.write(driver.page_source)
    while 0==0:
        nextPage_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, nextPage)))
        os.system('pause')
        nextPage_button.click()
        DumpFile.write(driver.page_source)

'''
Takes DumpFile.txt and parses all the art numbers
and attatches it to URL base
returns the list of article urls
'''
def getKbUrls():
    f = open('DumpFile.txt', 'r', encoding='UTF-8')
    result = open('result.txt', 'w', encoding='UTF-8')
    requestContent = f.readlines()
    l = parser(str(requestContent),'[a-zA-Z0-9]{15}','')
    c = [i for i in l if i[0:2] == 'ka' or i[0:2] == 'Ka' or i[0:2] == 'kA' or i[0:2] == 'KA']
    p = ['https://globalvf.my.salesforce.com/knowledge/publishing/articleOnlineDetail.apexp?id=' + i for i  in c]
    mylist = list(dict.fromkeys(p))
    print(len(mylist))
    result.write(str(mylist))
    return mylist

'''
opens salesforce kb with automated browser
pauses until you get past the okta auth, user logs in
after pressing enter on the cmd window, continues to go through each url
in the list returned by above function, opens the page, saves it, and goes to the next
'''
def genKbHtmls():
    driver.get('https://globalvf.my.salesforce.com/knowledge/publishing/knowledgePublishingHome.apexp')
    os.system('pause')
    counter = 0
    mylist = getKbUrls()
    for i in mylist:
        print(i)
        driver.get(i)
        titleText = parser(driver.page_source, 'articleNumber" class="TEXT">[0-9]{9}', 'articleNumber" class="TEXT">')
        print(titleText)
        print(str(counter) + '/' + str(len(mylist)))
        try:
            f = open('SFKBs10_11_19\\' + titleText[0] + '.html', 'w', encoding = 'UTF-8')
            f.write(driver.page_source)
            f.close()
            
        except:
            pass
        counter += 1

'''
returns list of the kb dir's
'''
def titleKbs():
    fileList = os.listdir('SFKBs10_11_19 - Copy\\')
    KbDirs = ['SFKBs10_11_19 - Copy\\' + i for i in fileList]
    #print(KbDirs)
    return KbDirs

'''
cleans up the local html files(still working on this/WIP)
'''
#(<span id="articleDetail:j_id425">(.*?\n*? *?)*?    <\/script><\/span>)
#<span id="articleDetail:j_id425">(.*?\n*? *?)*?    </div></span>

def removeTags():
    rex = '(<!-- Start page content table -->(.*?\n*? *?)*?<!-- Body events -->)'
    Kbs = titleKbs()
    for i in Kbs:
        print('processing: ' + i) 
        file1 = open(i,'r', encoding='utf-8')
        file1Cont = file1.read()
        
        regex = re.findall(rex,file1Cont)
        file1.close()
        file2 = open(i, 'w', encoding='utf-8')
        file2.write(''.join(regex[0]))
        file2.close()
    





