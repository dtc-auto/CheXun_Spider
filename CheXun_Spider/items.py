# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChexunSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    serie_id = scrapy.Field()
    serie_name_cn = scrapy.Field()
    serie_name_en = scrapy.Field()
    serie_url = scrapy.Field()
    brand_id = scrapy.Field()
    company_id = scrapy.Field()
    create_time = scrapy.Field()
    last_update_time = scrapy.Field()

class ChexunSpiderBrandItem(scrapy.Item):
    brand_name_en = scrapy.Field()
    brand_name_cn = scrapy.Field()
    brand_id = scrapy.Field()
    create_time = scrapy.Field()
    last_update_time = scrapy.Field()

class ChexunSpiderCompaniesItem(scrapy.Item):
    company_id = scrapy.Field()
    company_name_cn = scrapy.Field()
    company_name_en = scrapy.Field()
    brand_id = scrapy.Field()
    create_time = scrapy.Field()
    last_update_time = scrapy.Field()

class ChexunSpiderConfiguration(scrapy.Item):
    series_id = scrapy.Field()
    spec_id = scrapy.Field()
    para_name = scrapy.Field()
    para_value = scrapy.Field()
    create_time = scrapy.Field()
    last_update_time = scrapy.Field()

class ChexunSpiderColumn(scrapy.Item):
    para_id = scrapy.Field()
    para_name = scrapy.Field()
    type_name = scrapy.Field()
    type_id = scrapy.Field()
