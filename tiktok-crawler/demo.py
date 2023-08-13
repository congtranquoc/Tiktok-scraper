# for (User,Link,Name,Content,Likes,Replies) in zip(scraped.commentUser,scraped.commentUserLink,scraped.commentUserName,scraped.commentContent,scraped.commentLikes,commentReplies):
#     print(f'     Scraping user {Fore.BLUE}{User}{Style.RESET_ALL} public information')
#
#     # driver.get('https://www.tiktok.com/@tatianemorais211')
#     driver.get(Link)
#     driver.implicitly_wait(.2) # seconds
#
#     pageSource = driver.page_source
#     soup = BeautifulSoup(pageSource, 'html.parser')
#
#     try:
#         following = soup.find("strong", {"title" : "Following"}).text
#     except:
#         following = 0
#     try:
#         likes = soup.find("strong", {"title" : "Likes"}).text
#     except:
#         likes = 0
#     try:
#         followers = soup.find("strong", {"title" : "Followers"}).text
#     except:
#         followers = 0
#
#     commDict[User] = {'Userlink':Link, 'UserName':Name, 'UserFollowing':following, 'UserFollowers':followers, 'UserLikes':likes, 'ReplyContent':Content, 'Replylikes':Likes, 'replies':Replies}
#     df_user.loc[len(df_user.index)] = {'Userlink':Link, 'originalPost':url.split('/')[-1], 'UserName':Name, 'UserFollowing':following, 'UserFollowers':followers, 'UserLikes':likes, 'ReplyContent':Content, 'Replylikes':Likes, 'replies':Replies}
#
#     save_csv(df_user,f'user_list_{keyword}.csv')

## BUILD CSV for USERS List
# if os.path.exists(f'results/user_list_{keyword}.csv'):

#
# if os.path.exists(os.path.join('results', f'user_list_{keyword}.csv')):
#     saved_df = pd.read_csv(os.path.join('results', f'user_list_{keyword}.csv'), on_bad_lines='skip').drop_duplicates() #Open file
#     frames = [df, saved_df]
#     df_final = pd.concat(frames)
#     df_final.to_csv(os.path.join('results', f'user_list_{keyword}.csv'), encoding='utf-8-sig',index=False)
# else:
#     df_user.to_csv(os.path.join('results', f'user_list_{keyword}.csv'), encoding='utf-8-sig',index=False)


## BUILD CSV for POSTS List

# # if os.path.exists(f'results/posts_list_{keyword}.csv'):
# if os.path.exists(os.path.join('results', f'posts_list_{keyword}.csv')):
#     dfdp = pd.read_csv(os.path.join('results', f'posts_list_{keyword}.csv'), on_bad_lines='skip').drop_duplicates() #Open file
#     frames = [df_posts, dfdp]
#     dfp = pd.concat(frames)
#     dfp.to_csv(os.path.join('results', f'posts_list_{keyword}.csv'), encoding='utf-8-sig',index=False)
# else:
#     df_posts.to_csv(os.path.join('results', f'posts_list_{keyword}.csv'), encoding='utf-8-sig',index=False)


# driver.get("https://www.tiktok.com")
# time.sleep(.2)
#
# login_btn = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,".//button[@data-e2e='top-login-button']")))
# login_btn.click()
# user_login = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,"//*[contains(text(), 'Use phone / email / username')]")))
# user_login.click()
# username = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,"//*[contains(text(), 'Log in with email or username')]")))
# username.click()
# user = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,".//*[@name='username']")))
# user.send_keys(os.getenv('user'))
# time.sleep(.2)
# password = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,".//*[@type='password']")))
# password.send_keys(os.getenv('pwd'))
# time.sleep(.2)
# login = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,".//button[@data-e2e='login-button']")))
# login.click()
#
# print(f'  3. {Fore.RED}Start runing scraper setup - If asked, perform human authentication{Style.RESET_ALL}')
#
# time.sleep(10)

# loged = 'False'
# while not loged:
#     try:
#         WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,"//*[contains(text(), 'Login Successful')]")))
#         loged = True
#     except:
#         loged = False
# print('\nThe only next step will be to add your search criteria for us to start scraping')
