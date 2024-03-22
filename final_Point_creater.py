#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import random
from random import randint
from selenium.common.exceptions import TimeoutException

url = "https://www.glassdoor.co.in/Reviews/Tata-Consultancy-Services-Reviews-E13461.htm"

final_review1= []
final_review2=[]
comapan_list=[]
def data_ex(url):
    driver= webdriver.Chrome()
    
# Navigate to the URL and wait for the page to load
    driver.get(url)
    wait = WebDriverWait(driver, 40)
    try:
    # wait for the element to appear on the page
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "empReview")))

    except TimeoutException:
    # if the element does not appear within the time limit, reload the page
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "empReview")))
    reviews = []
    star_review=[]
    # Parse the HTML content using BeautifulSoup
     # Extract the review data from the HTML soup
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    tooltip_containers = soup.find_all('div', class_='tooltipContainer')
    review_elements = soup.find_all('li', {'class': 'empReview'})
    for review_element in review_elements:
        review = {}
        if review_element.find('div', {'class': 'tooltipContainer'}):
            # Extract the review's ratin

            # Extract the review's rating
            rating_element = review_element.find('span', {'class': 'ratingNumber'})
            review['rating'] = rating_element.text.strip()

            # Extract the review's title and text
            review_title_element = review_element.find('span', {'class': 'middle common__EiReviewDetailsStyle__newGrey'})
            if review_title_element is not None:
                review['Data/postion'] = review_title_element.text.strip()
            else:
                review['Data/position'] = ""
            review_title_element_place = review_element.find('span', {'class': 'middle'}).find('span')
          
            review_link=review_element.find('a',{'class':'reviewLink'})
            if review_link is not None:
                review['Title']=review_link.text.strip()
            else:
                review['Title']=""
            review_time=review_element.find('span',{'class':'pt-xsm pt-md-0 css-1qxtz39 eg4psks0'})
            if review_time is not None:
                review['Current/Time']=review_time.text.strip()
            else:
                review['Current/Time']=""
            jobline_element = review_element.find('span', {'class': 'common__EiReviewDetailsStyle__newUiJobLine'})
            if jobline_element is not None:
                jobline_spans = jobline_element.find_all('span', {'class': 'middle'})
                jobline_text = [span.text.strip() for span in jobline_spans]
                review['Job Line'] = " - ".join(jobline_text)
            else:
                review['Job Line'] = ""    

            review_text_element = review_element.find('span', {'data-test': 'pros'})
            review['pros'] = review_text_element.text.strip()
            review_text_element2 = review_element.find('span', {'data-test': 'cons'})
            review['cons'] = review_text_element2.text.strip()
            reviews.append(review)
     
        
        
        
        

    
# Extract the content of each div tag
    for tooltip_container in tooltip_containers:
       
       if tooltip_container:
        # Find all the "li" tags
        li_tags = tooltip_container.find_all("li")

        # Loop over each "li" tag and collect the ratings
        star_dict = {"css-1mfncox": 1, "css-1lp3h8x": 2, "css-k58126": 3,
                     "css-94nhxw": 4, "css-11w4osi": 5}
        sub_rating_dict = {}
        
        for li_tag in li_tags:
            div_tags = li_tag.find_all("div")
            for div_tag in div_tags:                
                # Get the classname and the rating name
                if div_tag.has_attr("class"):
                    div_class = div_tag["class"][0]
                else:
                    sub_cat = div_tag.text.strip()
            if div_class in star_dict:
                star_value = star_dict[div_class]
                #print (star_value)
                sub_rating_dict[sub_cat] = star_value
    
        if len(sub_rating_dict)!=0:
            star_review.append(sub_rating_dict)
        
    #print("jbnjs")
   
      
    final_review1.extend(star_review)
    final_review2.extend(reviews)
    df = pd.DataFrame(final_review1)
    df.to_csv('Infosis_2_star1_4.csv', index=False)
    df = pd.DataFrame(final_review2)
    df.to_csv('infosis_2_Reviews1_4.csv', index=False)
    
    driver.quit()
company_list = [ "https://www.glassdoor.co.in/Reviews/Infosys-India-Reviews-EI_IE7927.0,7_IL.8,13_IN115_IP"]
name=1
for h in company_list:

    for page_number in range(1676,5000):
        # Update the URL to point to the next page
        url=str(h)+str(page_number)+str('.htm?sort.sortType=RD&sort.ascending=false&filter.iso3Language=eng&filter.employmentStatus=REGULAR&filter.employmentStatus=PART_TIME')
        
        print(page_number)
        
        
        
        if page_number%8==0:
            sleep_time = randint(5,10)
            time.sleep(sleep_time)
            
    # Call the scrape_page function with the updated URL
      
        data = data_ex(url)
        
        


# In[ ]:




