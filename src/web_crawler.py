import requests
from bs4 import BeautifulSoup as bs
import csv
import time
import re

cookie = 'study_postinvite_radio=1314; crisp-client%2Fsession%2F327214ac-6a2a-4c15-9e06-98c552cd5814=session_38ebc3fc-9d34-4063-8651-9caae550f8ef; 4Oaf_61d6_cookie_hash=ed033daec34b86851baf6a9ed134c1d4; 4Oaf_61d6_lastvisit=1597998145; 4Oaf_61d6_lastact=1598003602%09home.php%09spacecp; 4Oaf_61d6_ulastactivity=1598003601%7C0; 4Oaf_61d6_lastcheckfeed=469652%7C1598001754; 4Oaf_61d6_lip=199.19.110.43%2C1598001754; 4Oaf_61d6_member_login_status=1; 4Oaf_61d6_nofavfid=1; _ga=GA1.2.263377310.1598002218; _gid=GA1.2.1576428336.1598002218; 4Oaf_61d6_atarget=1; 4Oaf_61d6_forum_lastvisit=D_82_1598003601; 4Oaf_61d6_visitedfid=82; 4Oaf_61d6_sendmail=1; 4Oaf_61d6_checkpm=1'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
base_url = 'https://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=82&sortid=164&searchoption[3001][value]=1&searchoption[3001][type]=radio&searchoption[3002][value]=1&searchoption[3002][type]=radio&sortid=164&filter=sortid&orderby=dateline'


# login with cookies
def login(url):
    headers = {
        'User-Agent': user_agent,
        # How to get cookies?
        # Login, goto the page you want to use and run 'document.cookie' in console
        'Cookie': cookie,
    }
    session = requests.Session()
    response = session.get(url, headers=headers)
    response.text.encode('utf-8')
    if response.status_code != 200:
        print('WARNING: Login Failed!!')
    return response


def get_html_info(url):
    response = login(url)
    if response.status_code == 200:
        return response.text
    else:
        return response.status_code


def get_cur_page(pager):
    cur_page_data = pager.find('strong')
    cur_page = ''
    for page in cur_page_data:
        cur_page = page
    return cur_page


def get_max_page(pager):
    max_page_data = pager.find('a', class_='last')
    max_page = ''
    for page in max_page_data:
        page = page.replace('... ', '')
        max_page = page
    return max_page


def get_pager(soup):
    pager = soup.find('div', class_='pg')
    cur_page = get_cur_page(pager)
    next_page = str(int(cur_page) + 1)
    max_page = get_max_page(pager)
    return [cur_page, next_page, max_page]


def get_page_data(url):
    raw_html_info = get_html_info(url)
    if isinstance(raw_html_info, str):
        soup = bs(raw_html_info, 'html.parser')
        pager = get_pager(soup)


def main():
    url = base_url + '&page=1'
    get_page_data(url)


if __name__ == '__main__':
    main()
