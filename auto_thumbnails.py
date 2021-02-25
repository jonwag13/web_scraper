from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import urllib.request
import pandas as pd
from PIL import Image


'''
function: Make a list of hyperlink attributes given a list of selenium elements
args: elements<list>
returns: url_list<list>
'''
def make_url_list(elements):
    url_list = []
    
    for href in elements:
        url_list.append(str(href.get_attribute('href')))
   
    return url_list


#Make a pandas dataframe to store data in a csv format
df = pd.DataFrame(columns=['url_1','url_2','title','img_url','video_url','video_id'])   


#Initiate a chrome driver
driver = webdriver.Chrome("/usr/local/bin/chromedriver")


#Set number of seconds to wait between page requests
n = 3


#Starting page address
url_0 = "https://acls.com/free-resources/videos"


#Find all the wanted links on the starting page
driver.get(url_0)
driver.implicitly_wait(n)
elements = driver.find_elements(By.XPATH,'/html/body/section[2]/div/a')
url_1_list = make_url_list(elements)


#Navigate to each link and find all wanted links on current page
for url_1 in url_1_list:
    #Second Page
    driver.get(url_1)
    driver.implicitly_wait(n)
    elements = driver.find_elements(By.XPATH,'/html/body/section[2]/div/div[*]/div[2]/a')
    url_2_list = make_url_list(elements)
    

    #Navigate to each link and locate the desired data
    for url_2 in url_2_list:
        #Third Page
        driver.get(url_2)
        driver.implicitly_wait(n)
        title_element = driver.find_element(By.XPATH,'/html/body/div[1]/section/h1')
        title = title_element.text
        video_element = driver.find_element(By.XPATH,'// iframe')
        video_url = video_element.get_attribute('src') 
        video_id = video_url.split('/')[4]
        video_id = video_id.split('?')[0]
        img_url = "http://img.youtube.com/vi/"+video_id+"/maxresdefault.jpg"
        

        #Append desired data to the dataframe
        data_dict = {'url_1':url_1,
                     'url_2':url_2,
                     'title':title,
                     'img_url':img_url,
                     'video_url':video_url,
                     'video_id':video_id}
        df = df.append(data_dict, ignore_index=True)
        print(url_2)
        

        #Download the youtube thumbnail as .jpeg
        urllib.request.urlretrieve(img_url, video_id + '.jpeg')
             

#Close Driver
driver.close()


#Save .csv file
df.to_csv('thumbnail_links.csv')


#Resize the .jpeg images to a given basewidth, while maintaining aspect ratio
for i in df.video_id:
    jpeg = i + '.jpeg'
    img = Image.open(jpeg) # image extension *.png,*.jpg
    basewidth = 150
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS) 
    img.save('150w_' + jpeg) 



 
