import re
import requests
from bs4 import BeautifulSoup
import eventRec

PRE_LOGIN_URL = "https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1"
# LOGIN_URL = "https://login.uillinois.edu/auth/SystemLogin/sm_login.fcc"
REGISTER_URL = "https://ui2web1.apps.uillinois.edu/BANPROD1/twbkwbis.P_GenMenu?name=bmenu.P_StuMainMnu"
BANNER_URL = "https://banner.apps.uillinois.edu/StudentRegistrationSSB/ssb/registration?mepCode=1UIUC"

class AddCoure:
    def __init__(self, user="ADMIN", term:str=120228, retry=5, session=requests.session()) -> None:
        self.user = user
        self.crn = 0
        self.term = term
        self.retry = retry
        self.base_url = "https://banner.apps.uillinois.edu/StudentRegistrationSSB/ssb/classRegistration/"
        self.params = {
                        'X-Requested-With': 'XMLHttpRequest','ADRUM': {'isAjax':'true'},'Connection': 'keep-alive', 'Host': 'banner.apps.uillinois.edu',
                            'Referer': 'https://banner.apps.uillinois.edu/StudentRegistrationSSB/ssb/classRegistration/classRegistration' }
        self.session = session
        self.isLogin = False

    def GetLoginParams(self, username:str, password:str) -> dict:
        p = self.session.get(PRE_LOGIN_URL)
        smagentname = re.search('name=smagentname value="(.*)"', p.text).groups()[0]
        smauthreason = ""
        smquerydata = ""
        params = {
        "SMENC": "ISO-8859-1",
        "SMLOCALE": "US-EN",
        "USER": username,
        "PASSWORD": password,
        "queryString": "null",
        "target": "HTTPS://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1",
        "smquerydata": smquerydata,
        "smauthreason": smauthreason,
        "smagentname": smagentname,
        "postpreservationdata": "",
        "BTN_LOGIN": "Log+In"}

        return params, p.url
    def Login(self, username:str, password:str) -> bool:
        params, url = self.GetLoginParams(username, password)
        login = self.session.post(url=url, data=params)
        banner = self.session.get(url=BANNER_URL)
        self.isLogin = True
        return True

    def AddCourse(self, crn: int):
        if not self.isLogin:
            eventRec.fail_msg(sId=self.user, msg="Fail to AddCourse, must Login first")
    



s = requests.session()
test = AddCoure()