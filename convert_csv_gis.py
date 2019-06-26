import urllib2, os, zipfile, re, timeit, logging, getpass, datetime, arcpy
#from bs4 import BeautifulSoup
from selenium import webdriver
#import csv, zipfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

start = timeit.default_timer()

username = getpass.getuser()
initials = getpass.getuser()[:2].upper()

chrome_options = Options()
chrome_options.add_argument("--headless")
output_dir = r'C:\GIS-Long\REQUESTS\PWT\WasteIndustries_MapApplication_pickup_days\test_output'
#recollect_url = r"https://manage.recollect.net/admin/area/Apex/waste/metrics/calendar"
recollect_url =r'https://manage.recollect.net/admin/area/Apex/waste/connector/default/list/0'
driver = webdriver.Chrome("C:\Users\Jlong\Downloads\chromedriver_win32\chromedriver.exe",chrome_options=chrome_options)
driver.get(recollect_url)

csv_link ="https://recollect-connector-prod.s3.amazonaws.com/apex/raw/parcels-111296.csv.gz?AWSAccessKeyId" \
  "=AKIAIZCUAD573SWBYSLA&amp;Expires=1561146105&amp;Signature=x8%2FmmZ2Yuueg7VF62YOKyqhMCbE%3D"
#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
 #    "//button[@class='navbar-toggle menu-toggler pull-left'][type='button']//span[@class='sr-only']"))).click()

#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
 #                                                               "//a[@class='dropdown-toggle']//span["
  #                                                              "@class='menu-text'][contains(.,"
   #                                                             "'Addresses')]"))).click()

try:
    html = driver.page_source
    print html
    driver.find_element_by_xpath("//a[@href='{}'][@class='btn btn-white btn-xs']".format(csv_link)).click()
     #                           "@class='menu-text'][contains(.,'STFP Address Connector')]").click()

    #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
     #                                                           "//a[@class='dropdown-toggle']["
      #                                                          "@data-sidebar='address-dropdown']"))).click()

    #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
     #                                                           "//a[@data-sidebar='address-dropdown']//span["
      #                                                          "@class='menu-text'][contains(.,"
       #                                                        "'Addresses')]"))).click()





    print "Success"

except EC as e:
    print "Couldnt process", e