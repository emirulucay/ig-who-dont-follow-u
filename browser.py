from selenium import webdriver
import time
import userInfo as info


class Browser:
    def __init__(self, link):
        self.link = link
        self.browser = webdriver.Chrome()
        self.followers = []
        self.myFollows = []

        self.openInstagram()
        self.login()
        self.goProfile()
        self.getFollowers()
        self.getMyFollows()
        self.showDetails()

    def openInstagram(self):
        self.browser.get(self.link)
        time.sleep(2)

    def login(self):
        username = self.browser.find_element_by_name("username")
        password = self.browser.find_element_by_name("password")

        username.send_keys(info.userName)
        password.send_keys(info.password)

        loginBtn = self.browser.find_element_by_css_selector(
            "#loginForm > div > div:nth-child(3) > button")
        loginBtn.click()
        time.sleep(5)

    def goProfile(self):
        self.browser.get(self.link+"/"+"ahmetysf07")
        time.sleep(3)

    def getFollowers(self):
        self.browser.find_element_by_css_selector(
            "#react-root > section > main > div > header > section > ul > li:nth-child(2) > a > div").click()
        time.sleep(4)

        Browser.scrollDown(self)

        div = self.browser.find_elements_by_xpath(
            "/html/body/div[6]/div/div/div/div[2]/ul/div")
        for j in div:
            _followers = j.text.split('\n')
            followers = set(_followers)
            for i in followers:
                if i != "Çıkar":
                    self.followers.append(i)

        time.sleep(1)
        self.browser.find_element_by_xpath(
            "/html/body/div[6]/div/div/div/div[1]/div/div[3]/div/button").click()
        time.sleep(2)

    def getMyFollows(self):
        time.sleep(2)
        self.browser.find_element_by_css_selector(
            "#react-root > section > main > div > header > section > ul > li:nth-child(3) > a > div").click()
        time.sleep(4)

        Browser.scrollDown(self)

        div = self.browser.find_element_by_xpath(
            "/html/body/div[6]/div/div/div/div[3]/ul/div")
        for i in div.text.split('\n'):
            if i != "Takiptesin":
                self.myFollows.append(i)

        time.sleep(2)

    def showDetails(self):
        counter = 0
        for follow in self.myFollows:
            if(follow in self.followers):
                return
            else:
                if(follow == "Doğrulanmış") or (follow == "Takip") or (follow == "Takiptesin") or (follow == "İstek Gönderildi"):
                    return
                counter += 1
                print(f"=> {follow} seni takip etmiyor!")

        if counter == 0:
            print("Takip ettiğin herkes seni takip ediyor.")

    def scrollDown(self):
        jsKomut = """
		sayfa = document.querySelector(".isgrP");
		sayfa.scrollTo(0,sayfa.scrollHeight);
		var sayfaSonu = sayfa.scrollHeight;
		return sayfaSonu;
		"""
        sayfaSonu = self.browser.execute_script(jsKomut)
        while True:
            son = sayfaSonu
            time.sleep(3.5)
            sayfaSonu = self.browser.execute_script(jsKomut)
            if son == sayfaSonu:
                break
