# Submitted by K Shahsank
# Email: kshashank2301@gmail.com
#
#  Youtube data scrapping using Selenium and Geckowebdriver
# 


# import libraries
from selenium import webdriver
import time
import pandas as pd
import pickle

#Loading random yt-links aquired using Youtube API
with open('links.pkl','rb') as f:
    links = pickle.load(f)


# Running firefox webdriver from the executable path
driver = webdriver.Firefox(executable_path = 'D:\Desktop\gecko\geckodriver.exe')

#Creating DataFrame for storing the data
df = pd.DataFrame(columns=['Video_Link','Video_Views','Upload_date','Comments','Likes','Dislikes'])

#Function to scrape the data using webdriver
def scrape_yt(urlpage):
    
    driver.get(urlpage) # Geting web page
    
    time.sleep(3) # sleep for 3s
    
    driver.execute_script("window.scrollBy(0,500)", "") # Execute script to scroll to comments section
    
    time.sleep(5) # sleep for 5s
    
    # driver.quit()

    views = driver.find_elements_by_tag_name('yt-view-count-renderer')[0].text
    comments = driver.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string')[0].text
    ud = driver.find_elements_by_css_selector('div#date > yt-formatted-string')[0].text
    likes = driver.find_elements_by_css_selector('div#top-level-buttons > ytd-toggle-button-renderer')[0].text
    dislikes = driver.find_elements_by_css_selector('div#top-level-buttons > ytd-toggle-button-renderer')[1].text

        
    return views,comments,ud,likes,dislikes


# Looping over the Links
 for url in links:
    views,comments,ud,likes,dislikes = scrape_yt(url)
    df = df.append({'Video_Link':url,'Video_Views':views.strip(' views'),'Upload_date':ud,'Comments':comments.strip(' Comments'),'Likes':likes,'Dislikes':dislikes},ignore_index=True)

# Saving as a CSV File
df.to_csv('../Data/yt_scrap.csv',index=False)


# OUTPUT CONSISTS OF FOLLOWING VARIABLES
# -----------------------------------------------------------------------------------
# Video_Link : Link to the random yt Video
# Video_Views : Views of the video, either a number or "NO" if there are no views
# Upload_date: Upload date, it can be in date format or can be a live streamed/premeried at some time
# comments: Number of comments on a Video
# Likes : Either a number (numerical or like 5K,5M etc) or 'LIKE' if user disabled likes
# Dislikes : Either a number (numerical or like 5K,5M etc) or 'DISLIKE' if user disabled likes
