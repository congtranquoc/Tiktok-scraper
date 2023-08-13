#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import scrape as scrape
from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException
from modules.general_classes import *
from postcontent_extraction import *
from profile_extraction import *
from comment_extraction import *

init()
osID = platform.system().lower()
SCROLL_PAUSE_TIME = 2


def configure():
    load_dotenv()
def load_driver():
    ### Using Selenium as a puppeteer for amazon scraper
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    if 'windows' in osID:
        s = Service('C:/Program Files/Google/Chrome/Application/chromedriver.exe')  # Put the path of your chromedriver
        driver = webdriver.Chrome(service=s, options=options)
        return driver
def main(driver, keyword):
    post_scraper = PostContentScraper(driver)
    profile_scraper = ProfileScraper(driver)
    comment_scrapper = CommentScrapper(driver)

    if '#' in keyword:
        # https://www.tiktok.com/tag/jairbolsonaro
        driver.get(f'https://www.tiktok.com/tag/{keyword.replace("#", "")}')
        hashed = True
    else:
        ## Open page results with Keywork as query string
        driver.get(f'https://www.tiktok.com/search?q={keyword}')
        hashed = False
    delay = 3  # seconds
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_distance = 100
    while True:
        # Thực hiện script để cuộn xuống thêm một khoảng cách cụ thể
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Wait for a short time to let the new content load
    time.sleep(2)  # Adjust the time according to your needs
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        print(f'{Fore.YELLOW}Page is ready!{Style.RESET_ALL}')
    except TimeoutException:
        print(f'{Fore.YELLOW}Page is ready!{Style.RESET_ALL}')

    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, 'html.parser')
    # print(soup)
    if hashed:
        videoList = soup.find("div", {"data-e2e": "challenge-item-list"})
        allVids = videoList.findAll("div", {"class": "tiktok-c83ctf-DivWrapper e1cg0wnj1"})
    else:
        videoList = soup.find("div", {"mode": "search-video-list"})
        allVids = videoList.findAll("div", {"class": "tiktok-16ou6xi-DivTagCardDesc eih2qak1"})

    # allVids = videoList.findAll("div", {"class": "tiktok-1soki6-DivItemContainerForSearch e19c29qe9"})
    urls = [vid.find("a")['href'] for vid in allVids]
    print(
        f'\nFound total of {Fore.RED}{len(urls)}{Style.RESET_ALL} videos on this keyword.\n{Fore.GREEN}Start scraping{Style.RESET_ALL}')

    for url in urls:
        print(f'\n{Fore.BLUE}Scraping video post ID:{Style.RESET_ALL} {url.split("/")[-1]}')

        # url = "https://www.tiktok.com/@bolsonaromessiasjair/video/7120216471208283397"
        df_posts = pd.DataFrame(
            columns=['posturl', 'browseUser', 'postcontent', 'views', 'likes', 'saves', 'shares', 'commentcounts'])
        post_content = post_scraper.scrape_post_content(url)

        #craw cmt from the url
        comment_scrapper.scrapper_comment(keyword, url)

        df_profile = pd.DataFrame(
            columns=['Userlink', 'UserName', 'UserFollowing', 'UserFollowers', 'UserLikes'])

        views, profile = profile_scraper.scrape_profile_info(post_content['browseUser'], url)
        post_content['views'] = views

        df_profile.loc[len(df_profile.index)] = profile
        df_posts.loc[len(df_posts.index)] = post_content

        save_csv(df_profile, f'owner_post_{keyword}.csv')
        save_csv(df_posts, f'posts_list_{keyword}.csv')

    posts_clean = pd.read_csv(os.path.join('./data/craw', f'posts_list_{keyword}.csv'),
                              on_bad_lines='skip').drop_duplicates()  # Open file
    posts_clean.to_csv(os.path.join('./data/craw', f'posts_list_{keyword}.csv'), encoding='utf-8-sig', index=False)

    # return json.dumps(dict, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    configure()
    ## Clear screen and instructions on terminal window
    if 'windows' in platform.system().lower():
        os.system('cls')
    else:
        os.system('clear')

    keyword = input(f'{Fore.GREEN}Enter keyword or a hashtag to search and press enter:{Style.RESET_ALL} ')

    driver = load_driver()
    driver.maximize_window()

    print(f'{Fore.GREEN}Follow the bellow instruction{Style.RESET_ALL}\n')
    print('  1. Do not close this terminal window')
    # print('  2. A browser screen will open with TikTok login')
    json_object = main(driver, keyword)
