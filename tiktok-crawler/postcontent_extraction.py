from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from modules.general_classes import scrape
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import json

from colorama import Fore, Back, Style
from colorama import init

SCROLL_PAUSE_TIME = 1.5


class PostContentScraper:
    def __init__(self, driver):
        self.driver = driver
        self.hash = False

    def scrape_post_content(self, url):
        self.driver.get(url)
        time.sleep(3)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        scraped = scrape(soup)
        post = self.extraction(scraped, url)
        return post

    @staticmethod
    def extraction(scraped, url):
        # Find all the text within the div and its child elements
        text_postcontent = [tag.get_text(strip=True) for tag in scraped.postcontent.find_all()]
        return {'posturl': url,
                'postcontent': text_postcontent,
                'browseUser': scraped.browseUser,
                'views': 0,
                'likes': scraped.likes,
                'saves': scraped.saves,
                'shares': scraped.shares,
                'commentcounts': scraped.commentsCount}
