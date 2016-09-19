# -*- coding: utf-8 -*-

import time
import requests
import re
from lxml import etree
from public.mysqlpooldao import MysqlDao
from public.headers import Headers


def get_category():
    mysql_dao = MysqlDao()
    sql = 'select `id`,`name`,`url` from  it_category'
    res = mysql_dao.execute(sql)
    return res


def get_myexception(cate_id, cate_url):
    headers = Headers.get_headers()
    req = requests.get(cate_url, headers=headers, timeout=30)
    if req.status_code == 200:
        html = req.content
        selector = etree.HTML(html)
        last_pages = selector.xpath('//div[@class="c_p_s"]/ul/font/li[last()]/a/@href')
        if len(last_pages) > 0:
            last_page = last_pages[0]
            match_obj = re.match(r'index_(.*?).html', last_page, re.M | re.I)
            page_num = int(match_obj.group(1))
            mysql_dao = MysqlDao()
            while True:
                if page_num <= 0:
                    break
                list_url = cate_url + 'index_%s.html' % page_num
                headers = Headers.get_headers()
                try:
                    print(list_url)
                    req = requests.get(list_url, headers=headers, timeout=10)
                    if req.status_code == 200:
                        html = req.content
                        selector = etree.HTML(html)
                        urls = selector.xpath('//div[@class="c_c"]/ul/li/a[1]/@href')
                        for url in urls:
                            sql = 'insert ignore into it_url(`url`,`cate`,`type`) VALUES ("%s",%s,0)' % (
                                url, cate_id)
                            mysql_dao.execute(sql)
                except:
                    print(list_url, 'timeout')
                page_num = page_num - 1


def get_cocoachina_lastpage(cate_url):
    last_page = 0
    headers = Headers.get_headers()
    req = requests.get(cate_url, headers=headers, timeout=30)
    if req.status_code == 200:
        html = req.content
        selector = etree.HTML(html)
        last_pages = selector.xpath('//div[@id="page"]/span/strong/text()')
        if len(last_pages) > 0:
            last_page = int(last_pages[0])
    return last_page


def get_url_by_cate_id(cate_id):
    url = ''
    if cate_id == 11:
        url = 'http://www.cocoachina.com/ios/list_69_%s.html'
    elif cate_id == 12:
        url = 'http://www.cocoachina.com/swift/list_73_%s.html'
    elif cate_id == 13:
        url = 'http://www.cocoachina.com/appstore/list_72_%s.html'
    elif cate_id == 14:
        url = 'http://www.cocoachina.com/design/list_77_%s.html'
    elif cate_id == 15:
        url = 'http://www.cocoachina.com/game/list_68_%s.html'
    elif cate_id == 16:
        url = 'http://www.cocoachina.com/industry/list_75_%s.html'
    elif cate_id == 17:
        url = 'http://www.cocoachina.com/apple/list_70_%s.html'
    elif cate_id == 18:
        url = 'http://www.cocoachina.com/market/list_74_%s.html'
    elif cate_id == 19:
        url = 'http://www.cocoachina.com/programmer/list_71_%s.html'
    return url


def get_cocoachina_normal(cate_id, cate_url):
    last_page = get_cocoachina_lastpage(cate_url)
    mysql_dao = MysqlDao()
    while True:
        if last_page == 0:
            break
        url = get_url_by_cate_id(int(cate_id))
        url = url % last_page
        req = requests.get(url)
        if req.status_code == 200:
            html = req.content
            selector = etree.HTML(html)
            urls = selector.xpath('//ul[@id="list_holder"]/li/div/a/@href')
            for url in urls:
                url = 'http://www.cocoachina.com' + url
                print(url)
                sql = 'insert ignore into it_url(`url`,`cate`,`type`) VALUES ("%s",%s,0)' % (
                    url, cate_id)
                mysql_dao.execute(sql)
        last_page = last_page - 1


def get_cocoachina_start_url_and_page(cate_id):
    url = ''
    if cate_id == 11:
        url = 'http://www.cocoachina.com/bbs/search_threads.php?action=essential&fid=21'
    elif cate_id == 12:
        url = 'http://www.cocoachina.com/bbs/search_threads.php?action=essential&fid=57'
    elif cate_id == 13:
        url = 'http://www.cocoachina.com/bbs/search_threads.php?action=essential&fid=14'
    elif cate_id == 14:
        url = 'http://www.cocoachina.com/bbs/search_threads.php?action=essential&fid=22'
    elif cate_id == 15:
        url = 'http://www.cocoachina.com/bbs/search_threads.php?action=essential&fid=18'
    elif cate_id == 16:
        url = 'http://www.cocoachina.com/bbs/search_threads.php?action=essential&fid=5'
    elif cate_id == 17:
        url = 'http://www.cocoachina.com/bbs/search_threads.php?action=essential&fid=14'
    elif cate_id == 18:
        url = 'http://www.cocoachina.com/bbs/search_threads.php?action=essential&fid=36'
    elif cate_id == 19:
        url = 'http://www.cocoachina.com/bbs/search_threads.php?action=essential&fid=5'
    headers = Headers.get_headers()
    array = requests.get(url, headers=headers).json()
    page = array['data']['page_total']
    print(page)
    return (url, page)


def get_cocoachina_start(cate_id, cate_url):
    (urll, page) = get_cocoachina_start_url_and_page(cate_id)
    mysql_dao = MysqlDao()
    while True:
        if page == 0:
            break
        urlll = urll + '&page=%s' % page
        headers = Headers.get_headers()
        print(urlll)
        try:
            array = requests.get(urlll, headers=headers).json()
        except:
            continue
        data = array['data']['thread_arr']
        for d in data:
            url = 'http://www.cocoachina.com/bbs/read.php?tid-%s.html' % d['tid']
            sql = 'insert ignore into it_url(`url`,`cate`,`type`) VALUES ("%s",%s,0)' % (
                url, cate_id)
            mysql_dao.execute(sql)
        page = page - 1


def get_cocoachina(cate_id, cate_url):
    get_cocoachina_normal(cate_id, cate_url)
    get_cocoachina_start(cate_id, cate_url)


def get_iteye_lastpage(url):
    last_page = 0
    headers = Headers.get_headers()
    req = requests.get(url, headers=headers, timeout=30)
    if req.status_code == 200:
        html = req.content
        selector = etree.HTML(html)
        last_urls = selector.xpath('//div[@class="pagination"]/a[last()-1]/@href')
        if len(last_urls) > 0:
            last_url = last_urls[0]
            match_obj = re.search(r'page=(.*?)&query', last_url, re.M | re.I)
            last_page = int(match_obj.group(1))
    return last_page


def get_iteye(cate_id, cate_url, cates):
    for cate in cates:
        url = 'http://www.iteye.com/search?type=blog&query=%s' % cate[1]
        page_num = get_iteye_lastpage(url)
        if page_num == 0:
            continue
        mysql_dao = MysqlDao()
        while True:
            if page_num == 0:
                break
            list_url = 'http://www.iteye.com/search?page=%s&query=%s&type=blog' % (page_num, cate[1])
            headers = Headers.get_headers()
            try:
                print(list_url)
                req = requests.get(list_url, headers=headers, timeout=10)
                if req.status_code == 200:
                    html = req.content
                    selector = etree.HTML(html)
                    urls = selector.xpath('//div[@class="content"]/h4/a[1]/@href')
                    for url in urls:
                        print(url)
                        sql = 'insert ignore into it_url(`url`,`cate`,`type`) VALUES ("%s",%s,0)' % (
                            url, cate_id)
                        mysql_dao.execute(sql)
            except:
                print(list_url, 'timeout')
            page_num = page_num - 1


def get_url(cates):
    for cate in cates:
        print(cate)
        cate_id = cate[0]
        cate_url = cate[2]
        if 'iteye' not in cate_url:
            continue
        if 'myexception' in cate_url:
            get_myexception(cate_id, cate_url)
        elif 'cocoachina' in cate_url:
            get_cocoachina(cate_id, cate_url)
        elif 'iteye' in cate_url:
            get_iteye(cate_id, cate_url, cates)


if __name__ == '__main__':
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    print(u'开始获取分类url...')
    cates = get_category()
    print(u'获取分类url完成...')
    print(u'开始获取分类下文章url...')
    get_url(cates)
    print(u'获取完成...')
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
