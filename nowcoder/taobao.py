#coding=utf-8

# 测试运行环境: ubuntu 14.04  python 2.7.6 chrome
# 需要安装 selenim chromedriver

from selenium import webdriver
from selenium.webdriver.common.by import By

import sys

GBK = 'gbk'

def logToFile(tag, msg):
    logFile = open('log', 'w')
    out = tag + '--\n' + msg
    logFile.write(out)

def log(tag, msg):
    print tag, ' -- '
    print msg

def defLog(msg):
    log('out', msg)

# 保存零食信息
class Item:
    def __init__(self):
        self.CODE = 'utf-8'

# 输出内容到markdown文件中
class MarkdownWriter:
    def __init__(self, name='out.md'):
        mdFile = open(name, 'w')
        self.mdFile = mdFile

    def writeContent(self, content):
        self.mdFile.write(content)

    def writeItems(self, title, items):
        # 组装markdown格式
        content = '### ' + title + '  \n'
        for item in items:
            content += '#### ' + item.title + '  \n'
            content += '![img](' + item.img + ')  \n'
            content += '[goto](' + item.url + ')  \n'
            content += 'money: ' + item.money + '  \n'
            content += 'store: ' + item.store + '  \n'
            content += '\n\n'

        self.mdFile.write(content)


class TaoBaoSpider: 
    def __init__(self):
        driver = webdriver.Chrome()
        self.driver = driver

    def getUrl(self, url):
        print 'start get ...'
        # 通过chrome加载url包括js脚本
        self.driver.get(url)
        print 'get finished ...'

    def getHtmlWithJs(self):
        return self.driver.page_source

    def getElements(self):
        print 'get item ...'
        els = self.driver.find_elements(By.CSS_SELECTOR, "li[class=' item  item-border'")
        return els

    def getContent(self, element):
        item = Item()
        # 从获取的html页面中获取需要的信息并封装到item类中
        item.img = element.find_element_by_tag_name('img').get_attribute('src')
        item.money = element.find_element(By.CSS_SELECTOR, "div[class='price child-component clearfix'").find_element_by_tag_name('strong').text
        titleElement = element.find_element(By.CSS_SELECTOR, "div[class='title child-component'").find_element_by_class_name('J_AtpLog')
        item.title = titleElement.text
        item.url = titleElement.get_attribute('href')
        item.store = element.find_element(By.CSS_SELECTOR, "div[class='seller child-component clearfix'").find_element_by_tag_name('a').text
        return item

    def start(self, url):
        self.url = url
        self.getUrl(url)
        els = self.getElements()
        items = []
        for e in els:
            item = self.getContent(e)
            items.append(item)

        return items


def main():
    # 设置下编码
    reload(sys)
    sys.setdefaultencoding('utf-8')

    url = 'https://world.taobao.com/search/search.htm?_ksTS=1478358034370_312&spm=a21bp.7806943.20151106.1&search_type=0&_input_charset=utf-8&navigator=all&json=on&q=%E5%A5%B3%E6%9C%8B%E5%8F%8B%20%E9%9B%B6%E9%A3%9F&cna=Eg9NDplivkkCAXuCB323%2Fsy9&callback=__jsonp_cb&abtest=_AB-LR517-LR854-LR895-PR517-PR854-PR895'
    # 爬虫运行
    spider = TaoBaoSpider()
    items = spider.start(url)
    # 输出到markdown文件中
    writer = MarkdownWriter('taobao.md')
    writer.writeItems('零食列表', items)

main()
