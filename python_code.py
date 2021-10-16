from selenium import webdriver
from ordered_set import OrderedSet
import time
import os
import csv

os.system("cls")
username = input("Enter Username: ")

f=open("testing2.csv","w")
csv_writer= csv.writer(f)
csv_writer.writerow(['Username','Date','Time',"Tweet content",'Likes','Retweet','Comments'])

driver = webdriver.Chrome('D:/virtualenvs_muthu/selenium_twitter/chromedriver_win32/chromedriver.exe') 
driver.get("https://twitter.com/%s"%username)
time.sleep(5)
os.system("cls")

scroll_list=OrderedSet()
scroll_list_time=OrderedSet()

for x in range(1,7):
    print("Scroll",x,)
    
    time.sleep(1)
    mutiple_tweets=driver.find_elements_by_css_selector('div[style^="position: absolute; width: 100%;"]')
    mutiple_tweets_time=driver.find_elements_by_tag_name('time')
    for elem,t in zip(mutiple_tweets,mutiple_tweets_time):
        scroll_list.add(elem.text)
        scroll_list_time.add(t.get_attribute("datetime"))


    h=driver.execute_script("return document.documentElement.clientHeight;")
    driver.execute_script(f"window.scrollTo(0, {x*h});")
    time.sleep(3.5)



temp=list(scroll_list)
temp2=[]
time_list1=list(scroll_list_time)
time_list2=[]
for x,y in zip(list(scroll_list), list(scroll_list_time)):
    if "@" in x or "Retweeted" in x:
        temp2.append(x)
        time_list2.append(y)


    
for x,y in zip(temp2,time_list2):

    print(y)
    print(x)
    xt=x.split("\n")
    if "Retweeted" in xt[0]:
        my_actual_list=[xt[0],xt[4],"retweeted"]+xt[-1:-4:-1]
    elif "Pinned" in xt[0]:
        my_actual_list=[xt[0],xt[4],"Pinned"]+xt[-1:-4:-1]
    else:

        if "Show this thread" in xt[-1]:
            my_actual_list=[xt[0],xt[3],xt[4]] + xt[-2:-5:-1]
        else:
            my_actual_list=[xt[0],xt[3],xt[4]]+xt[-1:-4:-1]
    
    my_actual_list.insert(2,y)
    
    csv_writer.writerow(my_actual_list)
    

print("original length:",len(temp))
print("\nModified list length:",len(temp2))

f.close()
        
