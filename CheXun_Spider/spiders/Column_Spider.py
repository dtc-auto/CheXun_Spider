# -*- coding: utf-8 -*-
import json
import pymssql
import re
import pandas as pd
import scrapy
from items import ChexunSpiderColumn
from settings import *


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
    sql_name = """SELECT PARA_NAME FROM [stg].[CONFIG_ITEM] 
                GROUP BY PARA_NAME"""
    name_list = get_list(sql_name)
    start_urls = get_list(sql_url)
    name = "Column_Spider"

    def parse(self, response):
        pattern_js = re.compile("var paraJson = (.+?);")
        js_list = re.findall(pattern_js, response.body)
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
        item = ChexunSpiderColumn()
        dit_result = dit[u'result']
        dit_typeitems = dit_result[key]
        for paramitems in dit_typeitems:
            type_name = paramitems['name']
            type_id = paramitems['typeId']
            if key == u'paramtypeitems':
                list_paramitems = paramitems[u'paramitems']  # 第二段为u'configitems'  第一段为[u'paramitems']
            else:
                list_paramitems = paramitems[u'configitems']
            for aim_dit in list_paramitems:
                if aim_dit[u'name']:
                    para_name = aim_dit[u'name']  # 得到 para_name
                    para_id = aim_dit[u'id']
                    #  给item赋值并返回
                    item['para_id'] = para_id
                    item['para_name'] = para_name
                    item['type_name'] = type_name
                    item['type_id'] = type_id
                    key_ = item['para_name']

                    # 增量爬取 精确到车型

                    server = DATABASE_SERVER_NAME
                    user = DATABASE_USER_NAME
                    password = DATABASE_USER_PASSWORD
                    database = DATABASE_NAME
                    host = DATABASE_HOST
                    conn = pymssql.connect(user=user,
                                           password=password,
                                           host=host,
                                           database=database)
                    list_df = pd.read_sql_query(self.sql_name, conn)
                    sql_url = list_df.values.tolist()
                    sql_list = []
                    for id in sql_url:
                        sql_list.append(id[0])
                    self.name_list = sql_list
                    if key_ not in self.name_list:
                        yield item


