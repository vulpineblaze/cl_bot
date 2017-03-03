from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from urlparse import urlparse
from urlparse import parse_qs

from pyvirtualdisplay import Display
import time
import datetime
import smtplib
import base64
import gc

SLEEP_SECONDS = 90
DRIVER_TIMEOUT = 5



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

    print " begin navigation in find_model() "



    a=[];
    a = driver.find_elements_by_class_name("b1");  


    print " found class: "+str(a)

    count = 0
    for child in a:

        print "child: " + str(child.text)+" | "+str(child.get_attribute("href"))
        print "child class: "+ str(child.get_attribute("class"))
        the_link = child.find_element_by_css_selector('a').get_attribute('href')
        print "child link: " + str(the_link)
        model.append(the_link)

        break #only run once during dev

    o = urlparse(the_link)
    print "o is:"
    print o
    the_query = parse_qs(o.query)
    print the_query 
    the_id = str(the_query['id'][0])
    print "id:" + the_id
    # print "link id is:" + str(o.id)
    dl_link = "https://archive3d.net/?a=download&do=get&id=" + the_id
    print "dl_link is:" + dl_link

    driver.quit()

    return model




def grab_stuff_from_link(the_link):
    ''' now we navigate to the_link and grab up the desired data '''

    print " inside grab_stuff_from_link() "



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


    print " found id: "+str(info)

    print "info: " + str(info.text)+" | "+str(info.get_attribute("href"))
    print "info class: "+ str(info.get_attribute("class"))
    # print "info h2: "+str(info.find_elements_by_tag_name("h2")[0])
    h2 = info.find_elements_by_tag_name("h2")[0]
    if h2:
        print "info h2: "+str(h2.text)

    # for each in info:
    #     print "info child:"+ each
    # links=[]
    tmp = info.find_elements_by_tag_name("a")
    for tag in tmp:
        # maybe_link = tag.get_attribute("href")
        if tag.text:
            print "tmp.tag.text: " + str(tag.text)
        else:
            print "tmp.tag: " + str(tag)
            maybe_link = tag.get_attribute("href")

            if maybe_link:
                # links.append(str(maybe_link.text))
                print "maybe_link: " + str(maybe_link)

        # tag_link = tag.find_element_by_css_selector('a').get_attribute('href')
        # print "tag link: " + str(the_link)



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

    # for the_link in model:
    #     # break
    #     grab_stuff_from_link(the_link)
    # grab_stuff_from_link("https://archive3d.net/?a=download&id=f8c7417c")


        
    
    
    display.stop()
    print "archive3d bot complete"


# Here's our payoff idiom!
if __name__ == '__main__':
    main()
