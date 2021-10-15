#!/usr/bin/env python
# _*_coding:utf-8 _*_
#@Time    :2019/6/8 0008 下午 11:00
#@Author  :喜欢二福的沧月君（necydcy@gmail.com）
#@FileName: CSDN.py

#@Software: PyCharm

import requests
from pyquery import PyQuery as pq

def find_html_content(url):
    headers = {
                'User-Agent': 'Chrome/52.0.2743.116 Safari/537.36'
            }
    html = requests.get(url,headers=headers).text
    return html
def read_and_wiriteblog(html):
    doc = pq(html)

    article = doc('.blog-content-box')
    #文章标题
    title = article('.title-article').text()

    content = article('.article_content')

    try:
        dir = "F:/DXW/"+title+'.txt'
        with open(dir, 'a', encoding='utf-8') as file:
            file.write(title+'\n'+content.text())
    except Exception:
        print("保存失败")


def geturls(url):
    content = find_html_content(url)
    doc = pq(content)
    urls = doc('.article-list .content a')
    return urls

def main(offset):
    url = 'https://blog.csdn.net/weixin_41261833/article/details/108050152/' + str(offset)
    urls = geturls(url)
    for a in urls.items():
        a_url = a.attr('href')
        print(a_url)
        html = find_html_content(a_url)
        read_and_wiriteblog(html)
if __name__ == '__main__':
    for i in range(1):
        print(i)
        main(offset = i+1)