#!/usr/bin/env python

# os
import os
# requests
import requests

# lxml
from lxml import etree

# bs4
from bs4 import BeautifulSoup


# url parse
from urllib.parse import urlparse

# subprocess
import subprocess



def get_html(url):
    r = requests.get(url)
    return r.text

def parse_xpath(html, xpath):
    root = etree.HTML(html)
    result = root.xpath(xpath)
    return result

if __name__ == "__main__":
    # read news url array from news_source.txt
    news_source = open('news_source.txt').read().split('\n')
    xpaths = {
        'www.ettoday.net': '//*[@id="society"]/div[4]/div[2]/div[9]/div/div/div[1]/div[1]/article/div',
        'www.chinatimes.com': '//*[@id="page-top"]/div/div[2]/div/div/article/div/div[1]/div[2]/div[2]/div[2]',
        'udn.com': '/html/body/main/div/section[2]/section/article/div/section[1]',
        'news.ltn.com.tw': '//*[@id="ltnRWD"]/div[10]/section/div[4]/div[2]',
        'finance.ettoday.net': '//*[@id="finance"]/div[3]/div[2]/div[7]/div/div[1]/div[1]/div[2]/div[4]',
        'ctee.com.tw': '//*[@id="post--24779"]/div[3]'
    }
    css_selector = {
        'www.ettoday.net': '#society > div.wrapper_box > div.wrapper > div.container_box > div > div > div.c1 > div.part_area_1 > article > div > div.story',
        'www.chinatimes.com': '#page-top > div > div:nth-child(2) > div > div > article > div > div:nth-child(2) > div.row > div.col-xl-11 > div.article-body',
        'udn.com': 'body > main > div > section.wrapper-left.main-content__wrapper > section > article > div > section.article-content__editor',
        'news.ltn.com.tw': '#ltnRWD > div.content > section > div:nth-child(16) > div.text.boxTitle.boxText',
        'finance.ettoday.net': '#finance > div.wrapper_box > div.wrapper > div.container_box > div > div.r1.clearfix > div.c1 > div.subject_article > div.story',
        'ctee.com.tw': 'div.entry-content.clearfix.single-post-content'
    }
    # check output.csv exist or not, if not create it with default header
    if not os.path.exists('output.csv'):
        with open('output.csv', 'w') as f:
            f.write('新聞連結,犯罪人與公司,刑責,刑責進度,摘要\n')
    for news_url in news_source:
        try:
            print('URL', news_url)
            # get url host, not hostname
            host = urlparse(news_url).netloc
            # get html
            html = get_html(news_url)
            # parse html
            soup = BeautifulSoup(html, 'html.parser')
            sel = css_selector[host]
            news_html = soup.select(sel)
            news_content = news_html[0].text
            # pass arguments to main.sh
            
            process = subprocess.Popen(['./main.sh', news_url], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Pass the news_content to main.sh through the pipe
            output, error = process.communicate(input=news_content)
            print(output)
        except:
            print('Error', news_url)
            pass
        