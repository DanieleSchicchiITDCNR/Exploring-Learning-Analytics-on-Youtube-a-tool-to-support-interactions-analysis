import isodate
import json
import googleapiclient.discovery    
import csv
import time
import mysql.connector
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.ui import WebDriverWait
from mysql.connector import Error
from selenium.common import exceptions


def create_connection(host_name, user_name, user_password,db):

    connection = None

    try:

        connection = mysql.connector.connect(

            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db,
            buffered=True

        )

        print("Connection to MySQL DB successful")

    except Error as e:

        print(f"The error '{e}' occurred")


    return connection

def isInDb(video_id,cursor):
    cursor.execute("select * from video where id = %s",[video_id])
    if(cursor.rowcount>0):
        return 1
    else:
        return 0


def getSuggestedTimes(video_id,cursor):
    cursor.execute("select suggested_times from video where id=%s",[video_id])
    return cursor.fetchone()[0]


def getDuration(id):
    if "&" in id:
        id=id[0:id.index("&")]
    api_key="AIzaSyCWH5-fbx-6X4GHB3fc291PdVOBCyYOQGQ"

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)
    
    request = youtube.videos().list(
        part="contentDetails",
        id=id
    )
    response=request.execute()
    time.sleep(3)
    dur=isodate.parse_duration(response['items'][0]["contentDetails"]["duration"])
    print("il video con id="+id+" durera'"+str(dur.total_seconds())+"s")
    return int(dur.total_seconds())
 
def login(driver,email,password):
    wait = WebDriverWait(driver, 10)
    elem =wait.until(cond.element_to_be_clickable((By.ID,"action-button")))
    elem.find_element_by_class_name("yt-simple-endpoint").click()
    elem=driver.find_element_by_id("identifierId")
    elem.send_keys(email)
    driver.find_element_by_id("identifierNext").find_element_by_tag_name("button").click()
    
    wait.until(cond.element_to_be_clickable((By.ID,"password"))).find_element_by_tag_name("input").send_keys(password)
    driver.find_element_by_id("passwordNext").find_element_by_tag_name("button").click()

#Recupera gli id dei video presenti nella lista a parametro, li stampa nel csv e ritorna il primo video suggerito
def getHomeVideosId(driver,file,idSetup): 
    videos=driver.find_element_by_id("contents").find_elements_by_id("content")
    next_video=""
    writer=csv.writer(file)
    i=0
    for element in videos:
        try:    

            url=element.find_element_by_id("thumbnail").get_attribute("href") 
            print(url)
            if(url):
                if next_video=="":
                    next_video=element
                    writer.writerow(["",url[url.index("=")+1:],1,1,time.time(),"", idSetup ])
                else:
                    writer.writerow(["",url[url.index("=")+1:],0,1,time.time(),"", idSetup ])
                i+=1
        except exceptions.NoSuchElementException:
            print("elemento non trovato")
        
        print(i)
        if(i==20):
            break
    return next_video

#Recupera gli id dei video presenti nella lista a parametro, li stampa nel csv e ritorna il primo video suggerito
def getQueryResult(driver,file,idSetup): 
    wait=WebDriverWait(driver,15)
    contents=wait.until(cond.presence_of_element_located((By.ID,"contents")))
    videos=contents.find_elements_by_id("dismissable")
    next_video=""
    writer=csv.writer(file)
    i=0
    print(videos)
    for element in videos:
        print(element)
        try:    
            
            url=element.find_element_by_id("thumbnail").get_attribute("href") 
           
            if(url):
                if next_video=="":
                    next_video=element
                    writer.writerow(["",url[url.index("=")+1:],1,1,time.time(),"", idSetup ])
                else:
                    writer.writerow(["",url[url.index("=")+1:],0,1,time.time(),"", idSetup ])
                i+=1
        except exceptions.NoSuchElementException:
            print("elemento non trovato")
        except exceptions.StaleElementReferenceException:
            pass
        print(i)
        if(i==20):
            break
    print(next_video)
    return next_video


#-----getNextVideo scrive sul csv la lista di tutti i video che vengono consigliati durante la visualizzazione di un video e 
#     restituisce l'id del video che verrà automaticamente riprodotto una volta finito il video che si sta visualizzando-----
def getNextVideo(driver,file,watched,tempoOsservazione,idSetup):
    
    next_=driver.find_element_by_id("related").find_element_by_id("items").find_element_by_id("contents")
    next_video=next_.find_element_by_id("thumbnail").get_attribute("href")
    related_videos=driver.find_element_by_id("related").find_element_by_id("items").find_elements_by_id("dismissable")
    print(next_video)

    writer=csv.writer(file)
    writer.writerow([watched,next_video[next_video.index("=")+1:],1,0,time.time(),tempoOsservazione,idSetup ])
    print(len(related_videos))
    for v in related_videos[1:]:
        relatedVideoId=v.find_element_by_id("thumbnail").get_attribute("href")[v.find_element_by_id("thumbnail").get_attribute("href").index("=")+1:]
        if("&" in relatedVideoId):
            relatedVideoId=relatedVideoId[0:relatedVideoId.index("&")]
        writer.writerow([watched,relatedVideoId,0,0,time.time(),tempoOsservazione,idSetup ])
        
        print(relatedVideoId)
    
    return next_

#-----getNextVideo scrive sul csv la lista di tutti i video che vengono consigliati durante la visualizzazione di un video e 
#     restituisce l'intera lista dei video suggeriti-----
def getRelatedVideos(driver,file,watched,tempoOsservazione,idSetup):
    
    
    next_=driver.find_element_by_id("related").find_element_by_id("items").find_element_by_id("contents")
    next_video=next_.find_element_by_id("thumbnail").get_attribute("href")
    related_videos=driver.find_element_by_id("related").find_element_by_id("items").find_elements_by_id("dismissable")

    writer=csv.writer(file)
    writer.writerow([watched,next_video[next_video.index("=")+1:],1,0,time.time(),tempoOsservazione,idSetup ])
    print(len(related_videos))
    for v in related_videos[1:]:
        relatedVideoId=v.find_element_by_id("thumbnail").get_attribute("href")[v.find_element_by_id("thumbnail").get_attribute("href").index("=")+1:]
        if("&" in relatedVideoId):
            relatedVideoId=relatedVideoId[0:relatedVideoId.index("&")]
        writer.writerow([watched,relatedVideoId,0,0,time.time(),tempoOsservazione,idSetup ])
        
        print(relatedVideoId)
    
    
    return related_videos

#----la funzione config setta i parametri di esplorazione in base ad un file di configurazione fornito in input----
def search(driver,query,enter):
    driver.find_element_by_id("search-input").find_element_by_tag_name("input").send_keys(query+enter)
    time.sleep(10)

def getDataFromDb(query):
    
    dict_to_hist={}
    connection=create_connection("localhost","root","","tesi")
    cursor=connection.cursor()
    cursor.execute(query)
        
    for result in cursor.fetchall():
        
        dict_to_hist[result[0]]=int(result[1])
    
    return dict_to_hist

#-----Ritorna tutte le sessioni ongoing che devono essere rieseguite----------
def checkForOngoing(connection,cursor):
    ongoing_query="select * from setupsessione where status='ongoing' and "+str(time.time())+"-lastExecution>frequency "
    cursor.execute(ongoing_query)

    #---Creo un dizionario che ha come chiavi i nomi delle colonne del db e come valori i dati presenti all'interno della tabella----
    desc = cursor.description
    column_names = [col[0] for col in desc]
    setup_list = [dict(zip(column_names, row))  for row in cursor.fetchall()]
   
    return setup_list

def checkForReady(connection,cursor):
    query="select id,account,tipo,query,steps,viewTime,iterations,executedTimes from setupsessione where status='ready'"
    cursor.execute(query)

    #---Creo un dizionario che ha come chiavi i nomi delle colonne del db e come valori i dati presenti all'interno della tabella----
    desc = cursor.description
    column_names = [col[0] for col in desc]
    setup_list = [dict(zip(column_names, row))  for row in cursor.fetchall()]
    
    
    return setup_list
    
def aggiorna_setupsessione(setup,connection,cursor):
    query_setup="update setupsessione set executedTimes=%s, status=%s, lastExecution=%s where id=%s"
    timestamp=str(time.time())
    timestamp=timestamp[0:timestamp.index(".")]
    if(setup['iterations']-setup['executedTimes']<=1):  
        
        cursor.execute(query_setup,[setup['executedTimes']+1,"completed",timestamp,setup['id']])
    else:
        cursor.execute(query_setup,[setup['executedTimes']+1,"In progress",timestamp,setup['id']])
    
    connection.commit()
    return timestamp

def setSessionEndTime(setupId,startedAtTimestamp):
   query="INSERT INTO sessione(setupId,startedAt,finishedAt) VALUES(%s,%s,%s)"
   connection=create_connection("localhost","root","","Tesi")
   cursor=connection.cursor()
   cursor.execute(query,[setupId,startedAtTimestamp,time.time()])
   cursor.execute("update setupsessione set status=%s where status !=%s  and id=%s",["ongoing","completed",setupId])
   connection.commit()
