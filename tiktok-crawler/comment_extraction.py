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

SCROLL_PAUSE_TIME = 1

class CommentScrapper:

    def __init__(self, driver):
        self.driver = driver
        self.commentReplies = []

    def scrapper_comment(self, keyword, url):

        global last_height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Thực hiện script để cuộn xuống thêm một khoảng cách cụ thể
            self.driver.execute_script(f"window.scrollBy(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(2)  # Adjust the time according to your needs
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        scraped = scrape(soup)
        for comment in scraped.comments:
            try:
                self.commentReplies.append(
                    comment.find("p",
                                 {"data-e2e": "view-more-1"}).text.replace('View more replies (', '').replace(')', ''))
            except:
                self.commentReplies.append(0)
        df_cmt = pd.DataFrame(
            columns=['Userlink', 'originalPost', 'UserName', 'ReplyContent', 'Replylikes', 'replies'])
        for (User, Link, Name, Content, Likes, Replies) in zip(scraped.commentUser, scraped.commentUserLink,
                                                               scraped.commentUserName, scraped.commentContent,
                                                               scraped.commentLikes, self.commentReplies):
            comment_content = {'Userlink': Link,
                                'originalPost': url.split('/')[-1],
                                'UserName': Name,
                                'ReplyContent': Content,
                                'Replylikes': Likes,
                                'replies': self.commentReplies}
            df_cmt.loc[len(df_cmt.index)] = comment_content
            save_csv(df_cmt, f'cmt_post_{keyword}.csv')
