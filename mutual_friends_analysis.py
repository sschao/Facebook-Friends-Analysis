import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

friends_html = 'C:\\Users\\shawn\\Desktop\\Programming\\Facebook\\db\\index.html'
usr=input('Enter Email Id:') #enter email
pwd=input('Enter Password:') #enter password

driver = webdriver.Chrome("C:\\Users\\shawn\\Desktop\\Programming\\Facebook\\chromedriver.exe") #change this path to appropriate chrome driver directory
driver.get("http://facebook.com")

username_box = driver.find_element_by_id('email')
username_box.send_keys(usr)

password_box = driver.find_element_by_id('pass')
password_box.send_keys(pwd)

login_box = driver.find_element_by_id('loginbutton')
login_box.click()

actions = ActionChains(driver)
actions.move_to_element_with_offset(driver.find_element_by_tag_name('body'), 0,0)
actions.move_by_offset(100, 200).click().perform()

def download_friends():
    driver.get("https://m.facebook.com/me/friends")
    time.sleep(5)
    print('Scrolling to bottom...')
    #Scroll to bottom
    while driver.find_elements_by_css_selector('#m_more_friends'):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

download_friends()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

mutual_friends = soup.findAll("div", { "class" : "notice ellipsis" })
friend_names = soup.findAll("div", { "class" : "_84l2" })
mutual_friend_dict = {}
url_dict = {}

#didnt use function here because wanted to return two separate dictionaries
for i in range(len(mutual_friends)):
    try:
        num_mutual_friends = int(mutual_friends[i].text[:-15])
    except ValueError:
        try:
            num_mutual_friends = int(mutual_friends[i].text[:-14]) #singular when I only have "1 mutual friend"
        except ValueError:
            continue
    friend_name =  friend_names[i].find("a").text
    if friend_name in mutual_friend_dict.keys():
        dup_count = 0
        while friend_name in mutual_friend_dict.keys():
            dup_count+=1
            if dup_count == 1: #first iteration so friend name does not have any extra stuff added onto it
                friend_name = f"{friend_name}_{str(dup_count)}"
            else:
                friend_name = f"{friend_name[:-len(str(dup_count-1))-1]}_{str(dup_count)}" #concise way to label duplicates

    mutual_friend_dict[friend_name] = num_mutual_friends
    try:
        friend_url = "http://facebook.com" +friend_names[i].find("a")["href"]
        url_dict[friend_name] = friend_url
    except KeyError: #these people dont have FB Urls and may have deleted their Facebooks
        print(friend_name)

top_mutual_friends = sorted(mutual_friend_dict, key=mutual_friend_dict.get, reverse = True)

df_friends = pd.DataFrame(list(mutual_friend_dict.items()), columns=['Friend Name', 'Number of Mutual Friends'])
df_friends_decr = df_friends.sort_values(by =["Number of Mutual Friends"], ascending = False).reset_index(drop=True)
df_friends_decr["Ranking"] = df_friends_decr.index+1

df_friends_decr["Percentile"],df_friends_decr["Facebook Link"] = [None,None]
for index, row in df_friends_decr.iterrows(): #create percentile column
    df_friends_decr.at[index,'Percentile'] = stats.percentileofscore(df_friends_decr["Number of Mutual Friends"],df_friends_decr["Number of Mutual Friends"][index])
    try:
        df_friends_decr.at[index,'Facebook Link'] = url_dict[df_friends_decr["Friend Name"][index]]
    except KeyError: #people who deleted their FB
        pass

df_friends_decr.to_csv("(Input your own file directory)", index = False) #change this
plt.figure()
plt.plot(df_friends_decr["Percentile"], df_friends_decr["Number of Mutual Friends"])
plt.title("Number of Facebook Friends vs Percentile")
plt.xlabel("Percentile")
plt.ylabel("Number of Facebook Friends")

def find_friend_info(df, friend_name): #if multiple people with the same name returns both
    df_friend= df[df["Friend Name"].str.contains(friend_name)] 
    return df_friend


