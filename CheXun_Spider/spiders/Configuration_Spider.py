# -*- coding: utf-8 -*-
import json
import pymssql
import re

import pandas as pd
import scrapy

from CheXun_Spider.items import ChexunSpiderConfiguration
from CheXun_Spider.settings import *
from CheXun_Spider.utils.Save_Source import Save_Source


class UrlSpiderSpider(scrapy.Spider):

    # 提取star_url, 提取series_id为做增量

    def get_list(sql):
        server = DATABASE_SERVER_NAME
        user = DATABASE_USER_NAME
        password = DATABASE_USER_PASSWORD
        database = DATABASE_NAME
        host = DATABASE_HOST
        conn = pymssql.connect(user=user,
                               password=password,
                               host=host,
                               database=database)
        list_df = pd.read_sql_query(sql, conn)
        sql_url = list_df.values.tolist()
        sql_list = []
        for id in sql_url:
            sql_list.append(id[0])
        return sql_list

    sql_url = """SELECT SERIE_URL FROM [stg].[CONFIG_SERIES]"""
    sql_id = """SELECT SPEC_ID FROM [stg].[CONFIGURATION_DETAILS_2018_01_25] GROUP BY SPEC_ID"""
    sql_spec_id = get_list(sql_id)
    start_urls = get_list(sql_url)
    name = "Configuration_Spider"

    def parse(self, response):
        # 将网页源代码存入.txt
        url = response.url
        file_name = re.findall(r"com\/(.+?)\/data",url)[0]
        if SAVE_SOURCE_DATA == 1:
            Save_Source(response.body, file_name)
        pattern_js = re.compile("var paraJson = (.+?);")
        js_list = re.findall(pattern_js, response.body.decode('utf-8'))
        js_item = js_list[0]
        str_json = json.loads(js_item)
        js_list = list(str_json)
        for each in self.dict_flatlist(js_list, i=1):
            yield each
        # 返回


    def dict_flatlist(self, d, i):
        #print(d)
        #x_list = json.loads(d)
        paramtypeitems = d[0]
        configtypeitems = d[1]
        #self.get_configuration(paramtypeitems, u'paramtypeitems')  # 定位第一段item
        #self.get_configuration(configtypeitems, u'configtypeitems')  # 定位第二段item
        for param, configtype in [(paramtypeitems, u'paramtypeitems'), (configtypeitems, u'configtypeitems')]:
            for each in self.get_configuration(param, configtype):
                yield each

    def get_configuration(self, dit, key):
        item = ChexunSpiderConfiguration()
        dit_result = dit[u'result']
        series_id = dit_result[u'seriesid']  # 得到series_id
        dit_typeitems = dit_result[key]
        for paramitems in dit_typeitems:
            if key == u'paramtypeitems':
                list_paramitems = paramitems[u'paramitems']  # 第二段为u'configitems'  第一段为[u'paramitems']
            else:
                list_paramitems = paramitems[u'configitems']
            for aim_dit in list_paramitems:
                if aim_dit[u'name']:
                    para_name = aim_dit[u'name']  # 得到 para_name
                    list_valueitems = aim_dit[u'valueitems']
                    for items in list_valueitems:
                        spec_id = items[u'specid']  # 得到 spec_id
                        para_value = items[u'value']  # 得到 para_value
                        #  给item赋值并返回
                        item['series_id'] = series_id
                        item['spec_id'] = spec_id
                        item['para_name'] = para_name
                        item['para_value'] = para_value
                        # 增量爬取 精确到车型
                        key_ = str(item['spec_id'])
                        if key_ not in self.sql_spec_id:
                            yield item

