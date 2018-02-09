# -*- coding: utf-8 -*-
import scrapy
import re
import json
import pymssql
import pandas as pd
from CheXun_Spider.settings import *
from CheXun_Spider.items import ChexunSpiderCompaniesItem
class UrlSpiderSpider(scrapy.Spider):

    start_urls = ['http://auto.chexun.com/search-a0-b0-c0-d0-e0-f0-g0-h0-i0:0.html']
    name = "Companies_Spider"

    def parse(self, response):

        self.server = DATABASE_SERVER_NAME
        self.user = DATABASE_USER_NAME
        self.password = DATABASE_USER_PASSWORD
        self.database = DATABASE_NAME
        self.host = DATABASE_HOST
        self.conn = pymssql.connect(user=self.user,
                                    password=self.password,
                                    host=self.host,
                                    database=self.database)

        sql = """SELECT COMPANY_ID FROM [stg].[CONFIG_COMPANIES_2018_01_30]"""
        url_list_df = pd.read_sql_query(sql, self.conn)
        sql_id = url_list_df.values.tolist()
        self.sql_id_list = []
        for id in sql_id:
            self.sql_id_list.append(id[0])

        pattern_js = re.compile("\"companyMap\":(.+?)\,\"seriesMap\"")
        js_list = re.findall(pattern_js, response.body.decode('utf-8'))
        js_item = js_list[0]
        str_json = json.loads(js_item)
        js_item = dict(str_json)
        #print js_item
        for each in self.dict_flatlist(js_item, i=1):
            yield each


    def dict_flatlist(self, d, i):
        item = ChexunSpiderCompaniesItem()
        #print(d)
        for x in d.keys():
            if type(d[x]) == list:
                for dit in d[x]:
                    item['company_id'] = str(dit['companyId'])
                    item['company_name_cn'] = dit['companyName']
                    item['company_name_en'] = dit['englishName']
                    item['brand_id'] = x
                    # 增量判断 表中是否有重复数据 （表中serie_id唯一）
                    key = str(item['company_id'])
                    if key not in self.sql_id_list:
                        yield item

