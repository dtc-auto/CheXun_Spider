# coding:utf-8
from scrapy import cmdline
import CheXun_Spider.settings

def main():
    Spider_name = CheXun_Spider.settings.STAR_SPIDER_NAME
    star_spider = "scrapy crawl %s" %(Spider_name)
    cmdline.execute(star_spider.split())

if 1:
    main()