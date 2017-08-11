# -*- coding: utf-8 -*-
import scrapy
import re
import json
import pymssql
import pandas as pd
from CheXun_Spider.settings import *
from CheXun_Spider.items import ChexunSpiderBrandItem

class UrlSpiderSpider(scrapy.Spider):

    start_urls = ['http://auto.chexun.com/search-a0-b0-c0-d0-e0-f0-g0-h0-i0:0.html']
    name = "Brand_Spider"

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

        sql = """SELECT BRAND_ID FROM [stg].[CONFIG_BRANDS]"""
        url_list_df = pd.read_sql_query(sql, self.conn)
        sql_id = url_list_df.values.tolist()
        self.sql_id_list = []
        for id in sql_id:
            self.sql_id_list.append(id[0])

        pattern_js = re.compile("\"brandMap\":(.+?)\,\"companyMap\"")
        js_list = re.findall(pattern_js, response.body)
        js_item = js_list[0]
        str_json = json.loads(js_item)
        js_item = dict(str_json)
        #print js_item
        for each in self.dict_flatlist(js_item, i=1):
            yield each

    def dict_flatlist(self, d, i):
        item = ChexunSpiderBrandItem()
        #print(d)
        for x in d.keys():
            if type(d[x]) == list:
                for dit in d[x]:
                    for key in dit:
                        # l.append(dit[key])
                        if key.encode("utf8") == 'englishName':
                            item['brand_name_en'] = dit[key]
                        if key.encode("utf8") == 'brandName':
                            item['brand_name_cn'] = dit[key]
                        if key.encode("utf8") == 'brandId':
                            item['brand_id'] = dit[key]
                            item['brand_id'] = str(item['brand_id'])
                            # 增量判断 表中是否有重复数据（表中serie_id唯一）
                            key = str(item['brand_id']).decode('gb2312')
                            if key not in self.sql_id_list:
                                yield item