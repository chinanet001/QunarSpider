#!/usr/bin/python
# -*- coding: utf-8 -*-

''' 去哪儿网成都酒店信息爬虫 '''

import time

from lxml import etree
from pymongo import MongoClient
from selenium import webdriver

mongo_conn = MongoClient('127.0.0.1', 27017, connect=False)
db = mongo_conn.qunar
curse = db.hotel

url = 'http://hotel.qunar.com/city/chengdu/#fromDate=2018-09-15&cityurl=chengdu&from=qunarHotel&toDate=2018-09-16'


def schedule(page):
    '''  主调度程序 '''
    browser = webdriver.Chrome()
    browser.get(url)
    while page:
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        page_source = browser.page_source
        parse_info(page_source)
        time.sleep(2)
        next_button = browser.find_element_by_xpath('//li[@class="item next "][1]')
        next_button.click()
        page -= 1
    browser.close()


def parse_info(page):
    ''' 解析酒店信息 '''
    html = etree.HTML(page)
    divs = html.xpath('//*[@id="jxContentPanel"]//div[@class="clrfix"]')
    for div in divs:
        img = div.xpath('.//div[@class="item_hotel_photo js-photo"]/a/img/@src')
        name = div.xpath('.//span[@class="hotel_item"]/a[1]/text()')
        level = div.xpath('.//span[@class="hotel_item"]/em/text()')
        addr = div.xpath('.//p[@class="address"]/em/text()')
        rate = div.xpath('.//div[@class="level levelmargin"]//strong/text()')
        dianpin_num = div.xpath('.//div[@class="level levelmargin"]//a[2]/text()')
        price = div.xpath('.//div[@class="hotel_price"]//a[1]/b/text()')
        item = {
            'img'        : img,
            'name'       : name,
            'level'      : level,
            'addr'       : addr,
            'rate'       : rate,
            'dianpin_num': dianpin_num,
            'price'      : price
        }
        curse.insert(item)


# todo 替换成无头chrome

def main():
    schedule(3)


if __name__ == '__main__':
    main()
