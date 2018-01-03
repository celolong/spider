# coding=utf-8
"""
author:cello
"""

from selenium import webdriver
from lxml import etree

driver = webdriver.PhantomJS()
url = 'http://music.163.com/#/playlist?id=724445066'
driver.get(url)
print(driver)
el_iframe = driver.find_element_by_xpath('//*[@name="contentFrame"]')
driver.switch_to.frame(el_iframe)
html = driver.page_source
print(html)
el =driver.find_elements_by_xpath('//div[@id="song-list-pre-cache"]/div/div/table/tbody/tr')
# print(el[0].find_elements_by_xpath('./tbody'))
print(len(el))


