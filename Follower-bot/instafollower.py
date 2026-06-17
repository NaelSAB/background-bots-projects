from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException
import time




class InstaFollower:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, timeout=10)


    def login(self, url, user, password):
        self.driver.get(url)
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        username_input.send_keys(user)
        password_input = self.driver.find_element(By.NAME, "pass")
        password_input.send_keys(password)
        login_btn = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Log In"]')
        login_btn.click()
        try:
            save_login = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and text()="Not now"]')))
            save_login.click()
        except Exception as e:
            print(f"Unexpected error: {e}")
        try:
            Turn_on_notifications = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')))
            Turn_on_notifications.click()
        except Exception as e:
            print(f"Unexpected error: {e}")


    def find_followers(self, account):
        new_url = f"https://www.instagram.com/{account}"
        self.driver.get(new_url)
        followers = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "followers")]')))
        followers.click()
        time.sleep(2)

    def follow(self):
        all_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button._aswp._aswr')
        for button in all_buttons:
            try:
                self.driver.execute_script("arguments[0].click();", button)
                time.sleep(1)
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Cancel')]")
                cancel_button.click()
