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
recollect_url = r"https://manage.recollect.net/admin"
driver = webdriver.Chrome("C:\Users\Jlong\Downloads\chromedriver_win32\chromedriver.exe",chrome_options=chrome_options)
driver.get(recollect_url)
#pagesource = driver.page_source


try:

    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class='auth0-lock-input'][@name='email']"))).clear()

    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class='auth0-lock-input'][@name='email']"))).send_keys(
        "jeff.long@apexnc.org")

    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class='auth0-lock-input'][@name='password']"))).clear()

    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class='auth0-lock-input'][@name='password']"))).send_keys(
        "K0ston126*")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                "//button[@class='auth0-lock-submit']//span[@class='auth0-label-submit'][contains(.,'Log In')]"))).click()

    uname_txt = driver.find_element_by_xpath( "//input[@class='auth0-lock-input'][@name='email']").get_attribute(
        'value')

    pw_txt = driver.find_element_by_xpath("//input[@class='auth0-lock-input'][@name='password']").get_attribute(
        'value')

    print uname_txt, pw_txt
    html = driver.page_source
    print html

    #driver.find_element_by_xpath("//a[@href='/admin/area/Apex/waste/connector/default']//span["
     #                            "@class='menu-text'][contains(.,'STFP Address Connector')]").click()

    #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
     #"//button[@class='navbar-toggle menu-toggler pull-left']//span[@class='sr-only']"))).click()


    #print "Dropdown Found Worked"
    #except:
    #print "dropdown Failed"

    print "Page is ready!"

except EC as e:

    print "wouldnt load", e


driver.quit()


"""
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                    "//a["
                                                                    "@href='/admin/area/Apex/waste/connector/default']"))).click()
        print "Parcels Link found"
    except:
        print "parcels linke failed"

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                    "//a["
                                                                    "@data-href='/area/Apex/waste/connector/default/list/0']["
                                                                    "@href='#']"))).click()
        print "Export Parcels Btn found"
    except:
        print ("export parcels button failed")



    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
     #                                                           "//button["
      #                                                          "@class='btn btn-success']["
       #                                                         "@id='export-parcel']"))).click()"""




#bsobj = BeautifulSoup(pagesource, 'lxml')

#user = bsobj.find('div', {'id': 'login-box'}).find_all('input', {'type': 'email'})
#pw = bsobj.find('div', {'id': 'login-box'}).find_all('input', {'type': 'password'})
#elem = driver.find_element_by_xpath(".//input[@name='email']")
#element = driver.find_element_by_css_selector()
#time.sleep(10)

#un = driver.find_element_by_xpath("//input[@class='auth0-lock-input'][@name='email']").send_keys(
 #   "kerrin.cox@apexnc.org")
#pw = driver.find_element_by_xpath("//input[@class='auth0-lock-input'][@name='password']").send_keys(
 #   "ApexInfo14!")


#pw = driver.find_element_by_xpath("//input[@name='password']").send_keys("ApexInfo14!")
#WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.NAME,'email')))
#elem2 = driver.find_element_by_xpath("//div[@class='auth0-lock-form']")
#email = elem2.find_elements_by_name('email')


#driver.find_element_by_xpath("//button[@type='submit']").click()






#driver.find_element_by_id('login-box')#.send_keys("kerrin.cox@apexnc.org")
#driver.find_element_by_id ('login-passwordless')#.send_keys('ApexInfo14!')





