import re
import requests
from bs4 import BeautifulSoup as bs
import xlrd
import xlwt
from xlutils.copy import copy
import time

cookie = '__cfduid=df5c329fc009c62e45bef0cfadcfb3d311598103315; 4Oaf_61d6_saltkey=GkK5JZSW; 4Oaf_61d6_lastvisit=1598099715; 4Oaf_61d6_sendmail=1; _ga=GA1.2.255742118.1598103321; _gid=GA1.2.657097761.1598103321; _gat=1; 4Oaf_61d6_cookie_hash=498d9c937b305355f346c584acd8e0bf; __gads=ID=9bbd87e9f19d5ee1:T=1598103321:S=ALNI_MYd9SMC1CGCUnFroeReshlJkv0daQ; _gat_gtag_UA_167278674_1=1; 4Oaf_61d6_lastact=1598103368%09member.php%09logging; 4Oaf_61d6_ulastactivity=1598103368%7C0; 4Oaf_61d6_auth=1edbCNcMM8nx%2BthjxqKMBwDPazTRd0Ns%2BcZU5XsoA5nl8NIhzGyL%2BJ5w08wb4voZBfgLXm1W9lLtiC1qMMMQVcQr2Vk; 4Oaf_61d6_lastcheckfeed=469652%7C1598103368; 4Oaf_61d6_checkfollow=1; 4Oaf_61d6_lip=199.19.110.43%2C1598103368'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
dir_url = 'https://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=82&sortid=164&searchoption[3001][value]=1&searchoption[3001][type]=radio&searchoption[3002][value]=1&searchoption[3002][type]=radio&sortid=164&filter=sortid&orderby=dateline'
base_url = 'https://www.1point3acres.com/bbs/'
filename = '../data/ans.xls'
sleep = False


# login with cookies
def login(url):
    headers = {
        'User-Agent': user_agent,
        # How to get cookies?
        # Chrome: F12 and goto 'Network' page, login and check the Request Header in Name='bbs/', you can get cookie in Request Header section
        # Firefox: F12 and goto 'Network' page, login and check cookie page from name='bbs/', copy all cookies. You need to reformat it first from lots of 'xx:"yy"' to 'xx=yy; xxx=yyy'
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
    cur_page = "".join(cur_page_data.contents)
    return cur_page


def get_max_page(pager):
    max_page_data = pager.find('a', class_='last')
    max_page = "".join(max_page_data.contents)
    max_page = max_page.replace('... ', '')
    return max_page


def get_pager(soup):
    pager = soup.find('div', class_='pg')
    cur_page = get_cur_page(pager)
    next_page = str(int(cur_page) + 1)
    max_page = get_max_page(pager)
    page_info = [['当前页', '下一页', '最大页'], [cur_page, next_page, max_page]]
    return page_info


def get_posts(soup):
    posts_data = soup.find_all('tbody', id=re.compile('^normalthread_'))
    posts_info = [['标题', '帖子地址', '作者', '作者主页地址']]
    for post in posts_data:
        post_data = post.find('a', class_='s xst', href=True)
        post_title = "".join(post_data.contents)
        post_url = base_url + post_data['href']
        post_author = post.find('cite')
        if post_author.find('a', href=True) is None:
            post_author_name = '地里的匿名用户'
            post_author_url = ''
        else:
            post_author = post_author.find('a', href=True)
            post_author_name = "".join(post_author.contents)
            post_author_url = base_url + post_author['href']
        posts_info.append([post_title, post_url, post_author_name, post_author_url])
    return posts_info


def get_page_data(url):
    raw_html_info = get_html_info(url)
    if isinstance(raw_html_info, str):
        soup = bs(raw_html_info, 'html.parser')
        pager = get_pager(soup)
        posts = get_posts(soup)
        return pager, posts


def get_index(apply_info, th):
    return apply_info.index(th)


def get_apply_data(post_url):
    raw_html_info = get_html_info(post_url)
    if isinstance(raw_html_info, str):
        soup = bs(raw_html_info, 'html.parser')
        apply_table = soup.find('table', class_='cgtl mbm')
        apply_table = apply_table.find('tbody')
        apply_table = apply_table.find_all('tr')
        apply_info = ['申入学年度:', '入学学期:', '专业:', '具体项目名称:', '学位:', '全奖/自费:', '提交时间:', '申请结果:',
                      '学校名称:', '通知时间:', '本科学校名称:', '本科学校档次:', '本科专业:', '本科成绩和算法，排名:',
                      '研究生学校名称:', '研究生学校档次:', '研究生专业:', '研究生成绩和算法，排名:', 'T单项和总分:',
                      'G单项和总分:', 'sub专业和分数:', '背景的其他说明（如牛推等）:', '个人其他信息:', '结果学校国家、地区:', '查到status的方式:', '备注:']
        apply_line = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        mark = soup.find('td', class_='t_f')
        mark = "".join(mark.strings)
        mark = mark.strip()
        start = mark.find('\n\n')
        end = mark.find('\n\n', start + 2)
        mark = mark[start + 2:end]
        index = get_index(apply_info, '备注:')
        apply_line[index] = mark
        for tr in apply_table:
            th = tr.find('th')
            th = "".join(th.contents)
            index = get_index(apply_info, th)

            td = tr.find('td')
            if td.find('a', onclick=True):
                td = td.find('a', onclick=True)
                td = td['onclick']
                start = td.find('forum.php?')
                end = td.find(', ')
                td = td[start:end - 1]
                td = base_url + td
                raw_html_info = get_html_info(td)
                if isinstance(raw_html_info, str):
                    soup = bs(raw_html_info, 'html.parser')
                    td = soup.find('root')
                    td = "".join(td.contents)
                    apply_line[index] = td
            elif td.find('a', href=True):
                td = td.find('a', href=True)
                td = td['href']
                apply_line[index] = td
            else:
                td = "".join(td.contents)
                apply_line[index] = td

        return apply_line


def create_xls(filename):
    new_line = ['标题:', '帖子地址:', '作者:', '作者主页地址:', '申入学年度:', '入学学期:', '专业:', '具体项目名称:', '学位:',
                '全奖/自费:', '提交时间:', '申请结果:', '学校名称:', '通知时间:', '本科学校名称:', '本科学校档次:',
                '本科专业:', '本科成绩和算法，排名:', '研究生学校名称:', '研究生学校档次:', '研究生专业:', '研究生成绩和算法，排名:',
                'T单项和总分:', 'G单项和总分:', 'sub专业和分数:', '背景的其他说明（如牛推等）:', '个人其他信息:', '结果学校国家、地区:', 
                '查到status的方式:', '备注:']
    wb = xlwt.Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    for i in range(len(new_line)):
        sheet1.write(0, i, new_line[i])
    wb.save(filename)
    print('*INFO: xls file has created.')


def write_xls_append(filename, new_line):
    workbook = xlrd.open_workbook(filename)
    sheets = workbook.sheet_names()
    worksheet = workbook.sheet_by_name(sheets[0])
    exist_rows = worksheet.nrows
    new_workbook = copy(workbook)
    new_worksheet = new_workbook.get_sheet(0)
    for i in range(len(new_line)):
        new_worksheet.write(exist_rows, i, new_line[i])
    new_workbook.save(filename)
    print('INFO: Append new line. CurLine:' + str(exist_rows))


def main():
    cur_page = 0
    next_page = cur_page + 1
    max_page = 65535
    create_xls(filename)
    while cur_page < max_page:
        page = get_page_data(dir_url + '&page=' + str(next_page))
        cur_page = int(page[0][1][0])
        next_page = int(page[0][1][1])
        max_page = int(page[0][1][2])
        for post in page[1][1:]:
            apply_info = get_apply_data(post[1])
            ans = (post + apply_info)
            write_xls_append(filename, ans)
            if sleep == True:
                time.sleep(1)
        print('*INFO: Append new page. CurPage:' + str(cur_page))
        if sleep == True:
            time.sleep(5)
    print('************************************************************')
    print('*INFO: Web Crawler has done crawling. CurPage:' + str(cur_page), 'MaxPage:' + str(max_page))


if __name__ == '__main__':
    main()
