# -*- coding: utf-8 -*-
"""
Created on Wed May 19 19:44:09 2021

@author: vahidu.z
"""


"""This script is to extract data from USGS's database for HighWaterMark (HWM"""

#Import required libraries
import selenium
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome('C:/Users/Desktop/ChromeDriver/chromedriver')
driver.get('https://stn.wim.usgs.gov/fev/')
driver.maximize_window()

######activate the search box:
driver.find_element_by_xpath('//ul').click()

#find the number of events stored in the database in the dropdown list:
events_no = len(driver.find_elements_by_xpath('//div[4]/div/div/div[2]/div/select/option'))


driver.find_element_by_xpath('/html/body/span/span/span/ul/li['+str(1)+']').click()  #select the i-th event from the dropdown list
driver.find_element_by_xpath('//button[@id="btnSubmitEvent"]').click()               #submit the event for search 
time.sleep(5)

driver.find_element_by_xpath('//a[@href="#downloadPanel"]').click()                  #activate the get data button
time.sleep(6)

driver.find_element_by_xpath('//span[@value="HWM"]').click()
driver.find_element_by_xpath('//a[@id="hwmDownloadButtonCSV"]').click()



#####for new search, slightly different form pops up:
#

for i in range(2, 5):
    time.sleep(5)
    driver.find_element_by_xpath('//button[@id="btnChangeFilters"]').click()
    time.sleep(3)
    Remove_choice = driver.find_elements_by_xpath('//span[@class="select2-selection__choice__remove"]') # clear the form for new search
    Remove_choice[1].click()
    
    driver.find_element_by_xpath('/html/body/span/span/span/ul/li['+str(i)+']').click()  #select the i-th event from the dropdown list
    driver.find_element_by_xpath('//button[@id="btnSubmitFilters"]').click()               #submit the new event for search 
    #WebDriverWait(driver, 15).until
    time.sleep(10)
    
    
    driver.find_element_by_xpath('//span[@value="HWM"]').click()
    driver.find_element_by_xpath('//a[@id="hwmDownloadButtonCSV"]').click()
    


