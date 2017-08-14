# -*- coding: utf-8 -*-
import scrapy
import re
import json
import pymssql
import pandas as pd
from CheXun_Spider.settings import *
from CheXun_Spider.items import ChexunSpiderItem

class UrlSpiderSpider(scrapy.Spider):

    start_urls = ['http://auto.chexun.com/search-a0-b0-c0-d0-e0-f0-g0-h0-i0:0.html']
    name = "URL_Spider"

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

        sql = """SELECT SERIE_ID FROM [stg].[CONFIG_SERIES]"""
        url_list_df = pd.read_sql_query(sql, self.conn)
        sql_id = url_list_df.values.tolist()
        self.sql_id_list = []
        for id in sql_id:
            self.sql_id_list.append(id[0])

        pattern_js = re.compile("\"seriesMap\":(.+?)};")
        js_list = re.findall(pattern_js, response.body)
        js_item = js_list[0]
        str_json = json.loads(js_item)
        js_item = dict(str_json)
        #print js_item
        for each in self.dict_flatlist(js_item, i=1):
            yield each

    def dict_flatlist(self, d, i):
        item = ChexunSpiderItem()
        #print(d)
        for x in d.keys():
            if type(d[x]) == dict:
                self.dict_flatlist(d[x])
            if type(d[x]) == list:
                for dit in d[x]:
                    for key in dit:
                        # l.append(dit[key])
                        if key.encode("utf8") == 'seriesId':
                            item['serie_id'] = dit[key]
                        if key.encode("utf8") == 'companyId':
                            item['company_id'] = dit[key]
                        if key.encode("utf8") == 'brandId':
                            item['brand_id'] = dit[key]
                        if key.encode("utf8") == 'seriesName':
                            item['serie_name_cn'] = dit[key]
                        if key.encode("utf8") == 'englishName':
                            item['serie_name_en'] = dit[key]
                            en_name = dit[key].encode("utf8")
                            ser_url = "http://auto.chexun.com/%s/data" % (en_name)
                            item['serie_url'] = ser_url


                        # 增量判断 表中是否有重复数据（表中serie_id唯一）
                            key = str(item['serie_id']).decode('gb2312')
                            if key not in self.sql_id_list:
                                item['serie_id'] = str(item['serie_id'])
                                yield item

            else:

                if key.encode("utf8") == 'seriesId':
                    item['serie_id'] = dit[key]
                if key.encode("utf8") == 'seriesName':
                    item['serie_name_cn'] = dit[key].encode('utf-8')
                if key.encode("utf8") == 'englishName':
                    item['serie_name_en'] = dit[key].encode('utf-8')
                    en_name = dit[key].encode("utf8")
                    ser_url = "http://auto.chexun.com/%s/data" % (en_name)
                    item['serie_url'] = ser_url
                if key.encode("utf8") == 'brandId':
                    item['brand_id'] = dit[key]
                if key.encode("utf8") == 'companyId':
                    item['company_id'] = dit[key]
                    # 增量判断 表中是否有重复数据（表中serie_id唯一）
                    key = str(item['serie_id']).decode('gb2312')
                    if key not in self.sql_id_list:
                        item['serie_id'] = str(item['serie_id'])
                        yield item
