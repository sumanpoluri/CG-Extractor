'''
Created on Aug 2, 2017

@author: sumanpoluri
'''

from sys import exit
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import UnexpectedAlertPresentException
import mysql.connector
from mysql.connector import Error as MysqlError

class Listing:
    """Represents a Craigslist listing"""
    
    def __init__(self):
        self.id = None
        self.createdTs = None
        self.sourceId = None
        self.postedTime = None
        self .title = None
        self.link = None
        self.sourceListingId = None
        self.location = None
        self.category = None
        self.message = None
        self.contactName = None
        self.contactPhoneNumbers = []
        self.contactEmailAddresses = []
    
def main():
    # Define error log file
    #path_to_log = '/Users/yourname/Desktop/'
    #log_errors = open(path_to_log + 'log_errors.txt', mode = 'w')
    
    path_to_chromedriver = '/usr/local/bin/chromedriver'
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)
    #path_to_firefoxdriver = '/usr/local/bin/geckodriver'
    #browser = webdriver.Firefox(executable_path=path_to_firefoxdriver)
    
    url = 'https://sanantonio.craigslist.org/search/hsw'
    browser.get(url)
    
    try:
        print "Waiting for the results to appear..."
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "paginator")]')))
        print "Results loaded. Locating the page number range..."
        pageNumRangeEls = []
        pageNumRangeEls = browser.find_elements_by_xpath('//span[contains(@class, "pagenum")]/span[@class="range"]')
        print "Found", pageNumRangeEls.__len__(), "page number range elements"
        
        if (pageNumRangeEls.__len__() == 0):
            print "Could not locate the page number range. Something's wrong."
            exit()
        
        print "Locating the current sort type..."
        sortedOn = browser.find_element_by_xpath('//div[@class="search-sort"]/div[contains(@class, "dropdown-sort")]/ul[contains(@class, "dropdown-list")]/li[@aria-selected="true"]/a')
        print "Currently sorted by " + str(sortedOn.text)
        
        if (sortedOn.text != "newest"):
            print "Locating the sort dropdown..."
            sortButtonDiv = browser.find_element_by_xpath('//div[@class="search-sort"]/div[contains(@class, "dropdown-sort")]')
            sortButtonDiv.click()
            print "Locating the sort by newest option..."
            sortByDateOption = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="search-sort"]/div[contains(@class, "dropdown-sort")]/ul[contains(@class, "dropdown-list")]/li[@aria-selected="false"]/a[@data-selection="date"]')))
            print "Found, sorting by " + str(sortByDateOption.text.encode('utf-8'))
            sortByDateOption.click()
            
        print "Getting search results..."
        results = browser.find_elements_by_xpath('//p[@class="result-info"]')
        print "Found", results.__len__(), "entries"
        
        if results.__len__() == 0:
            exit()
        
        # Get Database Connection
        conn = getDbConnection()
        
        for index, result in enumerate(results):
            seconds = 5 + (random.random() * 5)
            time.sleep(seconds)
            
            timeElement = result.find_element_by_tag_name('time')
            resultLink = result.find_element_by_class_name('result-title')
            print "Result", index+1, timeElement.get_attribute('datetime'), resultLink.text, resultLink.get_attribute('href'), resultLink.get_attribute('data-id')
            
            listing = Listing()
            listing.sourceId = 1 # Craigslist
            listing.postedTime = timeElement.get_attribute('datetime')
            listing.title = resultLink.text
            listing.link = resultLink.get_attribute('href')
            listing.sourceListingId = resultLink.get_attribute('data-id')
            listing.location = "San Antonio"
            listing.category = "hsw"
            
            # Open result in new tab
            print "Opening a new tab for this result"
            actions = ActionChains(browser)
            actions.key_down(Keys.COMMAND).click(resultLink).key_up(Keys.COMMAND).perform()
            print "Switching to the new tab"
            browser.switch_to_window(browser.window_handles[1])
            
#             print "Waiting to click the 'reply' button..."
#             seconds = 5 + (random.random() * 5)
#             time.sleep(seconds)
            
#             print "Clicking the 'reply' button..."
#             replyButton = browser.find_element_by_class_name('reply_button')
#             replyButton.click()
            
            # Wait for the reply information to laod
            # Sometimes, a CAPTCHA or reCAPTCHA is presented. In that case, alert the user to solve it before continuing...
#             replyBox = None
#             
#             if replyBox == None:
#                 try:
#                     replyBox = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'replyflap')))
#                 except TimeoutException:
#                     # If timed out, look for a reCATPCHA
#                     print "'reply' button not found. Could be due to captcha..."
#                     captchaForm = browser.find_element_by_class_name('captcha_form')
#                     if captchaForm:
#                         print "Captcha detected..."
#                         try:
#                             browser.execute_script('window.alert("reCAPTCHA detected. Solve to continue.")')
#                         except UnexpectedAlertPresentException:
#                             # This is expected
#                             print "Alerted user about the reCAPTCHA input"
#     
#                         replyBox = WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'replyflap')))
#                     
#             if replyBox == None:
#                 print "Reply information not loaded. Proceeding without reply information."
#             else:
#                 print "Reply information found"
#             
#             replyInfoItems = replyBox.find_elements_by_tag_name('li')
            contactName = ""
            phoneNumbers = []
            emailAddresses = []
            listingMessage = browser.find_element_by_id('postingbody').text
#             for replyInfoItem in replyInfoItems:
#                 className = replyInfoItem.get_attribute("class")
#                 print "className = " + str(className)
#                 
#                 if className == "reply-tel":
#                     phoneNumbers += replyInfoItem.find_element_by_class_name('reply-tel-number').text
#                 elif className == "reply-email":
#                     emailAddresses += replyInfoItem.find_element_by_class_name('mailapp').text
#                 else:
#                     replyInfoItemHeader = replyInfoItem.find_element_by_tag_name('h1')
#                     if replyInfoItemHeader.text == "contact name:":
#                         contactName = replyInfoItem.find_element_by_tag_name('p').text
#                         
            print "Name:", contactName, "\nPhone numbers:", str(phoneNumbers), "\nEmail Addresses:", str(emailAddresses) + "\nListing Message:", listingMessage
            
            listing.message = listingMessage
            listing.contactName = contactName
            listing.contactPhoneNumbers = phoneNumbers
            listing.contactEmailAddresses = emailAddresses
            saveListing(conn, listing)
            
            # Close tab and return to results tab
            print "Closing this tab"
            #actions = ActionChains(browser)
            #actions.key_down(Keys.COMMAND).key_down('w').key_up(Keys.COMMAND).key_up('w').perform()
            #browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
            browser.close()
            print "Switching back to the results tab"
            browser.switch_to_window(browser.window_handles[0])
            
#             if index == 1:
#                 break 
            
        # Get Database Connection
        closeDbConnection(conn)
        
    except TimeoutException:
        #log_errors.write('couldnt locate button XYZ when searching for "balloon"' + '\n')
        print "Results did not load in 5s"
        
def saveListing(conn, listing):
    """ Save listing in database """
    print "Saving this listing"
    isListingAlreadyPresent = findListingExistsBySourceListingIdAndPostedDate(conn, listing.sourceListingId, listing.postedTime)
    print "isListingAlreadyPresent?", isListingAlreadyPresent
     
    if isListingAlreadyPresent == False:
        insertListing(conn, listing)
    
    
def findListingExistsBySourceListingIdAndPostedDate(conn, sourceListingId, postedTime):
    """ Fetch listing from database """
    print "findListingExistsBySourceListingId...sourceListingId =", sourceListingId, ", postedTime =", postedTime
    query = "SELECT * " \
            "FROM leoresearch.real_estate_listings " \
            "WHERE source_listing_id = %s " \
            "AND DATE(posted_time) = DATE('%s') " \
            "LIMIT 1" % (sourceListingId, postedTime)
    print "query =", query
    listingFound = False
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        
        if row is not None:
            print(row)
            listingFound = True
        else:
            print "No row found"
            listingFound = False
    except MysqlError as e:
        print e
    finally:
        cursor.close()
    
    return listingFound
    
def insertListing(conn, listing):
    """ Insert listing in database """
    print "Inserting this listing"
    query = "INSERT INTO leoresearch.real_estate_listings (created_ts, source_id, posted_time, title, link, source_listing_id, location, category, message, contact_name, contact_phone_numbers, contact_email_addresses) " \
            "VALUES (UTC_TIMESTAMP(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    args = (listing.sourceId, listing.postedTime, listing.title, listing.link, listing.sourceListingId, listing.location, listing.category, listing.message, listing.contactName, str(listing.contactPhoneNumbers), str(listing.contactEmailAddresses))
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, args)
        
        if cursor.lastrowid:
            print "Inserted row id =", cursor.lastrowid
        else:
            print "Last insert id not found"
        
        conn.commit()
    except MysqlError as e:
        print e
    finally:
        cursor.close()

def getDbConnection():
    """ Connect to database """
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='leoresearch',
            user='root',
            password='root' )
        
        if conn.is_connected():
            print "Connected to the database"
            return conn
            
    except MysqlError as e:
        print "Could not connect to the database " + str(e)
        
    
def closeDbConnection(conn):
    """ Close database connection """
    try:
        if conn == None:
            return
        
        if not conn.is_connected:
            return
            
        conn.close()
        print "Database connection closed"
            
    except MysqlError as e:
        print "Encountered " + str(e)
        
if __name__ == "__main__":
    main()