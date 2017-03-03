from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


from pyvirtualdisplay import Display
import time
import datetime
import smtplib
import base64
import gc

SLEEP_SECONDS = 90
DRIVER_TIMEOUT = 2

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

def initialize_webdriver():
    user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36")

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = user_agent

    driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    driver.set_page_load_timeout(DRIVER_TIMEOUT)
    driver.set_window_size(1120, 550)

    return driver

    
def find_model():
    ''' finds a model on archive3d '''
    print " inside find_model() "

    model = []
    driver = initialize_webdriver() 
    target_site = "https://archive3d.net/"
    # target_site = "https://www.google.com"
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
    a = driver.find_elements_by_class_name("b1");  
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
    # return 0;


    driver = initialize_webdriver() 
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


    info=[];
    info = driver.find_element_by_id("info");  
    # title = elements.find_element_by_tag_name("a")
    # title = elements[1].find_elements_by_xpath(".//a[@class='']")

    print " found id: "+str(info)

    print "info: " + str(info.text)+" | "+str(info.get_attribute("href"))
    print "info class: "+ str(info.get_attribute("class"))
    # print "info h2: "+str(info.find_elements_by_tag_name("h2")[0])
    # h2 = info.find_elements_by_tag_name("h2")[0]
    # if h2:
    #     print "info h2: "+str(h2)

    # for each in info:
    #     print "info child:"+ each
    # links=[]
    # tmp = info.find_element_by_tag_name("p")
    # for tag in tmp:
    #     if tag.get_attribute("href"):
    #         links.append(str(tag.get_attribute("href").text))

    # print "info tag: "+str(tag)

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

    print "archive3d bot started"

    model = find_model()

    for the_link in model:
        break
        # grab_stuff_from_link(the_link)

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
    print "archive3d bot complete"


# Here's our payoff idiom!
if __name__ == '__main__':
    main()
