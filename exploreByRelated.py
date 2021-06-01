from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.ui import WebDriverWait
import lib
import csv
import time
import sys
from json import loads


password="t3stings3lenium"

base_url="https://www.youtube.com/watch?v="
driver = webdriver.Firefox()
#------- carico estensione per bloccare le pubblicità-------#
driver.install_addon("extensions\\uBlock0@raymondhill.net.xpi", temporary=True)
driver.get("http://www.youtube.com")
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 10); 
#setup=sys.argv[1]
setup=loads(sys.argv[1])
assert "YouTube" in driver.title

#-----Accesso account-------
lib.login(driver,setup['account'],password)
#-----/Accesso account------
print(setup['account'],setup['id'])


with open("results/"+setup['account']+"/by_related_exploration.csv","a+",newline='') as session:
    #-----Ricerca dei video in home page e visualizzazione del primo consigliato-----
    toWatch=lib.getHomeVideosId(driver,session,setup['id'])
    if(setup['query']):
        lib.search(driver,setup['query'],Keys.ENTER)
        
        lib.getQueryResult(driver,session,setup['id']).click()
    else:
        toWatch.click()
    currentVideoId=driver.current_url[driver.current_url.index("=")+1:]
    time.sleep(5)
    related_videos=lib.getRelatedVideos(driver,session,currentVideoId,setup['viewTime'],setup['id'])
    print(related_videos)
    i=0
    while setup['steps']>0:
        
        '''try: 
            
            element = wait.until(cond.element_to_be_clickable(driver.find_element_by_xpath("//button[@class='ytp-ad-skip-button ytp-button']")))
            element.click();  
            
            print("Pubblicita' skippata")
        except exceptions.NoSuchElementException:
            print("Il video non contiene pubblicita'")'''

        currentVideoId=driver.current_url[driver.current_url.index("=")+1:]
        length=lib.getDuration(currentVideoId)
        #---se le api di yt restituiscono length=0 vuol dire che si sta osservando una live, per evitare errori setto length=31, trattandola come un normale video
        if length==0: 
            length=31
        if length>setup['viewTime']:
            time.sleep(setup['viewTime'])
        else:
            time.sleep(length-length/4)
        setup['steps']-=1
        if i>=1:
            driver.back()
        #wait.until(cond.element_to_be_clickable(related_videos[i].find_element_by_id("thumbnail")))
        time.sleep(5)
        related_videos[i].click()
        i+=1
assert "No results found." not in driver.page_source
time.sleep(5)
driver.close()

#------Una volta terminati i passi avvio la procedura per inserire i dati relativi ai video e alla sessione nel database------- 
lib.setSessionEndTime(setup['id'],setup["startedAtTime"])
print("Id sessione:"+str(setup['id']))
exec(open("fillUpDb.py").read(),{"account":setup['account'],"tipo":2,"idSetup":setup['id']})

