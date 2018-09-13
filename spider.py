import time

from lxml import etree

from selenium import webdriver

url = 'http://hotel.qunar.com/city/chengdu/#fromDate=2018-09-15&cityurl=chengdu&from=qunarHotel&toDate=2018-09-16'


def get_page_source(url):
    browser = webdriver.Chrome()
    browser.get(url)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    page_text = browser.page_source
    return page_text


def parse_info(page):
    html = etree.HTML(page)

    divs = html.xpath('//*[@id="jxContentPanel"]//div[@class="clrfix"]')

    for div in divs:
        name = div.xpath('.//span[@class="hotel_item"]/a[1]/text()')
        print(name)


page = get_page_source(url)
infos = parse_info(page)
