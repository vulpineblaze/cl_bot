from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import time
import datetime
import smtplib
import base64
import gc

SLEEP_SECONDS = 90

def find_cl_post():
    cl_post = {}
    driver = webdriver.PhantomJS()
    driver.get("https://sacramento.craigslist.org/zip/")
    # assert "Python" in driver.title
    
    # elem = driver.find_element_by_class_name("row")
    # cl_id = elem.get_attribute('data-pid')
    # elem = driver.find_elements_by_xpath("//p[contains(@class,'row')]/span")
    
    elements = driver.find_elements_by_xpath("//span[@class='pl']/a")
    # title = elements.find_element_by_tag_name("a")
    # title = elements[1].find_elements_by_xpath(".//a[@class='']")
    count = 0
    for child in elements:
        cl_post['title'] = str(child.text)
        cl_post['link'] = str(child.get_attribute("href"))
        break
        # print str(child.text)+" | "+str(child.get_attribute("href"))
        # count += 1
        # if count > 5:
            # break
        
    # print str(title)
    
    # elem.send_keys("selenium")
    # elem.send_keys(Keys.RETURN)
    driver.quit()
    
    return cl_post
    
def send_cl_email(cl_post):
    print "send email! "+cl_post['title']+" | "+cl_post['link']
    
    fromaddr = 'yourcompusolutions@gmail.com'
    toaddrs  = 'jacobmaestre916@gmail.com'
    
    passwd = "NTQkQXNob3Q="
    
    msg = "\r\n".join([
        "From: "+fromaddr,
        "To:  "+toaddrs,
        "Subject: NEW CL! "+cl_post['title'],
        "",
        "What up Jacob!",
        "",
        "I'm a bot telling you about a post I perceive as new from craigslist!",
        "",
        "Post has the title: \""+cl_post['title']+ "\" and heres the link: "+cl_post['link'],
        ""
        ])

   
    # Credentials (if needed)
    username = 'yourcompusolutions'
    password = base64.b64decode(passwd)

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    try:
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, msg)
    except:
        print "Failed to contact GMail at" + str(datetime.date.today())
    finally:
        server.quit()
    
def main():
    '''business logic for when running this module as the primary one!'''
    display = Display(visible=0, size=(1024, 768))
    display.start()

    fresh_cl_post = find_cl_post()
    prev_cl_post = {"title":"","link":""}
    old_cl_post = {"title":"","link":""}
    
    # find_cl_post()
    while True:
        # print "TEST" + str(datetime.date.today())
        fresh_cl_post = find_cl_post()
        
        try:
            if fresh_cl_post['title'] != prev_cl_post['title']:
            
                old_cl_post = prev_cl_post
                prev_cl_post = fresh_cl_post
            
                send_cl_email(fresh_cl_post)

        except:
            print "Failed to test & send mail at: "+str(datetime.datetime.now())

        gc.collect()
        time.sleep(SLEEP_SECONDS)
        
    
    
    display.stop()

# Here's our payoff idiom!
if __name__ == '__main__':
    main()
