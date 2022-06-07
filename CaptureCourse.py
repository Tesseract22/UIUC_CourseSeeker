from distutils.log import error
from email import message
from multiprocessing.sharedctypes import Value
from os import times
from re import sub
import time
from requests import cookies
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
# from bs4 import BeautifulSoup
# /getRegistrationEvents?termFilter=null
BANNER_URL = "https://banner.apps.uillinois.edu/StudentRegistrationSSB/ssb/registration?mepCode=1UIUC"
TERM_URL = "https://banner.apps.uillinois.edu/StudentRegistrationSSB/ssb/term/termSelection?mode=registration"
UNIQE_ID_NAME = "xe.unique.session.storage.id"
IGNORE_COOKIES_KW = ['httpOnly', 'sameSite']
TERM_SELECT_URL = "https://banner.apps.uillinois.edu/StudentRegistrationSSB/ssb/term/search?mode=registration"
REGISTER_URL = "https://banner.apps.uillinois.edu/StudentRegistrationSSB/ssb/classRegistration"
ADD_API = "/addRegistrationItem?term=%i&courseReferenceNumber=%i&olr=false"
GET_API = "/getRegistrationEvents?termFilter=null"
GET_API_PARAM = "&crn=%i"
SUBMIT_API = "/submitRegistration/batch"

# refer to REGISTER_URL

class CaptuerCourse:
    def __init__(self, netid:str, password:str, term:int=120228, driver=webdriver.Edge(), session=requests.session(), retry=5):
        self.netid = netid
        self.password = password
        self.term = term
        self.driver = driver
        self.session = session
        self.isLogin = False
        self.session_id = ""
        self.retry = retry

    def Login(self) -> bool:

        self.driver.get(BANNER_URL)
        self.driver.get(TERM_URL)
        
        netid_key = self.driver.find_element(by=By.ID, value="netid")
        password_key = self.driver.find_element(by=By.NAME, value="PASSWORD")
        submit_key = self.driver.find_element(by=By.NAME, value="BTN_LOGIN")

        netid_key.send_keys(self.netid)
        password_key.send_keys(self.password)
        submit_key.click()

        # ! TO DO: Login Success Decider to be implemented !
        self.isLogin = True
        return True

    def GetCookies(self) -> list[dict]:
        if not self.isLogin:
            # ! TO DO: message !
            return
        res = self.driver.get_cookies()
        for cookie in res:
            for k in IGNORE_COOKIES_KW:
                try:
                    del cookie[k]
                except:
                    pass
        return res
    
    def GetSessionId(self) -> str:
        if not self.isLogin:
            # ! TO DO: message !
            return
        self.session_id = self.driver.execute_script("return window.sessionStorage;")[UNIQE_ID_NAME]
        return self.session_id
    def Close(self) -> None:
        self.driver.close()
        self.session.close()

    def LoadCookies(self) -> None:
        cookies_adrum_obj = cookies.create_cookie(**self.GetCookies()[0])
        cookies_jsessionid_obj = cookies.create_cookie(**self.GetCookies()[1])
        self.session.cookies.set_cookie(cookie=cookies_adrum_obj)
        self.session.cookies.set_cookie(cookie=cookies_jsessionid_obj)
        return cookies_jsessionid_obj
    def AttempBanner(self) -> None:
        b = self.session.get(TERM_URL)
        print(b.content)

    def SelectTerm(self) -> None:
        
        term_input = self.driver.find_element(By.NAME, value="txt_term")
        self.driver.execute_script("arguments[0].setAttribute('value', %s)"%self.term, term_input)
        self.driver.execute_script("arguments[0].setAttribute('listofsearchterms', %s)"%self.term, term_input)

        term_go = self.driver.find_element(By.ID, "term-go")
        term_go.click()

    def GetRegisteredCourses(self, load_limit:int=50, load_interval:int=0.5) -> list[dict]:
        # ! TO DO !
        times = 0
        courses = list()
        while times < load_limit:
            time.sleep(load_interval)
            times += 1
            courses = json.loads(self.session.get(url=REGISTER_URL + GET_API).content)
            if courses != list():
                break
        return courses
    def AddCourse(self, crn:int, load_limit:int=50, load_interval:int=0.5) -> bool:
        # ! TO DO: Detect what prevent from adding course !
        # Course that are not submitted would be clear after closed
        times = 0
        res = list()
        while times < load_limit:
            time.sleep(load_interval)
            times += 1
            res = json.loads(self.session.post(REGISTER_URL + ADD_API%(self.term, crn)).content)
            if res["success"] or res["message"] != "Please contact the help desk":
                break
        return res["success"]
    def SubmitCourse(self):
        # ! TO DO !
        submit = json.loads(self.session.post(REGISTER_URL + SUBMIT_API).content)
        if not submit["success"]:
            print("internet connection error")
        message = submit["message"]
        course = submit["data"]["update"][-1]
        course_info = course["subject"] + " " + course["campus"] + " " + course["courseReferenceNumber"]
        error_flag = course["errorFlag"]
        message_type = course["messageType"]
        return error_flag == None, message_type, course_info
                # print(submit)
        # with open("test.txt", "wb") as f:
        #     f.write(submit.content)
        pass
    def CaptureCourseUntil(self) -> None:
        # ! TO DO !
        pass

    def main(self):
        # ! TO DO !
        self.Login()
        self.SelectTerm()
        self.LoadCookies()
        self.AddCourse(29867)
        self.SubmitCourse()
        self.Close()


