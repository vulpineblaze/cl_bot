from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from urlparse import urlparse
from urlparse import parse_qs

from mongoengine import *

from urllib2 import urlopen

from pyvirtualdisplay import Display
import time
import datetime
import smtplib
import base64
import gc
import sys


SLEEP_SECONDS = 90
DRIVER_TIMEOUT = 5

DEBUG = False
# DEBUG = True


# mongodb://<dbuser>:<dbpassword>@ds119750.mlab.com:19750/mondodb_dev
# pocket bound123
# connect('mondodb_dev', host='mongodb://pocket:bound123@ds119750.mlab.com:19750/mondodb_dev')

connect('mondodb_dev', host='mongodb://pocket:bound123@ds119750.mlab.com:19750/mondodb_dev')

class Model(Document):
    desc =  StringField(max_length=1200, required=True)
    link =  URLField(max_length=1200, required=True)
    tags = StringField()
    thumb = FileField()
    file = FileField()

def model_saver(desc,link,tags):
    condition = True

    for link in Model.objects(link=link):
        checker = True

        if not desc == link.desc:
            link.desc = desc
            checker = False

        if not tags == link.tags:
            link.tags = tags
            checker = False

        # if not file == link.file:
        #     link.file = file
        #     checker = False

        if not checker:
            link.save()
            print "Tried to add dupe item, found diffs, overwritten!"
        else:
            print "Tried to add dupe item, found no diff, ignored!"

        if condition:
            condition = False
        

    if condition:
        this_model = Model(desc=desc,link=link,tags=tags)
        this_model.file.new_file()
        # this_model.file.write('some_image_data')

        response = urlopen(link)
        CHUNK = 16 * 1024
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            this_model.file.write(chunk)

        this_model.file.close()
        this_model.save()

        # debug
        with open(this_model.desc+"_model_found.ext", 'wb') as f:
            chunk = this_model.file.read()
            f.write(chunk) 
        


        

def initialize_webdriver():
    user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36")

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = user_agent

    driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    driver.set_page_load_timeout(DRIVER_TIMEOUT)
    driver.set_window_size(1120, 550)

    return driver

    
def find_model(list_of_models, page_cnt = 1):
    ''' finds a model on archive3d '''
    if DEBUG: print " inside find_model() " 

    model = {}
    driver = initialize_webdriver() 
    
    target_site = "https://archive3d.net/?page="
    # target_site = "https://www.google.com"
    trys = 0

    while True:
        try:
            print " try driver.get() "+target_site+str(page_cnt)
            driver.get(target_site+str(page_cnt))
        except TimeoutException:
            trys += 1
            print "Timeout #"+str(trys)+", retrying..."
            if trys > 3:
                break
            continue
        else:
            break

    if DEBUG: print " begin navigation in find_model() "



    a=[];
    a = driver.find_elements_by_class_name("b1");  


    if DEBUG: print " found class: "+str(a)

    count = 0
    for child in a:

        if DEBUG: print "child: " + str(child.text)+" | "+str(child.get_attribute("href"))
        if DEBUG: print "child class: "+ str(child.get_attribute("class"))
        the_link = child.find_element_by_css_selector('a').get_attribute('href')
        if DEBUG: print "child link: " + str(the_link)
        model['desc'] = str(child.text)

        if count >= 1:
            break #only run 5 during dev

        o = urlparse(the_link)
        if DEBUG: print "o is:"
        if DEBUG: print o
        the_query = parse_qs(o.query)
        if DEBUG: print the_query 
        the_id = str(the_query['id'][0])
        if DEBUG: print "id:" + the_id
        # print "link id is:" + str(o.id)
        dl_link = "https://archive3d.net/?a=download&do=get&id=" + the_id
        if DEBUG: print "dl_link is:" + dl_link
        model['link'] = str(dl_link)

        model['tags'] = grab_tags_from_link(the_link)

        #last thing in the loop!
        # list_of_models.append(model)
        model_saver(model['desc'],model['link'],model['tags'])

        count += 1

    driver.quit()

    return list_of_models




def grab_tags_from_link(the_link):
    ''' now we navigate to the_link and grab up the desired data '''

    if DEBUG: print " inside grab_tags_from_link() "



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

    if DEBUG: print " begin navigation in grab_tags_from_link() "

    # return 0


    info=[];
    info = driver.find_element_by_id("info");  


    if DEBUG: print " found id: "+str(info)

    if DEBUG: print "info: " + str(info.text)+" | "+str(info.get_attribute("href"))
    if DEBUG: print "info class: "+ str(info.get_attribute("class"))
    # print "info h2: "+str(info.find_elements_by_tag_name("h2")[0])
    h2 = info.find_elements_by_tag_name("h2")[0]
    if h2:
        if DEBUG: print "info h2: "+str(h2.text) 


    tag_index = info.text.find("Tags:")
    # x[2:]

    tag_string = info.text[tag_index:]
    if DEBUG: print "tag_string:"+tag_string
    # for each in info:
    #     print "info child:"+ each
    # links=[]
    # tmp = info.find_elements_by_tag_name("a")
    # for tag in tmp:
    #     # maybe_link = tag.get_attribute("href")
    #     if tag.text:
    #         print "tmp.tag.text: " + str(tag.text)
    #     else:
    #         print "tmp.tag: " + str(tag)
    #         maybe_link = tag.get_attribute("href")

    #         if maybe_link:
    #             # links.append(str(maybe_link.text))
    #             print "maybe_link: " + str(maybe_link)

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


    driver.quit()

    return tag_string




def main():
    '''business logic for when running this module as the primary one!'''
    display = Display(visible=0, size=(1024, 768))
    display.start()
    default_to_process = 10
    show_help = False

    print "archive3d bot started"


    list_of_models=[]


    print sys.argv 
    num_to_process = sys.argv[1]

    if num_to_process:
        if int(num_to_process):
            default_to_process = int(num_to_process)
        else:
            show_help = True
    else:
        show_help = True

    if show_help:
        print " >>> Run with first arg as amount to process. Default is 10."



    for i in range(0, int(default_to_process)):
        list_of_models = find_model(list_of_models, 1+(i*24))

    print list_of_models

    lastpost=""
    for post in Model.objects:
        print post.desc +" | "+ post.link
        lastpost = post

        # for dev, dont want db permanent:
        post.delete()
    # for the_link in list_of_models:
    #     # break
    #     grab_tags_from_link(the_link)
    # grab_tags_from_link("https://archive3d.net/?a=download&id=f8c7417c")
     

    print "lastpost: "+lastpost.link + ", and file:"+str(lastpost.file)
    CHUNK = 16 * 1024
    with open(post.desc+"_model.ext", 'wb') as f:
        while True:
            file = lastpost.file.read()
            for c in file.chunks():
                f.write(c.data)
            # chunk = lastpost.file.read(CHUNK)
            # if not chunk:
            #     break
            # # this_model.file.write(chunk)
            # # chunk = lastpost.file.read()
            # f.write(chunk) 
    
    
    display.stop()
    print "archive3d bot complete"


# Here's our payoff idiom!
if __name__ == '__main__':
    main()
