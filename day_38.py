from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

SIMILAR_ACCOUNT = "buzzfeedtasty"
USERNAME = "username"
PASSWORD = "passwoed"


class InstaFollower:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()

    def login(self):
        url = "https://www.instagram.com/accounts/login/"
        self.driver.get(url)
        time.sleep(2)


        decline_cookies_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]"
        cookie_warning = self.driver.find_elements(By.XPATH, decline_cookies_xpath)
        if cookie_warning:
            cookie_warning[0].click()

        username = self.driver.find_element(by=By.NAME, value="username")
        password = self.driver.find_element(by=By.NAME, value="password")

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        time.sleep(2.1)
        password.send_keys(Keys.ENTER)

        time.sleep(10)
        save_login_prompt = self.driver.find_element(by=By.XPATH, value="//div[contains(text(), 'Not now')]")
        if save_login_prompt:
            save_login_prompt.click()

    def find_followers(self):
        self.driver.get("https://www.instagram.com/buzzfeedtasty/")

        time.sleep(10)
        follow = self.driver.find_element(By.XPATH, value="//div[contains(text(), 'Follow')]")
        follow.click()

        time.sleep(15)

        follow_all = self.driver.find_element(By.XPATH, value="//div[contains(text(), 'Follow')]")

        for i in range(5):
            follow_all.click()

    def close_browser(self):
        self.driver.quit()



if __name__ == "__main__":
    bot = InstaFollower()
    bot.login()
    time.sleep(10)
    bot.close_browser()
