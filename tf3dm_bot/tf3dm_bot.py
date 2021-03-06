from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from pyvirtualdisplay import Display
import time
import datetime
import smtplib
import base64
import gc

SLEEP_SECONDS = 90
DRIVER_TIMEOUT = 13

# def find_cl_post():
#     cl_post = {}
#     driver = webdriver.PhantomJS()
#     driver.get("https://sacramento.craigslist.org/zip/")
#     # assert "Python" in driver.title
    
#     # elem = driver.find_element_by_class_name("row")
#     # cl_id = elem.get_attribute('data-pid')
#     # elem = driver.find_elements_by_xpath("//p[contains(@class,'row')]/span")
    
#     elements = driver.find_elements_by_xpath("//span[@class='pl']/a")
#     # title = elements.find_element_by_tag_name("a")
#     # title = elements[1].find_elements_by_xpath(".//a[@class='']")
#     count = 0
#     for child in elements:
#         cl_post['title'] = str(child.text)
#         cl_post['link'] = str(child.get_attribute("href"))
#         break
#         # print str(child.text)+" | "+str(child.get_attribute("href"))
#         # count += 1
#         # if count > 5:
#             # break
        
#     # print str(title)
    
#     # elem.send_keys("selenium")
#     # elem.send_keys(Keys.RETURN)
#     driver.quit()
    
#     return cl_post
    
# def send_cl_email(cl_post):
#     print "send email! "+cl_post['title']+" | "+cl_post['link']
    
#     fromaddr = 'yourcompusolutions@gmail.com'
#     toaddrs  = 'jacobmaestre916@gmail.com'
    
#     passwd = "NTQkQXNob3Q="
    
#     msg = "\r\n".join([
#         "From: "+fromaddr,
#         "To:  "+toaddrs,
#         "Subject: NEW CL! "+cl_post['title'],
#         "",
#         "What up Jacob!",
#         "",
#         "I'm a bot telling you about a post I perceive as new from craigslist!",
#         "",
#         "Post has the title: \""+cl_post['title']+ "\" and heres the link: "+cl_post['link'],
#         ""
#         ])

   
#     # Credentials (if needed)
#     username = 'yourcompusolutions'
#     password = base64.b64decode(passwd)

#     # The actual mail send
#     server = smtplib.SMTP('smtp.gmail.com:587')
#     try:
#         server.starttls()
#         server.login(username,password)
#         server.sendmail(fromaddr, toaddrs, msg)
#     except:
#         print "Failed to contact GMail at" + str(datetime.date.today())
#     finally:
#         server.quit()
    
def find_model():
    ''' finds a model on tf3dm '''
    print " inside find_model() "

    model = []
    driver = webdriver.PhantomJS()
    driver.set_page_load_timeout(DRIVER_TIMEOUT)
    target_site = "http://www.tf3dm.com/"
    trys = 0

    while True:
        try:
            print " try driver.get() "+target_site
            driver.get(target_site)
        except TimeoutException:
            trys += 1
            print "Timeout #"+str(trys)+", retrying..."
            if trys > 3:
                break
            continue
        else:
            break

    # driver.get("")
    # driver.get("http://google.com/")
    # assert "Python" in driver.title
    
    # elem = driver.find_element_by_class_name("row")
    # cl_id = elem.get_attribute('data-pid')
    # elem = driver.find_elements_by_xpath("//p[contains(@class,'row')]/span")
    
    # elements = driver.find_elements_by_xpath("//span[@class='pl']/a")
    print " begin navigation in find_model() "

    # return 0


    a=[];
    a = driver.find_elements_by_class_name("model-entry-block");  
    # title = elements.find_element_by_tag_name("a")
    # title = elements[1].find_elements_by_xpath(".//a[@class='']")

    print " found class: "+str(a)

    count = 0
    for child in a:
        # model['title'] = str(child.text)
        # model['link'] = str(child.get_attribute("href"))
        print "child: " + str(child.text)+" | "+str(child.get_attribute("href"))

        print "child class: "+ str(child.get_attribute("class"))

        # elem = child.find_element_by_class_name("left-side")

        # print "elem: " + str(elem.text)+" | "+str(elem.get_attribute("href"))

        # print "elem class: "+ str(elem.get_attribute("class"))

        # print "elem link: " + str(elem.find_element_by_css_selector('a').get_attribute('href'))

        the_link = child.find_element_by_css_selector('a').get_attribute('href')

        print "child link: " + str(the_link)

        model.append(the_link)

        break #only run once during dev
    
        # print str(child.text)+" | "+str(child.get_attribute("href"))
        # count += 1
        # if count > 5:
            # break
        
    # print str(title)
    
    # elem.send_keys("selenium")
    # elem.send_keys(Keys.RETURN)
    driver.quit()

    return model


def grab_stuff_from_link(the_link):
    ''' now we navigate to the_link and grab up the desired data '''

    print " inside grab_stuff_from_link() "
    driver = webdriver.PhantomJS()
    driver.set_page_load_timeout(DRIVER_TIMEOUT)
    trys=0

    while True:
        try:
            print " try driver.get() "+str(the_link)
            driver.get(the_link)
        except TimeoutException:
            trys += 1
            print "Timeout #"+str(trys)+", retrying..."
            if trys > 3:
                break
            continue
        else:
            break

    # at this point we have the loaded detail page via driver

    print " begin navigation in grab_stuff_from_link() "

    # return 0


    a=[];
    a = driver.find_element_by_id("dl_btn_loader");  
    # title = elements.find_element_by_tag_name("a")
    # title = elements[1].find_elements_by_xpath(".//a[@class='']")

    print " found id: "+str(a)

    print "a: " + str(a.text)+" | "+str(a.get_attribute("href"))
    print "a class: "+ str(a.get_attribute("class"))

    # count = 0
    # for child in a:
    #     # model['title'] = str(child.text)
    #     # model['link'] = str(child.get_attribute("href"))
    #     print "child: " + str(child.text)+" | "+str(child.get_attribute("href"))

    #     print "child class: "+ str(child.get_attribute("class"))

    #     break #only run once during dev



def main():
    '''business logic for when running this module as the primary one!'''
    display = Display(visible=0, size=(1024, 768))
    display.start()

    print "tf3dm bot started"

    model = find_model()

    for the_link in model:
        grab_stuff_from_link(the_link)

    # fresh_cl_post = find_cl_post()
    # prev_cl_post = {"title":"","link":""}
    # old_cl_post = {"title":"","link":""}
    
    # # find_cl_post()
    # while True:
    #     # print "TEST" + str(datetime.date.today())
    #     fresh_cl_post = find_cl_post()
        
    #     try:
    #         if fresh_cl_post['title'] != prev_cl_post['title']:
            
    #             old_cl_post = prev_cl_post
    #             prev_cl_post = fresh_cl_post
            
    #             send_cl_email(fresh_cl_post)

    #     except:
    #         print "Failed to test & send mail at: "+str(datetime.datetime.now())

    #     gc.collect()
    #     time.sleep(SLEEP_SECONDS)
        
    
    
    display.stop()
    print "tf3dm bot complete"


# Here's our payoff idiom!
if __name__ == '__main__':
    main()
