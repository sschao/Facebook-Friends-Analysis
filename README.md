# Facebook-Friends-Analysis
Tool to analyze Facebook Friends. Using this tool could result in Facebook banning you, so use at your own discretion. Developer not liable for Facebook ban.

## Setup

Download the appropriate *.py* files. Download the Chrome driver that is the corresponding version as your Chrome browser. Link: https://chromedriver.chromium.org/

## mutual_friends_analysis.py
Finds the number of mutual friends that you have with each of your Facebook friends, exports it to a csv file along with the percentile, and also creates a graph plotting the number of mutual friends vs percentile and a histogram for frequency vs the number of mutual friends

### Required Packages
Open Command Prompt and run the following command to install all of the required packages for **mutual_friends_analysis.py**.
```
pip install selenium bs4 pandas scipy numpy datetime
```
### Changes to Make
Change to the appropriate directory path for your Chrome driver (include the chromedriver.exe) in the specified place (noted in the code). For example, 
```
driver = webdriver.Chrome("C:\\Users\\sschao\\Desktop\\Scripts\\Facebook\\chromedriver.exe") 
```
You can also put the chrome driver in the same folder/directory as your **mutual_friends_analysis.py** file. 

Also, change to the correct path for your output csv. For example, 
```
df_friends_decr.to_csv("C:\\Users\\sschao\\Desktop\\Scripts\\Programming\\Facebook\\Facebook Friends, Mutual Friends, Link.csv", index = False)
```
