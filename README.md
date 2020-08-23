# 1p3aMSCSAdminReport

[![LICENSE](https://img.shields.io/badge/License-GPL--2.0-green.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-v3.8.2-blue.svg?style=flat-square)](https://github.com/DolorHunter/1p3aMSCSAdminReport/releases)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-v4.9.1-yellow.svg?style=flat-square)](https://github.com/DolorHunter/1p3aMSCSAdminReport/releases)
[![xlutils](https://img.shields.io/badge/xlutils-v2.0.0-%23373737.svg?style=flat-square)](https://github.com/DolorHunter/OS_DR-PR/releases)
[![xlrd](https://img.shields.io/badge/xlrd-v1.2-lightgrey.svg?style=flat-square)](https://github.com/DolorHunter/1p3aMSCSAdminReport/releases)
[![xlwt](https://img.shields.io/badge/xlwt-v1.3-lightgrey.svg?style=flat-square)](https://github.com/DolorHunter/1p3aMSCSAdminReport/releases)

爬虫搜索 一亩三分地(1p3a) 研究生CS专业录取情况结果, 可获取隐藏内容.

__[依赖](#依赖)__ | __[如何使用](#如何使用)__ | __[警告](#警告)__

## 依赖

Python 3

```plain
$ pip install regex, requests, BeautifulSoup4, xlutils
```

## 如何使用

修改 /src/web_crawler.py 下的 `cookie` 和 `dir_url`(如果你想使用MSCS外的条件).

- 怎么获得Cookie:
  - Chrome: F12进入网络(Network)分页, 重新登录论坛, 查看名为 bbs/ 的请求的请求头(Request Header), 请求头内的 Cookie 即为你的 cookie, 替换全局变量 cookie 即可.
  - Firefox: F12进入网络(Network)分页, 重新登录论坛, 查看名为 bbs/ 的请求, 选择请求头(Request Header)分页, 复制所有的 Cookie 并调整格式. **xx:"yy" xxx:"yyy"** => **xx=yy; xxx=yyy**

- 怎么获得 dir_url:
  - 进入 [论坛›留学申请›录取汇报：研究生](https://www.1point3acres.com/bbs/forum-82-1.html)
  - (可选)调整筛选条件/过滤器
  - 进入非第一页的页面, 获得一个以 **&page=n** 结尾的链接
  - 去掉此结尾并替换全局变量 dir_url 即可.

## 警告

爬虫可能会触发网站的 bot 检测. 如果不幸触发请手动进入 https://www.1point3acres.com/bbs/ 进行 reCAPTCHA验证. 在未使用 sleep 的情况下大约爬取一两百个帖子会触发一次, 使用了 sleep 后似乎也不会有所提升? 因此默认 sleep 参数为 False.
