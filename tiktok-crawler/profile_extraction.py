import scrape as scrape
import time, random, json, platform
from bs4 import BeautifulSoup
from modules.general_classes import *
import requests
import json
import pandas as pd
from colorama import Fore, Back, Style
from colorama import init
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SCROLL_PAUSE_TIME = 0.5


class ProfileScraper:
    def __init__(self, driver):
        self.driver = driver
        self.video_views_text = 0

    def scrape_profile_info(self, profile_url, video_url):
        self.driver.get(profile_url)
        time.sleep(3)
        scroll_distance = 500
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        wait = WebDriverWait(self.driver, 10)
        scroll = True
        while scroll:
            start_time = time.time()
            # Thực hiện script để cuộn xuống thêm một khoảng cách cụ thể
            self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
            page_source = self.driver.page_source
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Đợi cho các phần tử mới tải xuống sau khi cuộn
            wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
            last_height = self.driver.execute_script('return document.body.scrollHeight')
            try:
                # Tìm phần tử a cụ thể với href
                link_element = self.driver.find_element(By.XPATH, f'//a[@href="{video_url}"]')
                # Tìm thẻ <strong> bên trong liên kết
                strong_element = link_element.find_element(By.XPATH, '//strong[@data-e2e="video-views"]')
                print(strong_element)
                # Lấy văn bản bên trong thẻ <strong>
                self.video_views_text = strong_element.text
                print(self.video_views_text)
                scroll = False
                break
            except:
                scroll = True

            if time.time() - start_time > 5:
                break

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            last_height = new_height

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        views, profile = self.extract_profile_info(profile_url, soup)
        return views, profile

    def extract_profile_info(self, profile_url, soup):
        try:
            following = soup.find("strong", {"title": "Following"}).text
        except:
            following = 0
        try:
            likes = soup.find("strong", {"title": "Likes"}).text
        except:
            likes = 0
        try:
            followers = soup.find("strong", {"title": "Followers"}).text
        except:
            followers = 0
        try:
            name = soup.find("h1", {"data-e2e": "user-title"}).text
        except:
            name = ""

        profile_info = {
            'Userlink': profile_url,
            'UserName': name,
            'UserFollowing': following,
            'UserFollowers': followers,
            'UserLikes': likes
        }
        return self.video_views_text, profile_info
